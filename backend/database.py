from pymongo import MongoClient
from dotenv import load_dotenv
from user import User
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chess_game"]
users_collection = db["users"]

def insert_user(user: User):
    user_dict = user.model_dump(by_alias=True)
    users_collection.insert_one(user_dict)
    
def find_user(username: str):
    return users_collection.find_one({"username": username})