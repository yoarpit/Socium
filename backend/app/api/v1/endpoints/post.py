from fastapi import APIRouter
from app.schemas.post import Post,EditPost
from app.db.session import users_collection


post=APIRouter()

@post.get("/post")
async def getpost():
    return{"post":"working"}