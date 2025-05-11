from fastapi import APIRouter
from app.schemas.user import User


users=APIRouter()

@users.get("/user/")
def home():
    return {"home":"my"}
