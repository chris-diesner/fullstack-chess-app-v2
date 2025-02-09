from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chess_board import ChessBoard
from chess_game import ChessGame

app = FastAPI()
app.state.game = ChessGame()
game = ChessGame()
board = ChessBoard()

game_router = APIRouter()

games = {}

# CORS-Unterstützung für das Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für die Entwicklung offen, später einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router, prefix="/game", tags=["Game"])

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
    game.move_figure((start_row, start_col), (end_row, end_col))
    return game.get_game_state()

@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
