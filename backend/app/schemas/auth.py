from pydantic import BaseModel
from typing import Optional
from datetime import date,time

class Auth(BaseModel):
    name:str
    email:str
    password:str
    time:time
    time:date


class UpdateAuth(BaseModel):
    name:Optional[str]
    email:Optional[str]
    password:Optional[str]
