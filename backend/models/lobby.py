from pydantic import BaseModel
from models.user import UserLobby
from typing import List

class Lobby(BaseModel):
    game_id: str
    players: List[UserLobby]