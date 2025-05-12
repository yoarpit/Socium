from fastapi import APIRouter
from app.api.v1.endpoints import auth,users,post,likes,notification,comment
api_router=APIRouter()

# api_router.include_router(auth,prefix="/auth", tags=["auth"])
api_router.include_router(users.users,prefix="/users", tags=["users"])
# api_router.include_router(likes,prefix="/likes", tags=["likes"])
# api_router.include_router(notification,prefix="/notification", tags=["notification"])
# api_router.include_router(comment,prefix="/comment", tags=["comment"])
api_router.include_router(post.post,prefix="/post", tags=["post"])

