from database.mongodb import users_collection
from models.user import UserDB
from pymongo import ReturnDocument


class UserRepository:
    def insert_user(self, user: UserDB):
        user_dict = user.model_dump(by_alias=True)
        user_dict["_id"] = user_dict.pop("user_id")
        users_collection.insert_one(user_dict)

    def find_user_by_username(self, username: str) -> UserDB | None:
        user_data = users_collection.find_one({"username": username})
        if user_data:
            user_data["user_id"] = user_data.pop("_id")
            return UserDB(**user_data)
        return None
    
    def find_user_by_id(self, user_id: str) -> UserDB | None:
        user_data = users_collection.find_one({"_id": user_id})
        if user_data:
            user_data["user_id"] = user_data.pop("_id")
            return UserDB(**user_data)
        return None

    def update_user(self, user_id: str, update_data: dict) -> UserDB | None:
        if not update_data:
            return None

        updated_user = users_collection.find_one_and_update(
            {"_id": user_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if updated_user:
            updated_user["user_id"] = str(updated_user.pop("_id"))
            return UserDB(**updated_user)
        
        return None

    def delete_user(self, user_id: str) -> bool:
        result = users_collection.delete_one({"_id": user_id})
        return result.deleted_count > 0