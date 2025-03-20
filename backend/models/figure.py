import uuid
from pydantic import BaseModel, Field
from enum import Enum

class FigureColor(str, Enum):
    WHITE = "white"
    BLACK = "black"

class Figure(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    color: FigureColor
    position: tuple[int, int]
    
    @property
    def image_path(self) -> str:
        return f"/assets/{self.color}_{self.name}.png"

class Pawn(Figure):
    name: str = "pawn"

class Rook(Figure):
    name: str = "rook"
    has_moved: bool = False

class Knight(Figure):
    name: str = "knight"

class Bishop(Figure):
    name: str = "bishop"

class Queen(Figure):
    name: str = "queen"

class King(Figure):
    name: str = "king"
    has_moved: bool = False
