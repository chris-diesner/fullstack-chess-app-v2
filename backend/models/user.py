from pydantic import BaseModel, Field
from typing import List
import uuid

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    captured_figures: List[str] = []
    move_history: List[str] = []

    class Config:
        populate_by_name = True
