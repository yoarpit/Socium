from pydantic import BaseModel,Field,HttpUrl
from datetime import datetime,timezone
from typing import Optional
class Post(BaseModel):
    title: str
    content: str
    author_id: str
    image_url: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class EditPost(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    image_url: Optional[str] = None
