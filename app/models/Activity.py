from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ActivityDetail(BaseModel):
    ID: Optional[int]
    CONTROL_ID: Optional[int]
    ACTIVITY_ID: Optional[int]
    ROUND_NUMBER: Optional[int]
    ROUND_NAME: Optional[str]
    FLAG: Optional[str]

class Activity(BaseModel):
    Form_Name: Optional[str] = None
    UserID: Optional[int] = None
    User_ID: Optional[int] = None
    Activity_ID: Optional[int] = None
    Activity_Name: Optional[str] = None
    Meeting_ID: Optional[int] = None
    Activity_Date: Optional[date] = None
    Points_Type_ID: Optional[int] = None
    Max_Points: Optional[int] = None
    Has_Rounds: Optional[bool] = None
    Rounds: Optional[int] = None
    Troop_ID: Optional[int] = None
    Activity_Master_Detail: Optional[str] = None
