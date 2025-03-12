from datetime import datetime, timedelta
from dotenv import load_dotenv
from passlib.context import CryptContext
from models.user import UserResponse
from repositories.user_repo import UserRepository
from jwt.exceptions import ExpiredSignatureError
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 90))
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

token_blacklist = set()

class AuthService:
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo or UserRepository()
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_current_user(token: str) -> str | None:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"verify_signature": True, "verify_exp": True},
            )
            return payload.get("sub")
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
    
    def authenticate_user(self, username: str, password: str) -> UserResponse | None:
        user_data = self.user_repo.find_user_by_username(username)
        if not user_data:
            return None
        if not self.verify_password(password, user_data.password_hash):
            return None

        return UserResponse(user_id=user_data.user_id, username=user_data.username)

    @staticmethod
    def logout(token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            exp = payload.get("exp")
            if not exp or datetime.fromtimestamp(exp) < datetime.now():
                return False

            token_blacklist.add(token)
            return True

        except ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        
    def is_token_valid(self, token: str) -> bool:
        if token in token_blacklist:
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            if not exp or datetime.fromtimestamp(exp) < datetime.now():
                return False
            return True
        except (ExpiredSignatureError, jwt.InvalidTokenError):
            return False

    @staticmethod
    def is_token_revoked(token: str) -> bool:
        return token in token_blacklist