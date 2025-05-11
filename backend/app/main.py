from fastapi import FastAPI
from app.api.v1.endpoints.users import users

app=FastAPI()


app.include_router(users, prefix="/api")

