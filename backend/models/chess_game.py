from enum import Enum
from pydantic import BaseModel
from models.chess_board import ChessBoard
from models.user import UserInGame
from datetime import datetime
from typing import Optional

class GameStatus(str, Enum):
    RUNNING = "running"
    ENDED = "ended"
    ABORTED = "aborted"

class ChessGame(BaseModel):
    
    game_id: str
    time_stamp_start: datetime
    player_white: UserInGame
    player_black: UserInGame
    current_turn: str
    board: ChessBoard
    status: GameStatus = GameStatus.RUNNING
    last_move: Optional[dict] = None
