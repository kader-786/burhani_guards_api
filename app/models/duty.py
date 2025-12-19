# app/models/duty.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any

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


class DutyByIdRequest(BaseModel):
    """Request model for getting duty by ID"""
    duty_id: int = Field(..., description="Duty ID to query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "duty_id": 1
            }
        }


class TeamsByJamiaatRequest(BaseModel):
    """Request model for getting teams by jamiaat"""
    jamiaat_id: int = Field(..., description="Jamiaat ID to query teams for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "jamiaat_id": 3
            }
        }


class DutyInsertRequest(BaseModel):
    """Request model for inserting a new duty"""
    team_id: int = Field(..., description="Team ID")
    miqaat_id: int = Field(..., description="Miqaat ID")
    quota: int = Field(..., description="Duty quota/capacity", gt=0)
    location: str = Field(..., description="Duty location", max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": 2,
                "miqaat_id": 5,
                "quota": 10,
                "location": "Main Gate"
            }
        }


class DutyUpdateRequest(BaseModel):
    """Request model for updating an existing duty"""
    duty_id: int = Field(..., description="Duty ID to update")
    team_id: int = Field(..., description="Team ID")
    miqaat_id: int = Field(..., description="Miqaat ID")
    quota: int = Field(..., description="Duty quota/capacity", gt=0)
    location: str = Field(..., description="Duty location", max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "duty_id": 1,
                "team_id": 2,
                "miqaat_id": 5,
                "quota": 12,
                "location": "Main Gate - Section A"
            }
        }


class DutyDeleteRequest(BaseModel):
    """Request model for deleting a duty"""
    duty_id: int = Field(..., description="Duty ID to delete")
    
    class Config:
        json_schema_extra = {
            "example": {
                "duty_id": 1
            }
        }


class GuardDutyInsertRequest(BaseModel):
    """
    Request model for guard duty insert/delete operations
    
    **For INSERT operation (flag='I'):**
    - Required: form_name, flag='I', duty_id, team_id, miqaat_id, its_id
    - user_id is automatically taken from JWT token
    
    **For DELETE operation (flag='D'):**
    - Required: form_name, flag='D', guard_duty_id
    - user_id is automatically taken from JWT token
    """
    form_name: str = Field(..., description="Form name for activity logging")
    flag: str = Field(..., description="Operation flag: 'I' for Insert, 'D' for Delete")
    
    # INSERT operation fields
    duty_id: Optional[int] = Field(None, description="Duty ID (required for INSERT)")
    team_id: Optional[int] = Field(None, description="Team ID (required for INSERT)")
    miqaat_id: Optional[int] = Field(None, description="Miqaat ID (required for INSERT)")
    its_id: Optional[int] = Field(None, description="ITS ID of the guard (required for INSERT)")
    
    # DELETE operation field
    guard_duty_id: Optional[int] = Field(None, description="Guard Duty ID (required for DELETE)")
    
    @field_validator('flag')
    @classmethod
    def validate_flag(cls, v):
        """Validate that flag is either 'I' or 'D'"""
        if v.upper() not in ['I', 'D']:
            raise ValueError("Flag must be 'I' (Insert) or 'D' (Delete)")
        return v.upper()
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Insert Guard Duty",
                    "description": "Assign a guard to a duty",
                    "value": {
                        "form_name": "GUARD_DUTY_FORM",
                        "flag": "I",
                        "duty_id": 1,
                        "team_id": 2,
                        "miqaat_id": 17,
                        "its_id": 10001002
                    }
                },
                {
                    "summary": "Delete Guard Duty",
                    "description": "Remove a guard from a duty (soft delete)",
                    "value": {
                        "form_name": "GUARD_DUTY_FORM",
                        "flag": "D",
                        "guard_duty_id": 15
                    }
                }
            ]
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


class DutyCRUDResponse(BaseModel):
    """Response model for duty CRUD operations"""
    success: bool
    status_code: int
    message: str
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Insert Success",
                    "value": {
                        "success": True,
                        "status_code": 201,
                        "message": "Duty created successfully",
                        "data": {"result_code": 1}
                    }
                },
                {
                    "summary": "Update Success",
                    "value": {
                        "success": True,
                        "status_code": 200,
                        "message": "Duty updated successfully",
                        "data": {"result_code": 2}
                    }
                },
                {
                    "summary": "Delete Success",
                    "value": {
                        "success": True,
                        "status_code": 200,
                        "message": "Duty deleted successfully",
                        "data": {"result_code": 3}
                    }
                },
                {
                    "summary": "Duplicate",
                    "value": {
                        "success": False,
                        "status_code": 409,
                        "message": "Duty already exists with same team, miqaat, and location",
                        "data": {"result_code": 4}
                    }
                },
                {
                    "summary": "Error",
                    "value": {
                        "success": False,
                        "status_code": 500,
                        "message": "Failed to process duty operation",
                        "data": {"result_code": 0}
                    }
                }
            ]
        }


class GuardDutyInsertResponse(BaseModel):
    """Response model for guard duty insert/delete operations"""
    success: bool
    status_code: int
    message: str
    result: int
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Insert Success",
                    "value": {
                        "success": True,
                        "status_code": 201,
                        "message": "Guard duty assigned successfully",
                        "result": 1
                    }
                },
                {
                    "summary": "Delete Success",
                    "value": {
                        "success": True,
                        "status_code": 200,
                        "message": "Guard duty removed successfully",
                        "result": 3
                    }
                },
                {
                    "summary": "Duplicate",
                    "value": {
                        "success": False,
                        "status_code": 409,
                        "message": "Guard already assigned to this duty",
                        "result": 4
                    }
                },
                {
                    "summary": "Error",
                    "value": {
                        "success": False,
                        "status_code": 500,
                        "message": "Failed to process guard duty operation",
                        "result": 0
                    }
                }
            ]
        }