# app/models/miqaat.py
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class MiqaatRequest(BaseModel):
    """Request model for miqaat queries that require miqaat_id"""
    miqaat_id: int = Field(..., description="Miqaat ID to query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_id": 1
            }
        }


class JamaatsByJamiaatMiqaatRequest(BaseModel):
    """Request model for getting jamaats by jamiaat_id"""
    jamiaat_id: int = Field(..., description="Jamiaat ID to query jamaats for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "jamiaat_id": 3
            }
        }


class MiqaatInsertRequest(BaseModel):
    """Request model for inserting a new miqaat"""
    miqaat_name: str = Field(..., description="Name of the miqaat", max_length=100)
    miqaat_type_id: int = Field(..., description="Miqaat type ID")
    start_date: datetime = Field(..., description="Start date and time of miqaat")
    end_date: datetime = Field(..., description="End date and time of miqaat")
    venue: str = Field(..., description="Venue location", max_length=200)
    jamaat_id: int = Field(..., description="Jamaat ID")
    jamiaat_id: int = Field(..., description="Jamiaat ID")
    quantity: int = Field(..., description="Quantity/capacity")
    is_active: Optional[bool] = Field(True, description="Active status flag")
    reporting_time: datetime = Field(..., description="Reporting time for miqaat")

    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_name": "Qadambosi - Andheri",
                "miqaat_type_id": 1,
                "start_date": "2025-01-15T18:00:00",
                "end_date": "2025-01-15T22:00:00",
                "venue": "Andheri Masjid",
                "jamaat_id": 1,
                "jamiaat_id": 3,
                "quantity": 50,
                "is_active": True
            }
        }


class MiqaatUpdateRequest(BaseModel):
    """Request model for updating an existing miqaat"""
    miqaat_id: int = Field(..., description="Miqaat ID to update")
    miqaat_name: str = Field(..., description="Name of the miqaat", max_length=100)
    miqaat_type_id: int = Field(..., description="Miqaat type ID")
    start_date: datetime = Field(..., description="Start date and time of miqaat")
    end_date: datetime = Field(..., description="End date and time of miqaat")
    venue: str = Field(..., description="Venue location", max_length=200)
    jamaat_id: int = Field(..., description="Jamaat ID")
    jamiaat_id: int = Field(..., description="Jamiaat ID")
    quantity: int = Field(..., description="Quantity/capacity")
    is_active: Optional[bool] = Field(None, description="Active status flag")
    reporting_time: datetime = Field(..., description="Reporting time for miqaat")

    
    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_id": 1,
                "miqaat_name": "Qadambosi - Andheri Updated",
                "miqaat_type_id": 1,
                "start_date": "2025-01-15T18:00:00",
                "end_date": "2025-01-15T22:00:00",
                "venue": "Andheri Masjid - Main Hall",
                "jamaat_id": 1,
                "jamiaat_id": 3,
                "quantity": 60,
                "is_active": True
            }
        }


class MiqaatDeleteRequest(BaseModel):
    """Request model for deleting a miqaat"""
    miqaat_id: int = Field(..., description="Miqaat ID to delete")
    
    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_id": 1
            }
        }


class MiqaatResponse(BaseModel):
    """Response model for miqaat queries"""
    success: bool
    status_code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Miqaat data retrieved successfully",
                "data": [
                    {
                        "miqaat_id": 1,
                        "miqaat_name": "Qadambosi - Andheri",
                        "start_date": "2025-01-15T18:00:00"
                    }
                ]
            }
        }