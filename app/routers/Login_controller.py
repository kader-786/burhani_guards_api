# app/routers/Login_controller.py
from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.login import (
    LoginRequest, LoginResponse, TokenData,
    RefreshTokenRequest, RefreshTokenResponse
)
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import (
    create_access_token, create_refresh_token,
    refresh_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
import traceback
import logging
import json
from psycopg2.extras import RealDictCursor  # ← ADD THIS IMPORT


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Login", tags=["Login"])


@router.post("/CheckLogin", response_model=LoginResponse)
async def check_login(payload: LoginRequest, request: Request):
    """
    Authenticate user and return user details with JWT tokens
    
    - **username**: User's ITS ID (numeric)
    - **password**: User's password
    
    Returns user information, authentication status, and JWT tokens
    """
    try:
        # Get client IP address
        client_ip = request.client.host if request.client else "unknown"
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.com_spr_login_json",
                {
                    "p_query_type": "CHECK_LOGIN",
                    "p_its_id": int(payload.username) if payload.username.isdigit() else 0,
                    "p_password": payload.password,
                    "p_ip_address": client_ip
                }
            )
            
            # Log the result for debugging
            logger.info(f"Login attempt for ITS ID: {payload.username}")
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result
            if result:
                # The function returns a JSON object
                if isinstance(result, str):
                    result = json.loads(result)
                
                # Check if the result has the expected structure
                if result and isinstance(result, dict):
                    success = result.get("success", False)
                    message = result.get("message", "Login failed")
                    data = result.get("data", None)
                    
                    # If login is successful, generate JWT tokens
                    if success and data:
                        # Prepare token payload with essential user info
                        token_payload = {
                            "its_id": data.get("its_id"),
                            "full_name": data.get("full_name"),
                            "email": data.get("email"),
                            "team_id": data.get("team_id"),
                            "position_id": data.get("position_id"),
                            "role_id": data.get("role_id"),
                            "is_admin": data.get("is_admin", False),
                            "access_rights": data.get("access_rights", ""),
                            "jamaat_id": data.get("jamaat_id"),
                            "jamiaat_id": data.get("jamiaat_id")
                        }
                        
                        # Generate access and refresh tokens
                        access_token = create_access_token(token_payload)
                        refresh_token = create_refresh_token(token_payload)
                        
                        # Create token response
                        token_data = TokenData(
                            access_token=access_token,
                            refresh_token=refresh_token,
                            token_type="bearer",
                            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
                        )
                        
                        return LoginResponse(
                            success=True,
                            message=message,
                            data=data,
                            tokens=token_data
                        )
                    else:
                        # Login failed
                        return LoginResponse(
                            success=False,
                            message=message,
                            data=None,
                            tokens=None
                        )
                else:
                    return LoginResponse(
                        success=False,
                        message="Invalid response format from server",
                        data=None,
                        tokens=None
                    )
            else:
                return LoginResponse(
                    success=False,
                    message="No response from authentication server",
                    data=None,
                    tokens=None
                )
            
    except Exception as ex:
        logger.error(f"Login error: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


@router.post("/RefreshToken", response_model=RefreshTokenResponse)
async def refresh_token(payload: RefreshTokenRequest):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    
    Returns new access and refresh tokens
    """
    try:
        # Use the refresh_access_token function from auth module
        new_access_token, new_refresh_token = await refresh_access_token(
            payload.refresh_token
        )
        
        # Create token response
        token_data = TokenData(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return RefreshTokenResponse(
            success=True,
            message="Token refreshed successfully",
            tokens=token_data
        )
        
    except HTTPException as he:
        raise he
    except Exception as ex:
        logger.error(f"Token refresh error: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


@router.get("/Me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Protected endpoint - requires valid access token
    Returns the user information from the token
    """
    return {
        "success": True,
        "message": "User information retrieved successfully",
        "data": current_user
    }


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Burhani Guards Login API",
        "database": "PostgreSQL",
        "authentication": "JWT"
    }


# ============================================================================
# NEW MAINTENANCE ENDPOINTS
# ============================================================================

@router.get("/Maintenance/get-all")
async def get_all_maintenance():
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Call function directly with fetchall()
                cursor.execute(
                    f"SELECT * FROM {PG_CONFIG['schema']}.com_spr_maintenance(%s)",
                    ('SELECT-ALL',)
                )
                
                # ✅ Get all rows
                results = cursor.fetchall()
                
                # Convert to list of dicts
                data = [dict(row) for row in results]
                
                return {
                    "success": True,
                    "message": "Maintenance settings retrieved successfully",
                    "data": data
                }
            
    except Exception as ex:
        logger.error(f"Error retrieving maintenance settings: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


@router.get("/Maintenance/get-by-name/{maint_name}")
async def get_maintenance_by_name(
    maint_name: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.com_spr_maintenance",
                {
                    "p_query_type": "SELECT-BY-ID",
                    "p_maint_name": maint_name
                }
            )
            
            logger.info(f"Maintenance setting '{maint_name}' requested by user: {current_user.get('its_id')}")
            
            # Check if result was found
            if result:
                # If result is a list with one item, extract it
                if isinstance(result, list) and len(result) > 0:
                    data = result[0]
                else:
                    data = result
                
                return {
                    "success": True,
                    "message": f"Maintenance setting '{maint_name}' retrieved successfully",
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "message": f"Maintenance setting '{maint_name}' not found",
                    "data": None
                }
            
    except Exception as ex:
        logger.error(f"Error retrieving maintenance setting '{maint_name}': {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )
 