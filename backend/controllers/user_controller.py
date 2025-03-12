from fastapi import APIRouter, HTTPException, Depends, Header, Request
from services.user_service import UserService
from services.auth_service import AuthService
from models.user import UserCreate, UserResponse

user_router = APIRouter()
user_service = UserService()
auth_service = AuthService()

@user_router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    new_user = user_service.create_user(user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Username existiert bereits")
    return new_user

def get_current_user_token(authorization: str = Header(None)) -> str | None:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        return auth_service.get_current_user(token)
    return None

@user_router.get("/me", response_model=UserResponse)
def get_current_user(username: str = Depends(get_current_user_token)):    
    if not username:
        raise HTTPException(status_code=401, detail="Nicht authentifiziert")

    user = user_service.get_user_by_username(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")

    return user

@user_router.put("/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    hashed_password = AuthService.hash_password(password) if password else None
    updated_user = user_service.update_user(user_id, username=username, password=hashed_password)

    if not updated_user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return updated_user

@user_router.delete("/delete/{user_id}")
def delete_user(user_id: str):
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return {"message": "Benutzer erfolgreich gelöscht"}
