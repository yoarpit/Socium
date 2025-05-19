from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()


app.include_router(api_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
