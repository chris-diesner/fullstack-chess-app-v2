from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from chess_board import ChessBoard

app = FastAPI()
board = ChessBoard()

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
    return {"board": board.get_board_state()}

app.include_router(game_router, prefix="/game", tags=["Game"])

@app.get("/")
def home():
    return {"message": "Welcome to the Fullstack Chess API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
