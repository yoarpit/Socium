from app.schemas.auth import RegisterModel,UserOut,LoginModel,TokenOut,VerifyOTPModel
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime,timedelta,timezone
from app.core.security import  hash_password,verify_password,create_access_token,decode_access_token,Header,generate_otp
from app.db.session import auth_collection,token_blacklist
from app.configure.email_utility import send_otp_email
auth=APIRouter()


@auth.post("/register", response_model=UserOut)
def register(user: RegisterModel):
    if auth_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}]}):
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_pw = hash_password(user.password)
    otp_code = generate_otp()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)
    auth_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_pw,
        "email_verified": False,
        "otp_code": otp_code,
        "otp_expiry": expiry
    })

    send_otp_email(user.email, otp_code)
    return {"username": user.username, "email": user.email}



@auth.post("/verify-email")
def verify_email(data: VerifyOTPModel):
    user = auth_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user["email_verified"]:
        return {"message": "Email already verified."}

    if user["otp_code"] != data.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP code.")
    
    

    # if datetime.now(timezone.utc) > user["otp_expiry"]:
    #     raise HTTPException(status_code=400, detail="OTP expired.")
    expiry = user["otp_expiry"]
    if expiry.tzinfo is not None:
        expiry = expiry.replace(tzinfo=None)

    if datetime.utcnow() > expiry:
       raise HTTPException(status_code=400, detail="OTP expired.")

    auth_collection.update_one({"email": data.email}, {"$set": {"email_verified": True}, "$unset": {"otp_code": "", "otp_expiry": ""}})
    return {"message": "Email verified successfully."}

@auth.post("/login", response_model=TokenOut)
def login(data: LoginModel):
    user = auth_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if not user.get("email_verified", False):
        raise HTTPException(status_code=403, detail="Email not verified.")

    token = create_access_token({"sub": user["username"]})

    print(token)
    return {"access_token": token}




@auth.get("/me", response_model=UserOut)
def get_me(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = Authorization.split(" ")[1]
    payload = decode_access_token(token)
    username = payload.get("sub")

    user = auth_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user["username"], "email": user["email"]}




@auth.post("/logout")
def logout(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = Authorization.split(" ")[1]
    payload = decode_access_token(token)
    print(token)
    token_blacklist.insert_one({
        "token": token,
        "exp": datetime.fromtimestamp(payload["exp"], tz=timezone.utc)  
    })

    return {"message": "Signed out successfully"}