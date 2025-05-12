from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/Socium")

# Access a database
db = client["socium"]

# You can define collections for reuse
users_collection = db["users"]
post_collection = db["posts"]
auth_collection = db["auth"]
comment_collection =db["comments"]
likes_collection=db["likes"]



