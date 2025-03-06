from models.user import UserCreate, UserResponse
from repositories.user_repo import UserRepository
from services.auth_service import AuthService
import uuid

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user_data: UserCreate) -> UserResponse | None:
        existing_user = self.get_user_by_username(user_data.username)
        if existing_user:
            return None
        hashed_password = AuthService.hash_password(user_data.password)
        new_user = UserResponse(
            id=str(uuid.uuid4()),
            username=user_data.username
        )
        self.user_repo.insert_user(new_user)
        return new_user

    def get_user_by_username(self, username: str) -> UserResponse:
        user_data = self.user_repo.find_user_by_username(username)
        if user_data:
            return UserResponse(**user_data) 
        return None
    
    def get_user_by_id(self, id: str) -> UserResponse:
        user_data = self.user_repo.find_user_by_id(id)
        if user_data:
            return UserResponse(**user_data)
        return None
    
    def update_user(self, user_id: str, username: str = None, password: str = None) -> UserResponse | None:
        update_data = {}

        if username:
            update_data["username"] = username

        if password:
            update_data["password_hash"] = AuthService.hash_password(password)

        updated_user = self.user_repo.update_user(user_id, update_data)

        if updated_user:
            return UserResponse(**updated_user)
        return None

    def delete_user(self, user_id: str) -> bool:
        return self.user_repo.delete_user(user_id)