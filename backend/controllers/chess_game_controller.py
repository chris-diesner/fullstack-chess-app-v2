from fastapi import APIRouter, HTTPException
from services.chess_game_service import ChessGameService

game_router = APIRouter()
game_service = ChessGameService()

@game_router.post("/game/move/{game_id}/{user_id}/{move}")
def move(game_id: str, user_id: str, move: str):
    try:
        return game_service.move_figure(game_id, user_id, move)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))