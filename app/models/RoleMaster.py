from pydantic import BaseModel
from typing import Optional, Union

class Details(BaseModel):
    formName: Optional[str] = None
    userId: int

class RoleMaster(BaseModel):
    details: Details
    RoleId: Optional[int] = None  # SQL numeric
    RoleName: Optional[str] = None
    AccessRights: Optional[str] = None
    IsAdmin: Optional[int] = None  # SQL bit
    Remark: Optional[str] = None

