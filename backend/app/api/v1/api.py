from fastapi import APIRouter
from app.api.v1.endpoints import auth,users,post,likes,notification,comment
api_router=APIRouter()

api_router.include_router(auth.auth,prefix="/auth", tags=["auth"])
api_router.include_router(users.users,prefix="/users", tags=["users"])
api_router.include_router(likes.like_router,prefix="/likes", tags=["likes"])
api_router.include_router(notification.notification_router,prefix="/notification", tags=["notification"])
api_router.include_router(comment.comment_router,prefix="/comment", tags=["comment"])
api_router.include_router(post.post,prefix="/post", tags=["post"])

