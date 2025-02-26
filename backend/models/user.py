from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import uuid

class PlayerColor(Enum):
    WHITE = "white"
    BLACK = "black"
    
class PlayerStatus(Enum):
    READY = "ready"
    NOT_READY = "not_ready"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    
class UserLobby(BaseModel):
    user_id: str
    username: str
    color: Optional[PlayerColor] = None
    status: PlayerStatus = Field(default=PlayerStatus.NOT_READY)
    
class UserResponse(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    captured_figures: List[str] = []
    move_history: List[str] = []

    class Config:
        populate_by_name = True
