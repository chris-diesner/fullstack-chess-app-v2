from enum import Enum
from pydantic import BaseModel
from models.chess_board import ChessBoard
from models.user import UserResponse
from typing import List

class PlayerColor(Enum):
    WHITE = "white"
    BLACK = "black"

class GameStatus(Enum):
    RUNNING = "running"
    ENDED = "ended"
    ABORTED = "aborted"

class ChessGame(BaseModel):
    
    game_id: str
    player_white: UserResponse
    player_black: UserResponse
    current_turn: PlayerColor = PlayerColor.WHITE
    board: ChessBoard
    move_history: List[str] = []
    status: GameStatus = GameStatus.RUNNING

    def get_current_player(self) -> UserResponse:
        return self.player_white if self.current_turn == PlayerColor.WHITE else self.player_black
