import uuid
from pydantic import BaseModel
from models.user import UserLobby
from typing import List
from typing import Dict, Optional

class Lobby(BaseModel):
    game_id: str
    players: List[UserLobby]