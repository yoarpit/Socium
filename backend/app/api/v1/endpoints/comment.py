# routes/comment.py

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime,timezone
from bson import ObjectId
from app.db.session import comment_collection, post_collection
from app.api.v1.endpoints.auth import get_current_user

from app.schemas.comment import CreateComment, CommentOut,UpdateCommentModel

comment_router = APIRouter()

@comment_router.post("/comments", response_model=CommentOut)
def create_comment(data: CreateComment, current_user: dict = Depends(get_current_user)):
    if not post_collection.find_one({"_id": ObjectId(data.post_id)}):
        raise HTTPException(status_code=404, detail="Post not found")

    comment = {
        "post_id": data.post_id,
        "author": current_user["username"],
        "content": data.content,
        "created_at": datetime.now(timezone.utc)
    }

    result = comment_collection.insert_one(comment)
    comment["_id"] = str(result.inserted_id)
    return {
        "id": comment["_id"],
        **data.model_dump(),
        "author": comment["author"],
        "created_at": comment["created_at"]
    }

@comment_router.get("/comments/{post_id}", response_model=list[CommentOut])
def get_comments(post_id: str):
    comments = comment_collection.find({"post_id": post_id})
    return [
        {
            "id": str(comment["_id"]),
            "post_id": comment["post_id"],
            "author": comment["author"],
            "content": comment["content"],
            "created_at": comment["created_at"]
        }
        for comment in comments
    ]




@comment_router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: str, data: UpdateCommentModel, current_user: dict = Depends(get_current_user)):
    comment = comment_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    comment_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": {"content": data.content}})
    comment["content"] = data.content
    return {
        "id": str(comment["_id"]),
        "post_id": comment["post_id"],
        "author": comment["author"],
        "content": comment["content"],
        "created_at": comment["created_at"]
    }


@comment_router.delete("/comments/{comment_id}")
def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    comment = comment_collection.find_one({"_id": ObjectId(comment_id)})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment["author"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    comment_collection.delete_one({"_id": ObjectId(comment_id)})
    return {"message": "Comment deleted successfully"}