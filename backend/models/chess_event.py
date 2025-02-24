import uuid
from pydantic import BaseModel
from typing import Optional
from models.figure import Figure
from datetime import datetime

class ChessEvent(BaseModel):
    
    event_id: str = str(uuid.uuid4())
    game_id: str
    player_id: str
    figure: Figure
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]
    captured_figure: Optional[Figure] = None
    timestamp: datetime = datetime.now()
