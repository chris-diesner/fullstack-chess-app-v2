from fastapi import APIRouter, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from services.chess_lobby_service import ChessLobbyService
from models.user import UserLobby
from models.lobby import Lobby

lobby_router = APIRouter()
lobby_service = ChessLobbyService()

@lobby_router.websocket("/ws/{game_id}")
async def websocket_lobby(websocket: WebSocket, game_id: str):
    await websocket.accept()
    await lobby_service.connect(websocket, game_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "refresh":
                await lobby_service.broadcast(game_id, {"message": "refresh_lobby"})
    except WebSocketDisconnect:
        lobby_service.disconnect(websocket, game_id)

@lobby_router.post("/create", response_model=Lobby)
async def create_lobby(user: UserLobby):
    try:
        return lobby_service.create_lobby(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@lobby_router.get("/list")
async def list_lobbies():
    try:
        return lobby_service.list_lobbies()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/join/{game_id}", response_model=Lobby)
async def join_lobby(game_id: str, user: UserLobby):
    try:
        return await lobby_service.join_lobby(game_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@lobby_router.post("/leave/{game_id}/{user_id}", response_model=Lobby | None)
async def leave_lobby(game_id: str, user_id: str):
    try:
        return await lobby_service.leave_lobby(game_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/set_color/{game_id}/{user_id}/{color}", response_model=Lobby)
async def set_player_color(game_id: str, user_id: str, color: str):
    try:
        return await lobby_service.set_player_color(game_id, user_id, color)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@lobby_router.post("/set_status/{game_id}/{user_id}/{status}", response_model=Lobby)
async def set_player_status(game_id: str, user_id: str, status: str):
    try:
        return await lobby_service.set_player_status(game_id, user_id, status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
