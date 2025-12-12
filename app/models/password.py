# app/models/password.py
from pydantic import BaseModel
from typing import Optional

class Details(BaseModel):
    formName: Optional[str] = None
    userId: Optional[int] = None

class Password(BaseModel):
    details: Optional[Details] = None
    UserName: Optional[str] = None
    Pass: Optional[str] = None
    New_Password: Optional[str] = None
    Txt_Current_Password: Optional[str] = None
    txt_FullName: Optional[str] = None
    txt_mob: Optional[str] = None
    txt_email: Optional[str] = None
