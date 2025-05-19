from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.db.session import post_collection
from app.api.v1.endpoints.auth import get_current_user

like_router = APIRouter()

@like_router.post("/posts/{post_id}/like")
def like_post(post_id: str, current_user: dict = Depends(get_current_user)):
    post = post_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user = current_user["username"]
    if user in post.get("likes", []):
        # Unlike
        post_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$pull": {"likes": user}}
        )
        return {"message": "Unliked post"}
    else:
        # Like
        post_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$addToSet": {"likes": user}}  # add only if not present
        )
        return {"message": "Liked post"}
