import uuid

class Figure:
    def __init__(self, color, position, name):
        self.color = color
        self.position = position
        self.name = name
        self.id = str(uuid.uuid4())
        self.move_history = []

    def within_board(self, pos):
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def is_path_clear(self, start_pos, end_pos, board):
        """ Check if there are no obstructions in a straight or diagonal path. """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
        step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
        
        row, col = start_row + step_row, start_col + step_col
        while (row, col) != (end_row, end_col):
            if board[row][col] is not None:
                return False
            row += step_row
            col += step_col
        return True

class Bishop(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "bishop")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        if abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class Rook(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "rook")
        self.has_moved = False
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class Queen(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "queen")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1] or abs(start_pos[0] - end_pos[0]) == abs(start_pos[1] - end_pos[1]):
            return self.is_path_clear(start_pos, end_pos, board)
        return False

class Pawn(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "pawn")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if self.color == "white" else 1
        start_rank = 6 if self.color == "white" else 1

        if start_col == end_col and board[end_row][end_col] is None:
            if end_row == start_row + direction:
                return True
            if start_row == start_rank and end_row == start_row + 2 * direction and board[start_row + direction][start_col] is None:
                return True
        
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if board[end_row][end_col] and board[end_row][end_col].color != self.color:
                return True
            if last_move and isinstance(last_move["figure"], Pawn):
                if last_move["start_pos"][0] == last_move["end_pos"][0] - 2 * direction and last_move["end_pos"] == (start_row, end_col):
                    return True
        return False

class King(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "king")
        self.has_moved = False
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return row_diff <= 1 and col_diff <= 1

class Knight(Figure):
    def __init__(self, color, position):
        super().__init__(color, position, "knight")
    
    def is_move_valid(self, start_pos, end_pos, board, last_move=None):
        if not self.within_board(end_pos):
            return False
        
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)