from pydantic import BaseModel
from typing import Optional

class Points(BaseModel):
    Form_Name: Optional[str] = None
    User_ID: Optional[str] = None
    Troop_ID: Optional[str] = None
    Meeting_ID: Optional[str] = None
    Activity_ID: Optional[str] = None
    Patrol_ID: Optional[str] = None
    Points_Type_ID: Optional[str] = None
    Round_ID: Optional[str] = None
    Point: Optional[str] = None
    Remarks: Optional[str] = None
    Year_ID: Optional[str] = None
