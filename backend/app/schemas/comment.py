from pydantic import BaseModel
from datetime import time
from typing import Optional


class Comment(BaseModel):
    name:str
    comment:str
    time:time

class EditComment(BaseModel):
    name:Optional[str]
    comment:Optional[str]
    time:Optional[time]
