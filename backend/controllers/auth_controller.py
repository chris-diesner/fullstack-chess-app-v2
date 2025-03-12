from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter()
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Username oder Passwort falsch")
    
    access_token = auth_service.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    success = auth_service.logout(token)

    if not success:
        raise HTTPException(status_code=401, detail="Token ungültig oder bereits abgelaufen")

    return {"message": "Logout erfolgreich"}

@auth_router.get("/check-token")
def check_token(token: str = Depends(oauth2_scheme)):
    if not auth_service.is_token_valid(token):
        raise HTTPException(status_code=401, detail="Token abgelaufen oder ungültig")
    
    return {"message": "Token ist gültig"}
