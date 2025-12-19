# app/models/attendance.py
from pydantic import BaseModel, Field
from typing import Optional

class AttendanceInsertRequest(BaseModel):
    """Request model for inserting attendance record"""
    form_name: str = Field(..., description="Name of the form calling this endpoint")
    user_id: int = Field(..., description="User ID performing the insert")
    its_id: int = Field(..., description="ITS ID of the person")
    miqaat_id: int = Field(..., description="Miqaat ID")
    team_id: int = Field(..., description="Team ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "form_name": "ATTENDANCE_FORM",
                "user_id": 3,
                "its_id": 10001002,
                "miqaat_id": 17,
                "team_id": 2
            }
        }


class AttendanceResponse(BaseModel):
    """Response model for attendance operations"""
    success: bool
    status_code: Optional[int] = None
    message: Optional[str] = None
    result: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Attendance record inserted successfully",
                "result": 1
            }
        }