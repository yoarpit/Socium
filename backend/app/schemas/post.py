# app/schemas/post.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime,timezone

class CreatePostModel(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostOut(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str]
    created_at: datetime
    author: str  # username or user ID


class UpdatePostModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
    image_url: Optional[str]    
