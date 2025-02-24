import uuid
from pydantic import BaseModel
from enum import Enum

class FigureColor(Enum):
    WHITE = "white"
    BLACK = "black"

class Figure(BaseModel):
    
    id: str = str(uuid.uuid4())
    name: str
    color: FigureColor
    position: tuple[int, int]

class Pawn(Figure):
    name: str = "pawn"

class Rook(Figure):
    name: str = "rook"

class Knight(Figure):
    name: str = "knight"

class Bishop(Figure):
    name: str = "bishop"

class Queen(Figure):
    name: str = "queen"

class King(Figure):
    name: str = "king"
    has_moved: bool = False
