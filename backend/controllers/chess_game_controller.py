from fastapi import APIRouter, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from services.chess_game_service import ChessGameService
from models.chess_game import ChessGame

game_router = APIRouter()
game_service = ChessGameService()

@game_router.websocket("/ws/{game_id}")
async def websocket_game(websocket: WebSocket, game_id: str):
    await websocket.accept()
    await game_service.connect(websocket, game_id)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "move":
                game_id_from_message = data.get("game_id")
                start_pos = data.get("start_pos")
                end_pos = data.get("end_pos")
                user_id = data.get("user_id")

                if game_id_from_message != game_id:
                    await websocket.send_json({"type": "error", "message": "Ungültige game_id!"})
                    return

                try:
                    game = game_service.move_figure(tuple(start_pos), tuple(end_pos), game_id, user_id)
                    await game_service.broadcast(game_id, {"type": "game_state", "data": game.model_dump()})
                except ValueError as e:
                    await websocket.send_json({"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        game_service.disconnect(websocket, game_id)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": f"Fehler: {str(e)}"})

    
@game_router.post("/start_game/{game_id}/{user_id}", response_model=ChessGame)
async def start_game(game_id: str, user_id: str):
    
    try:
        print(f"🟢 Spielstart angefordert für game_id={game_id}, user_id={user_id}")
        return await game_service.start_game(game_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# fallback route for debbuging 
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
