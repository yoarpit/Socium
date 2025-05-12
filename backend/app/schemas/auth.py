from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date,time

class Auth(BaseModel):
    name:str
    email:EmailStr
    password:str
    time:time
    time:date


class UpdateAuth(BaseModel):
    name:Optional[str]
    email:Optional[EmailStr]
    password:Optional[str]
