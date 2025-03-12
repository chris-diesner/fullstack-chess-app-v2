from models.chess_board import ChessBoard
from models.figure import Figure, FigureColor, Pawn, Rook, Knight, Bishop, Queen, King
from typing import List, Optional

class ChessBoardService:
    def __init__(self, board: Optional[ChessBoard] = None):
        self.board = board if board else ChessBoard.create_empty_board()


    def initialize_board(self) -> ChessBoard:
        self.board = ChessBoard(squares=self.create_start_position())
        return self.board

    @staticmethod
    def create_start_position() -> List[List[Optional[Figure]]]:
        board = ChessBoard.create_empty_board().squares

        board[0] = [
            Rook(color=FigureColor.BLACK, position=(0, 0)),
            Knight(color=FigureColor.BLACK, position=(0, 1)),
            Bishop(color=FigureColor.BLACK, position=(0, 2)),
            Queen(color=FigureColor.BLACK, position=(0, 3)),
            King(color=FigureColor.BLACK, position=(0, 4)),
            Bishop(color=FigureColor.BLACK, position=(0, 5)),
            Knight(color=FigureColor.BLACK, position=(0, 6)),
            Rook(color=FigureColor.BLACK, position=(0, 7)),
        ]
        board[1] = [Pawn(color=FigureColor.BLACK, position=(1, i)) for i in range(8)]

        board[6] = [Pawn(color=FigureColor.WHITE, position=(6, i)) for i in range(8)]
        board[7] = [
            Rook(color=FigureColor.WHITE, position=(7, 0)),
            Knight(color=FigureColor.WHITE, position=(7, 1)),
            Bishop(color=FigureColor.WHITE, position=(7, 2)),
            Queen(color=FigureColor.WHITE, position=(7, 3)),
            King(color=FigureColor.WHITE, position=(7, 4)),
            Bishop(color=FigureColor.WHITE, position=(7, 5)),
            Knight(color=FigureColor.WHITE, position=(7, 6)),
            Rook(color=FigureColor.WHITE, position=(7, 7)),
        ]
        return board
