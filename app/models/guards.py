# app/models/guards.py
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import date as DateType

class GuardsByDateRequest(BaseModel):
    """Request model for getting guards by miqaat date"""
    miqaat_date: DateType = Field(..., description="Miqaat date to query guards for (YYYY-MM-DD)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_date": "2025-01-10"
            }
        }


class GuardCheckRequest(BaseModel):
    """Request model for guard check by ITS ID"""
    its_id: int = Field(..., description="ITS ID to check guard information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "its_id": 10001001
            }
        }


# ← ADD THIS NEW MODEL
class GuardsWithDutyRequest(BaseModel):
    """Request model for getting all guards with duty assignment status"""
    miqaat_id: int = Field(..., description="Miqaat ID")
    duty_id: int = Field(..., description="Duty ID")
    team_id: int = Field(..., description="Team ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "miqaat_id": 1,
                "duty_id": 3,
                "team_id": 2
            }
        }


class GuardsResponse(BaseModel):
    """Response model for guards queries"""
    success: bool
    status_code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Guards retrieved successfully",
                "data": [
                    {
                        "its_id": 10001001,
                        "full_name": "Ali Hussain",
                        "team_name": "Team A",
                        "position_name": "Commander"
                    }
                ]
            }
        }