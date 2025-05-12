from fastapi import APIRouter,HTTPException
from app.schemas.user import User,UpdateUser
from app.db.session import users_collection



users=APIRouter()

@users.post("/user")
def insert_user(user: User):
       try:
        user_dict = user.model_dump()
        result = users_collection.insert_one(user_dict)
        return {"id": str(result.inserted_id), "message": "User created"}
       except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       

@users.get("/getuser/{name}")
async def getuser(name:str):
    user_data = users_collection.find_one({"name": name})
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert ObjectId to string
    user_data["_id"] = str(user_data["_id"])

    return user_data
  
@users.delete("/deleteuser/{name}")
async def deleteuser(name:str):
    user_data = users_collection.delete_one({"name": name})
    if user_data.deleted_count==0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

@users.put("/updateuser/{name}")
def update(name:str,user_update:UpdateUser):
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    result = users_collection.update_one({"name": name}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}




