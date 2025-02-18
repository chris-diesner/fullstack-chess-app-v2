from fastapi import APIRouter, HTTPException
from chess_board import ChessBoard
from chess_game import ChessGame
from chess_exception import ChessException
import uuid

game = ChessGame(white_name="white", black_name="black")
board = ChessBoard()
game_router = APIRouter()
game_lobbies = {}
games = {}

@game_router.post("/lobby/create")
def create_lobby(username: str):
    if username in game_lobbies:
        raise HTTPException(status_code=400, detail="Du bist bereits in einer Lobby")
    
    game_id = str(uuid.uuid4())
    
    game_lobbies[game_id] = {
        "players": {username: None},
        "ready_status": {username: False}
    }
    
    return {"message": "Lobby erstellt", "game_id": game_id}

@game_router.post("/lobby/{game_id}/join")
def join_lobby(game_id: str, username: str):
    if game_id not in game_lobbies:
        raise HTTPException(status_code=404, detail="Lobby nicht gefunden")
        
    if len(game_lobbies[game_id]["players"]) >= 2:
        raise HTTPException(status_code=400, detail="Lobby ist bereits voll")
    
    game_lobbies[game_id]["players"][username] = None
    game_lobbies[game_id]["ready_status"][username] = False
    
    return {"message": f"{username} ist der Lobby beigetreten", "game_id": game_id}

@game_router.post("/lobby/{game_id}/set_color_and_ready")
def set_color_and_ready(game_id: str, username: str, color: str, ready_status: bool):
    if game_id not in game_lobbies:
        raise HTTPException(status_code=404, detail="Lobby nicht gefunden")
    
    if color not in ["white", "black"]:
        raise HTTPException(status_code=400, detail="ungültige Farbe")
        
    if username not in game_lobbies[game_id]["players"]: 
        raise HTTPException(status_code=400, detail="Du bist nicht in dieser Lobby")
    
    if color in game_lobbies[game_id]["players"].values() and game_lobbies[game_id]["players"][username] != color:
        raise HTTPException(status_code=400, detail="Farbe ist bereits vergeben")
    
    game_lobbies[game_id]["players"][username] = color
    game_lobbies[game_id]["ready_status"][username] = ready_status
    
    return {"message": f"{username} hat {color} gewählt und ist bereit", "game_id": game_id}
    
@game_router.post("/new")
def create_game(game_id:str):
    if game_id not in game_lobbies:
        raise HTTPException(status_code=404, detail="Lobby nicht gefunden")
    
    if len(game_lobbies[game_id]["players"]) != 2:
        raise HTTPException(status_code=400, detail="Nicht genug Spieler")
    
    if None in game_lobbies[game_id]["players"].values():
        raise HTTPException(status_code=400, detail="Nicht alle Spieler haben eine Farbe gewählt")
    
    if not all(game_lobbies[game_id]["ready_status"].values()): 
        raise HTTPException(status_code=400, detail="Nicht alle Spieler sind bereit")
    
    white_player, black_player = None, None
    for user, color in game_lobbies[game_id]["players"].items():
        if color == "white":
            white_player = user
        else:
            black_player = user
            
    game = ChessGame(white_name=white_player, black_name=black_player)
    game.board.setup_board()
    games[game.game_id] = game
    
    del game_lobbies[game_id]
    
    return {"message": "Spiel erfolgreich gestartet", "game_id": game.game_id}

@game_router.get("/{game_id}/board")
def get_board_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.get_game_state()

@game_router.post("/{game_id}/move")
def move_figure(game_id: str, start_pos: str, end_pos: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    start_row, start_col = game.board.notation_to_index(start_pos)
    end_row, end_col = game.board.notation_to_index(end_pos)
    try:
        move_result = game.move_figure((start_row, start_col), (end_row, end_col))
        return {"message": move_result, "game_state": game.get_game_state()}
    except ChessException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@game_router.get("/{game_id}/history")
def get_move_history(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    history = {
        "white_moves": game.white_player.move_history,
        "black_moves": game.black_player.move_history
    }
    return history
