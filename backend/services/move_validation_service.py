from models.figure import Figure, FigureColor, Pawn, Rook, Knight, Bishop, Queen, King
from models.chess_board import ChessBoard

class MoveValidationService:

    @staticmethod
    def is_move_valid(figure: Figure, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:

        if not MoveValidationService.is_within_board(end_pos):
            return False

        target_figure = board.squares[end_pos[0]][end_pos[1]]

        if target_figure and target_figure.color == figure.color:
            return False  

        if isinstance(figure, Pawn):
            return MoveValidationService.is_move_valid_pawn(figure, start_pos, end_pos, board)
        if isinstance(figure, Rook):
            return MoveValidationService.is_valid_move_rook(figure, start_pos, end_pos, board)
        if isinstance(figure, Bishop):
            return MoveValidationService.is_valid_move_bishop(figure, start_pos, end_pos, board)
        if isinstance(figure, Queen):
            return MoveValidationService.is_valid_move_queen(figure, start_pos, end_pos, board)
        if isinstance(figure, Knight):
            return MoveValidationService.is_valid_move_knight(figure, start_pos, end_pos)
        if isinstance(figure, King):
            return MoveValidationService.is_valid_move_king(figure, start_pos, end_pos, board)

        return False
    
    @staticmethod
    def is_within_board(pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8
    
    @staticmethod
    def is_move_valid_pawn(figure: Pawn, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        direction = -1 if figure.color == FigureColor.WHITE else 1
        
        if end_row == start_row + direction and start_col == end_col and not board.squares[end_row][end_col]:
            return True
        
        if start_row == (6 if figure.color == FigureColor.WHITE else 1) and end_row == start_row + 2 * direction and start_col == end_col:
            if not board.squares[start_row + direction][start_col] and not board.squares[end_row][end_col]:
                return True

        if end_row == start_row + direction and abs(end_col - start_col) == 1:
            if board.squares[end_row][end_col] and board.squares[end_row][end_col].color != figure.color:
                return True
            
        return False

    @staticmethod
    def is_valid_move_rook(figure: Rook, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board.squares[start_row][col]:
                    return False
            return True

        if start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board.squares[row][start_col]:
                    return False
            return True
        
        return False

    @staticmethod
    def is_valid_move_bishop(figure: Bishop, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1
        row, col = start_row + step_row, start_col + step_col
        while row != end_row:
            if board.squares[row][col] is not None:
                return False
            row += step_row
            col += step_col

        return True

    @staticmethod
    def is_valid_move_queen(figure: Queen, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:
        return (
            MoveValidationService.is_valid_move_rook(figure, start_pos, end_pos, board) or 
            MoveValidationService.is_valid_move_bishop(figure, start_pos, end_pos, board)
        )

    @staticmethod
    def is_valid_move_knight(figure: Knight, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> bool:
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    @staticmethod
    def is_valid_move_king(figure: King, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard) -> bool:
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        if row_diff <= 1 and col_diff <= 1:
            return True

        return False

