from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import uuid

class PlayerColor(str, Enum):
    WHITE = "white"
    BLACK = "black"

class PlayerStatus(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"

class UserBase(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserDB(UserBase):
    password_hash: str

class UserInGame(UserBase):
    color: PlayerColor
    captured_figures: List[str] = []
    move_history: List[str] = []

class UserLobby(UserBase):
    color: Optional[PlayerColor] = None
    status: PlayerStatus = Field(default=PlayerStatus.NOT_READY)

class UserResponse(UserBase):
    pass
