from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from datetime import datetime,timezone

class RegisterModel(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)

    
class VerifyOTPModel(BaseModel):
    email: EmailStr
    otp_code: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr

class TokenOut(BaseModel):
    access_token: str
