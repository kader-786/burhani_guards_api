# app/models/team.py
from pydantic import BaseModel, Field
from typing import Optional, Any

class TeamRequest(BaseModel):
    """Request model for team queries"""
    team_id: int = Field(..., description="Team ID to query members for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1
            }
        }


class TeamResponse(BaseModel):
    """Response model for team queries"""
    success: bool
    status_code: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Team members retrieved successfully",
                "data": [
                    {
                        "its_id": 10001001,
                        "full_name": "Ali Hussain",
                        "position_name": "Commander",
                        "mobile": "9876543210"
                    }
                ]
            }
        }