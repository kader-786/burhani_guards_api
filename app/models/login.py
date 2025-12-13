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

class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "data": {
                    "its_id": 12345678,
                    "full_name": "John Doe",
                    "role_id": 1,
                    "team_id": 1
                }
            }
        }
