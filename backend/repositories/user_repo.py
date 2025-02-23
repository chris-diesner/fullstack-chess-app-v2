from database.mongodb import users_collection
from models.user import UserResponse
from pymongo import ReturnDocument


class UserRepository:
    def insert_user(self, user: UserResponse):
        user_dict = user.model_dump(by_alias=True)
        user_dict["_id"] = user_dict.pop("id")
        users_collection.insert_one(user_dict)

    def find_user_by_username(self, username: str):
        user_data = users_collection.find_one({"username": username})
        if user_data:
            user_data["id"] = user_data.pop("_id")
            user_data["username"] = username
            return user_data
        return None
    
    def find_user_by_id(self, id: str):
        user_data = users_collection.find_one({"_id": id})
        if user_data:
            user_data["id"] = user_data.pop("_id")
            return user_data
        return None

    def update_user(self, id: str, update_data: dict) -> UserResponse | None:
        if not update_data:
            return None

        updated_user = users_collection.find_one_and_update(
            {"_id": id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if updated_user:
            updated_user["id"] = str(updated_user.pop("_id"))
            return UserResponse(**updated_user)
        
        return None

    def delete_user(self, id: str) -> bool:
        result = users_collection.delete_one({"_id": id})
        return result.deleted_count > 0