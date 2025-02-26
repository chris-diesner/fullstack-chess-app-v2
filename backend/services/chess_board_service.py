from models.chess_board import ChessBoard
from models.figure import Figure
from typing import Optional

class ChessBoardService:
    """Service für das direkte Manipulieren des Schachbretts."""

    def __init__(self, board: Optional[ChessBoard] = None):
        self.board = board if board else ChessBoard()  # Neues Brett oder vorhandenes nutzen

    def move_figure(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> None:
        """Bewegt eine Figur auf dem Brett."""
        figure = self.board.squares[start_pos[0]][start_pos[1]]
        if figure is None:
            raise ValueError("Kein Stein auf Startposition!")

        # Figur bewegen
        self.board.squares[end_pos[0]][end_pos[1]] = figure
        self.board.squares[start_pos[0]][start_pos[1]] = None
        figure.position = end_pos

    def get_king_position(self, color) -> Optional[tuple[int, int]]:
        """Findet die Position des Königs einer bestimmten Farbe."""
        for row in range(8):
            for col in range(8):
                figure = self.board.squares[row][col]
                if isinstance(figure, Figure) and figure.name == "king" and figure.color == color:
                    return (row, col)
        return None  # Sollte nicht passieren, wenn das Spiel korrekt läuft

    def initialize_board(self) -> None:
        """Setzt das Brett auf die Standard-Schachposition zurück."""
        self.board = ChessBoard()
