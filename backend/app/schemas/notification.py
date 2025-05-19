# schemas/notification.py

from pydantic import BaseModel
from datetime import datetime

class NotificationOut(BaseModel):
    id: str
    recipient: str
    sender: str
    type: str
    post_id: str
    message: str
    is_read: bool
    timestamp: datetime
