# app/models/its_api.py
from pydantic import BaseModel, Field
from typing import Optional, Any

class ITSAPIRequest(BaseModel):
    """Request model for ITS API calls"""
    its_id: str = Field(..., description="ITS ID to query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "its_id": "10001001"
            }
        }


class ITSAPIResponse(BaseModel):
    """Response model for ITS API calls"""
    success: bool
    message: Optional[str] = None
    its_id: Optional[str] = None
    data: Optional[Any] = None
    raw_response: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Data retrieved successfully",
                "its_id": "10001001",
                "data": {
                    "field1": "value1",
                    "field2": "value2"
                },
                "raw_response": "<?xml version='1.0'?>..."
            }
        }