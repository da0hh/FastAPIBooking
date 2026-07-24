from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SignUp(BaseModel):
    username: str
    password: str

class LoginInAcc(BaseModel):
    username: str
    password: str

class LoginRead(BaseModel):
    user_id: int
    username:str
    date_registration: datetime
    #model_config = ConfigDict(from_attributes=True)

class ChangePassword(BaseModel):
    new_password: str

class ChangeUsername(BaseModel):
    new_username: str

class DeleteAccount(BaseModel):
    user_id: int
    password: int