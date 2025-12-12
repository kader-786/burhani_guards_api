from pydantic import BaseModel

class Login(BaseModel):
    UserName: str
    Password: str
