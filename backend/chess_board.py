from typing import List, Optional
from figures.figure import Figure, Bishop, Rook, Queen, Pawn, King, Knight

class ChessBoard:
    def __init__(self):
        self.squares: List[List[Optional[Figure]]] = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        
    def notation_to_index(self, notation):
        columns = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        row = 8 - int(notation[1])  
        col = columns[notation[0].upper()]
        return row, col
        
    def setup_board(self):
        for col in range(8):
            self.squares[6][col] = Pawn("white", (6, col))
            self.squares[1][col] = Pawn("black", (1, col))
            
        figures = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.squares[7][col] = figures[col]("white", (7, col))
            self.squares[0][col] = figures[col]("black", (0, col))
            
    def get_board_state(self):
        board_state = []
        for row in range(8):
            board_row = []
            for col in range(8):
                figure = self.squares[row][col]
                if figure:
                    board_row.append({
                        "type": figure.name,
                        "color": figure.color,
                        "position": f"{chr(97 + col)}{8 - row}"  
                    })
                else:
                    board_row.append(None)
            board_state.append(board_row)
        return board_state