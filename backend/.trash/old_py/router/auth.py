from fastapi import APIRouter, HTTPException, Depends
from backend.database.mongodb import users_collection
from user import User, UserCreate, UserResponse
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError
from dotenv import load_dotenv
import jwt
import os
import re

auth_router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
token_blacklist = set()

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in token_blacklist:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": True, "verify_exp": True},
        )
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")  

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_data = users_collection.find_one({"username": username})

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(**user_data)

@auth_router.post("/register")
def register(user: UserCreate):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    if not re.search(r"[A-Z]", user.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    
    if not re.search(r"[0-9]", user.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")
    
    new_user = User(username=user.username, password=user.password)
    users_collection.insert_one(vars(new_user))
    return {"message": "User registered successfully"}

@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=422, detail="Username is required")
    
    if not form_data.password:
        raise HTTPException(status_code=422, detail="Password is required")

    user_data = users_collection.find_one({"username": form_data.username})

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user = User(username=user_data["username"], password_hash=user_data["password_hash"], id=user_data["id"])

    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user

from datetime import datetime, timedelta, timezone  # ✅ timezone importieren

@auth_router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")

        if not exp or datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token already expired")

        token_blacklist.add(token)
        return {"message": "Logout successful"}

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token already expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")