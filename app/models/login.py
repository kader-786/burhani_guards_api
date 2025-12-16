# app/models/login.py
from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., description="User's ITS ID or username")
    password: str = Field(..., description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "12345678",
                "password": "password123"
            }
        }


class TokenData(BaseModel):
    """Token data model"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class LoginResponse(BaseModel):
    """Login response model with JWT tokens"""
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
    tokens: Optional[TokenData] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "data": {
                    "its_id": 12345678,
                    "full_name": "John Doe",
                    "role_id": 1,
                    "team_id": 1,
                    "is_admin": False
                },
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 3600
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request model"""
    refresh_token: str = Field(..., description="Refresh token to get new access token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenResponse(BaseModel):
    """Refresh token response model"""
    success: bool
    message: Optional[str] = None
    tokens: Optional[TokenData] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Token refreshed successfully",
                "tokens": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 3600
                }
            }
        }