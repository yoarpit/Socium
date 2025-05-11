from pydantic import BaseModel
from datetime import time
from typing import Optional
class Post(BaseModel):
    name:str
    post:str
    time:time

class EditPost(BaseModel):
    name:Optional[str]
    post:Optional[str]
    time:Optional[time]