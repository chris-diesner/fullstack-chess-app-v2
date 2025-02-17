from fastapi import APIRouter, HTTPException
from chess_board import ChessBoard
from chess_game import ChessGame
from chess_exception import ChessException

game = ChessGame()
board = ChessBoard()

game_router = APIRouter()

games = {}

@game_router.post("/new")
def create_game():
    game = ChessGame()
    game.board.setup_board()
    games[game.game_id] = game
    return {"message": "Game created", "game_id": game.game_id}

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
