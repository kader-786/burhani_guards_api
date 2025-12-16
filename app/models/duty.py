# app/models/duty.py
from pydantic import BaseModel, Field
from typing import Optional, List, Any

class TeamDutyRequest(BaseModel):
    """Request model for team duty queries"""
    team_id: int = Field(..., description="Team ID to query duties for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1
            }
        }


class GuardDutyRequest(BaseModel):
    """Request model for guard duty queries"""
    its_id: int = Field(..., description="ITS ID to query duties for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "its_id": 10001001
            }
        }


class DutyResponse(BaseModel):
    """Response model for duty queries"""
    success: bool
    status_code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Duties retrieved successfully",
                "data": [
                    {
                        "duty_id": 1,
                        "team_id": 1,
                        "miqaat_id": 1,
                        "miqaat_name": "Ashara Mubaraka 1446H",
                        "location": "Main Gate"
                    }
                ]
            }
        }