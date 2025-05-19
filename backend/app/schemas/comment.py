from pydantic import BaseModel
from datetime import datetime

class CreateComment(BaseModel):
    post_id: str
    content: str

class CommentOut(BaseModel):
    id: str
    post_id: str
    author: str
    content: str
    created_at: datetime


class UpdateCommentModel(BaseModel):
    content: str