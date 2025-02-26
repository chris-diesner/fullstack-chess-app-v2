from fastapi import APIRouter, HTTPException
from services.chess_lobby_service import ChessLobbyService
from models.user import UserLobby
from models.lobby import Lobby

lobby_router = APIRouter()
lobby_service = ChessLobbyService()

@lobby_router.post("/create", response_model=Lobby)
def create_lobby(user: UserLobby):
    try:
        return lobby_service.create_lobby(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@lobby_router.get("/list")
def list_lobbies():
    try:
        return lobby_service.list_lobbies()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/join/{game_id}", response_model=Lobby)
def join_lobby(game_id: str, user: UserLobby):
    try:
        return lobby_service.join_lobby(game_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    