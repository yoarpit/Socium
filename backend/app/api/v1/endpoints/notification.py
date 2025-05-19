from fastapi import APIRouter, Depends
from app.api.v1.endpoints.auth import get_current_user
from bson import ObjectId
from app.db.session import notifications_collection
from datetime import datetime,timezone
from app.schemas.notification import NotificationOut
notification_router = APIRouter()


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


@notification_router.get("/notifications", response_model=list[NotificationOut])
def get_notifications(current_user: dict = Depends(get_current_user)):
    cursor = notifications_collection.find({"recipient": current_user["username"]}).sort("timestamp", -1)
    return [
        {
            "id": str(n["_id"]),
            "recipient": n["recipient"],
            "sender": n["sender"],
            "type": n["type"],
            "post_id": n["post_id"],
            "message": n["message"],
            "is_read": n["is_read"],
            "timestamp": n["timestamp"]
        }
        for n in cursor
    ]
