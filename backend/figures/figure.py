import uuid
from abc import ABC, abstractmethod

class Figure(ABC):
    def __init__(self, color, position, name):
        self.color = color
        self.position = position
        self.name = name
        self.id = str(uuid.uuid4())
        self.move_history = []
        
    @abstractmethod
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        pass
        
    def within_board(self, pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

class Bishop(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "bishop")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        #Regel: Zuege nur innerhalb Spielfeld
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        
        #Regel: Laeufer bewegt sich nur diagonal
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        #Regel: Laeufer darf keine Figuren ueberspringen
        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1
        row, col = start_row + step_row, start_col + step_col
        while row != end_row:
            if board[row][col] is not None:
                return False
            row += step_row
            col += step_col
        
        #Regel: Zielfeld leer oder Gegner
        target_field = board[end_row][end_col]
        if target_field is None or target_field.color != self.color:
            return True
        
        return False

class Rook(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "rook")
        self.has_moved = False
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        #Regel: Zuege nur innerhalb Spielfeld
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        
        #Regel: rook bewegt sich nur horizontal oder vertikal
        if start_row != end_row and start_col != end_col:
            return False
        
        #Regel: rook darf keine Figuren ueberspringen
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range (start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
                
        elif start_col == end_col:
            step = 1 if end_row > start_row else -1
            for row in range (start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False
        
        #Regel: Zielfeld leer oder Gegner
        target_field = board[end_row][end_col]
        if target_field is None or target_field.color != self.color:
            return True
        
        return False
    

class Queen(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "queen")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        #Regel: Zuege nur innerhalb Spielfeld
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        #Regel: queen bewegt sich horizontal, vertikal oder diagonal
        if start_row == end_row:
            step_row, step_col = 0, 1 if end_col > start_col else -1
        elif start_col == end_col:
            step_row, step_col = 1 if end_row > start_row else -1, 0
        elif abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
        else:
            return False 

        #Regel: queen darf keine Figuren überspringen
        row, col = start_row + step_row, start_col + step_col
        while (row, col) != (end_row, end_col):
            if board[row][col] is not None:
                return False
            row += step_row
            col += step_col

        #Regel: Zielfeld leer oder Gegner
        target_field = board[end_row][end_col]
        if target_field is None or target_field.color != self.color:
            return True

        return False

class Pawn(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "pawn")
        
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if self.color == "white":
            #Regel: ein Feld nach vorne
            if end_row == start_row - 1 and start_col == end_col and board[end_row][end_col] is None:
                return True

            #Regel: zwei Felder nach vorne
            if start_row == 6 and end_row == start_row - 2 and start_col == end_col:
                if board[start_row - 1][start_col] is None and board[end_row][end_col] is None:
                    return True

            
            if end_row == start_row - 1 and abs(end_col - start_col) == 1:
                #Diagonaler Zug
                if board[end_row][end_col] is not None and board[end_row][end_col].color != self.color:
                    return True

                #En passant
                if last_move and isinstance(last_move["figure"], Pawn):
                    if (
                        last_move["start_pos"][0] == last_move["end_pos"][0] - 2 and  
                        last_move["end_pos"] == (start_row, end_col)
                    ):
                        return True

        if self.color == "black":
            #Regel: ein Feld nach vorne
            if end_row == start_row + 1 and start_col == end_col and board[end_row][end_col] is None:
                return True
            
            #Regel: zwei Felder nach vorne
            if start_row == 1 and end_row == start_row + 2 and start_col == end_col:
                if board[start_row + 1][start_col] is None and board[end_row][end_col] is None:
                    return True

            if end_row == start_row + 1 and abs(end_col - start_col) == 1:
                #Diagonaler Zug
                if board[end_row][end_col] is not None and board[end_row][end_col].color != self.color:
                    return True

                #En passant
                if last_move and isinstance(last_move["figure"], Pawn):
                    if (
                        last_move["start_pos"][0] == last_move["end_pos"][0] + 2 and  
                        last_move["end_pos"] == (start_row, end_col)
                    ):
                        return True

        return False


class King(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "king")
        self.has_moved = False
        
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        #Regel: Koenig bewegt sich genau ein Feld in jede Richtung
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff <= 1 and col_diff <= 1:
            target_field = board[end_row][end_col]
            return target_field is None or target_field.color != self.color

        return False

class Knight(Figure):
    
    def __init__(self, color, position):
        super().__init__(color, position, "knight")
        
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        #Regel: knight bewegt sich in einem "L"-Muster
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            target_field = board[end_row][end_col]
            return target_field is None or target_field.color != self.color

        return False