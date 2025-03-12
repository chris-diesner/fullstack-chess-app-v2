from fastapi import APIRouter, HTTPException
from services.chess_game_service import ChessGameService

game_router = APIRouter()
game_service = ChessGameService()

@game_router.post("/move/{game_id}/{user_id}")
def move(game_id: str, user_id: str, move_data: dict):
    try:
        start_pos = move_data.get("start_pos")
        end_pos = move_data.get("end_pos")

        if not start_pos or not end_pos:
            raise HTTPException(status_code=400, detail="Ungültige Eingabe! Start- und Endposition müssen angegeben werden.")

        return game_service.move_figure(tuple(start_pos), tuple(end_pos), game_id, user_id)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
