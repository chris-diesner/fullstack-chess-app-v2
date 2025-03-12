from pydantic import BaseModel
from typing import Optional, List
from models.figure import Figure

class ChessBoard(BaseModel):
    
    squares: List[List[Optional[Figure]]]

    @classmethod
    def create_empty_board(cls):
        return cls(squares=[[None for _ in range(8)] for _ in range(8)])
