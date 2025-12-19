# app/models/mumin_sync.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MuminSyncRequest(BaseModel):
    """Request model for syncing ITS data to mumin_master table"""
    its_id: str = Field(..., description="ITS ID to sync")
    
    class Config:
        json_schema_extra = {
            "example": {
                "its_id": "30327082"
            }
        }


class MuminSyncResponse(BaseModel):
    """Response model for mumin sync operation"""
    success: bool
    message: str
    its_id: Optional[str] = None
    operation: Optional[str] = None  # "INSERT" or "UPDATE"
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Member data synced successfully",
                "its_id": "30327082",
                "operation": "INSERT",
                "data": {
                    "full_name": "Mohammed bhai Mustafa bhai Shergadwala",
                    "mobile": "+918080692965",
                    "email": "mshergad@gmail.com"
                }
            }
        }