# app/auth.py
"""
JWT Authentication Module
Handles token generation, validation, and user authorization
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-CHANGE-THIS-in-production-use-openssl-rand-hex-32")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))  # 7 days

# Security scheme for Swagger UI
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: User data to encode (its_id, role_id, is_admin, etc.)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    
    Example:
        token = create_access_token({"its_id": 12345678, "role_id": 1})
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token (longer expiration)
    
    Args:
        data: User data to encode
    
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token has expired
        exp = payload.get("exp")
        if exp is None:
            raise credentials_exception
        
        if datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user from JWT token
    
    Usage in protected endpoints:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            return {"user": current_user}
    
    Args:
        credentials: HTTP Authorization credentials with Bearer token
    
    Returns:
        Dictionary containing user information from token
    
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    # Verify it's an access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user data from token
    its_id = payload.get("its_id")
    if its_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


async def require_admin(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency to require admin privileges
    
    Usage:
        @router.delete("/users/{user_id}")
        async def delete_user(user_id: int, admin: dict = Depends(require_admin)):
            # Only admins can access this
            return {"message": "User deleted"}
    
    Args:
        current_user: Current authenticated user from get_current_user
    
    Returns:
        User dictionary if user is admin
    
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user


async def check_permission(
    required_permission: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Check if user has a specific permission
    
    Args:
        required_permission: Permission string to check
        current_user: Current authenticated user
    
    Returns:
        User dictionary if user has permission
    
    Raises:
        HTTPException: If user doesn't have the required permission
    """
    # Admin has all permissions
    if current_user.get("is_admin", False):
        return current_user
    
    # Check if user has the required permission
    access_rights = current_user.get("access_rights", "")
    user_permissions = [p.strip() for p in access_rights.split(",") if p.strip()]
    
    if required_permission not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: '{required_permission}' required"
        )
    
    return current_user


def create_permission_checker(required_permission: str):
    """
    Factory function to create permission checker dependency
    
    Usage:
        # Create a dependency that checks for specific permission
        require_view_duties = create_permission_checker("view_duties")
        
        @router.get("/duties")
        async def get_duties(user: dict = Depends(require_view_duties)):
            # Only users with 'view_duties' permission can access
            return {"duties": [...]}
    
    Args:
        required_permission: Permission string to check
    
    Returns:
        Dependency function that checks the permission
    """
    async def permission_checker(
        current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        return await check_permission(required_permission, current_user)
    
    return permission_checker


class OptionalAuth:
    """
    Dependency for optional authentication
    Returns user if token is provided and valid, None otherwise
    
    Usage:
        @router.get("/public-or-private")
        async def mixed_route(user: Optional[dict] = Depends(OptionalAuth())):
            if user:
                return {"message": f"Hello {user['full_name']}!"}
            return {"message": "Hello Guest!"}
    """
    
    async def __call__(
        self,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(
            HTTPBearer(auto_error=False)
        )
    ) -> Optional[Dict[str, Any]]:
        if credentials is None:
            return None
        
        try:
            token = credentials.credentials
            payload = verify_token(token)
            return payload
        except HTTPException:
            return None


# Utility function to refresh access token using refresh token
async def refresh_access_token(
    refresh_token: str
) -> tuple[str, str]:
    """
    Generate new access token using refresh token
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        Tuple of (new_access_token, new_refresh_token)
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        
        # Remove token metadata before creating new tokens
        user_data = {k: v for k, v in payload.items() if k not in ["exp", "iat", "type"]}
        
        # Create new tokens
        new_access_token = create_access_token(user_data)
        new_refresh_token = create_refresh_token(user_data)
        
        return new_access_token, new_refresh_token
        
    except JWTError as e:
        logger.error(f"Refresh token error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token"
        )