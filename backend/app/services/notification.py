from app.db.session import notifications_collection
from datetime import datetime,timezone

def create_notification(recipient, sender, post_id, type_):
    messages = {
        "like": f"{sender} liked your post",
        "comment": f"{sender} commented on your post"
    }

    notification = {
        "recipient": recipient,
        "sender": sender,
        "type": type_,
        "post_id": post_id,
        "message": messages.get(type_, ""),
        "is_read": False,
        "timestamp": datetime.now(timezone.utc)
    }

    notifications_collection.insert_one(notification)
