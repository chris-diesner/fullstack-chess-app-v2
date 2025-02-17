from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://cdiesner12:***@cluster2025.fq8uc.mongodb.net/")
client = MongoClient(MONGO_URI)
db = client["chess_game"]
users_collection = db["users"]
