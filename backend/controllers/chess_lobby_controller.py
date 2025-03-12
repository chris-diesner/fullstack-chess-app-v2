from fastapi import APIRouter, HTTPException
from services.chess_lobby_service import ChessLobbyService
from models.user import UserLobby
from models.lobby import Lobby
from models.chess_game import ChessGame

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

@lobby_router.post("/leave/{game_id}/{user_id}", response_model=Lobby | None)
def leave_lobby(game_id: str, user_id: str):
    try:
        return lobby_service.leave_lobby(game_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/set_color/{game_id}/{user_id}/{color}", response_model=Lobby)
def set_player_color(game_id: str, user_id: str, color: str):
    try:
        return lobby_service.set_player_color(game_id, user_id, color)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/set_status/{game_id}/{user_id}/{status}", response_model=Lobby)
def set_player_status(game_id: str, user_id: str, status: str):
    try:
        return lobby_service.set_player_status(game_id, user_id, status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/start_game/{game_id}/{user_id}", response_model=ChessGame)
def start_game(game_id: str, user_id: str):
    try:
        return lobby_service.start_game(game_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))