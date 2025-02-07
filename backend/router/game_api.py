from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from chess_board import ChessBoard
from chess_game import ChessGame

app = FastAPI()
game = ChessGame()

game_router = APIRouter()

# CORS-Unterstützung für das Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für die Entwicklung offen, später einschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Router für das Spiel
@game_router.get("/board")
def get_board_state():
    return {"board": game.board.get_board_state()}

app.include_router(game_router, prefix="/game", tags=["Game"])

@game_router.post("/move")
def move_figure(start_pos: str, end_pos: str):
    start_row, start_col = game.board.notation_to_index(start_pos)
    end_row, end_col = game.board.notation_to_index(end_pos)
    game.move_figure((start_row, start_col), (end_row, end_col))
    return {"board": game.board.get_board_state()}

@game_router.post("/reset")
def reset_game():
    global game
    game = ChessGame()
    return {"message": "Game reset"}


@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
