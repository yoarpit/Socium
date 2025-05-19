from fastapi import APIRouter, Depends,HTTPException
from datetime import datetime,timezone
from app.schemas.post import CreatePostModel, PostOut, UpdatePostModel
from app.db.session import post_collection
from app.api.v1.endpoints.auth import get_current_user
from bson import ObjectId

post = APIRouter()

@post.post("/posts", response_model=PostOut)
def create_post(data: CreatePostModel,current_user: dict = Depends(get_current_user)):
    post_data = {
        "title": data.title,
        "content": data.content,
        "image_url": data.image_url,
        "created_at": datetime.now(timezone.utc),
        "author": current_user["username"]
    }

    result = post_collection.insert_one(post_data)
    post_data["_id"] = str(result.inserted_id)

    return {
        "id": post_data["_id"],
        **data.model_dump(),
        "created_at": post_data["created_at"],
        "author": post_data["author"]
    }




@post.put("/posts/{post_id}")
def update_post(post_id: str, data: UpdatePostModel, current_user: dict = Depends(get_current_user)):
    post = post_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})
    return {"message": "Post updated successfully"}

@post.delete("/posts/{post_id}")
def delete_post(post_id: str, current_user: dict = Depends(get_current_user)):
    post = post_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    post_collection.delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post deleted successfully"}