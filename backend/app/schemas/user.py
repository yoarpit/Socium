from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name:str
    age:int
    location:str
    education:str


class UpdateUser(BaseModel):
    name:Optional[str]
    age:Optional[int]
    location:Optional[str]
    education:Optional[str]
