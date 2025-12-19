# app/models/team.py
from pydantic import BaseModel, Field
from typing import Optional, Any, List

class TeamRequest(BaseModel):
    """Request model for team queries that require team_id"""
    team_id: int = Field(..., description="Team ID to query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1
            }
        }


# ← ADD THIS NEW MODEL
class JamaatsByJamiaatRequest(BaseModel):
    """Request model for getting jamaats by jamiaat_id"""
    jamiaat_id: int = Field(..., description="Jamiaat ID to query jamaats for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "jamiaat_id": 3
            }
        }


class TeamInsertRequest(BaseModel):
    """Request model for inserting a new team"""
    team_name: str = Field(..., description="Name of the team", max_length=100)
    jamiaat_id: int = Field(..., description="Jamiaat ID")
    jamaat_ids: List[int] = Field(..., description="List of Jamaat IDs to link with the team")
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_name": "Team Alpha",
                "jamiaat_id": 3,
                "jamaat_ids": [1, 3, 5]
            }
        }


class TeamUpdateRequest(BaseModel):
    """Request model for updating an existing team"""
    team_id: int = Field(..., description="Team ID to update")
    team_name: str = Field(..., description="Name of the team", max_length=100)
    jamiaat_id: int = Field(..., description="Jamiaat ID")
    jamaat_ids: List[int] = Field(..., description="List of Jamaat IDs to link with the team")
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 1,
                "team_name": "Team Alpha Updated",
                "jamiaat_id": 3,
                "jamaat_ids": [1, 3, 5, 7]
            }
        }


class TeamDeleteRequest(BaseModel):
    """Request model for deleting a team"""
    team_id: int = Field(..., description="Team ID to delete")
    
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
                "message": "Team data retrieved successfully",
                "data": [
                    {
                        "team_id": 1,
                        "team_name": "Team A"
                    }
                ]
            }
        }