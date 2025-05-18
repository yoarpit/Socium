from fastapi import APIRouter,HTTPException
from app.schemas.post import Post,EditPost
from app.db.session import post_collection,users_collection
from bson import ObjectId


post=APIRouter()

@post.post("/posts/")
def create_post(post: Post):
    try:
        author_obj_id = ObjectId(post.author_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid author_id format")

    user = users_collection.find_one({"_id": author_obj_id})
    if not user:
        raise HTTPException(status_code=404, detail="Author (user) not found")

    post_data = post.model_dump()
    post_data["author_id"] = author_obj_id  # store as actual ObjectId in MongoDB

    result = post_collection.insert_one(post_data)
    return {"id": str(result.inserted_id), "message": "Post created"}