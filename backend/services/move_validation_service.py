from models.figure import Figure, FigureColor, Pawn, Rook, Knight, Bishop, Queen, King
from models.chess_board import ChessBoard
from models.chess_game import ChessGame
from copy import deepcopy

class MoveValidationService:

    @staticmethod
    def is_move_valid(figure: Figure, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard, game: ChessGame) -> bool:
        if not MoveValidationService.is_within_board(end_pos):
            return False

        target_figure = board.squares[end_pos[0]][end_pos[1]]

        if target_figure and target_figure.color == figure.color:
            return False  

        if isinstance(figure, Pawn):
            return MoveValidationService.is_move_valid_pawn(figure, start_pos, end_pos, board, game)
        if isinstance(figure, Rook):
            return MoveValidationService.is_valid_move_rook(figure, start_pos, end_pos, board)
        if isinstance(figure, Bishop):
            return MoveValidationService.is_valid_move_bishop(figure, start_pos, end_pos, board)
        if isinstance(figure, Queen):
            return MoveValidationService.is_valid_move_queen(figure, start_pos, end_pos, board)
        if isinstance(figure, Knight):
            return MoveValidationService.is_valid_move_knight(figure, start_pos, end_pos)
        if isinstance(figure, King):
            if abs(start_pos[1] - end_pos[1]) == 2:
                if not MoveValidationService.is_valid_castling(figure, start_pos, end_pos, board, game):
                    return False
                return True
            return MoveValidationService.is_valid_move_king(figure, start_pos, end_pos, board)

        return False
    
    @staticmethod
    def is_within_board(pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8
    
    @staticmethod
    def is_move_valid_pawn(figure: Pawn, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard, game: ChessGame) -> bool:
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

            if MoveValidationService.is_valid_en_passant(figure, start_pos, end_pos, board, game):
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

    @staticmethod
    def is_king_in_check(game: ChessGame, board: ChessBoard) -> tuple[bool, list]:
        king = None
        for row in range(8):
            for col in range(8):
                figure = board.squares[row][col]
                if isinstance(figure, King) and figure.color == game.current_turn:
                    king = figure
                    king_position = (row, col)
                    break
            if king:
                break

        if not king:
            raise ValueError("Kein König für den aktuellen Spieler gefunden!")

        attacking_figures = []

        for row in range(8):
            for col in range(8):
                attacker = board.squares[row][col]
                if attacker and attacker.color != game.current_turn:
                    if MoveValidationService.is_move_valid(attacker, (row, col), king_position, board, game):
                        attacking_figures.append((attacker, (row, col)))

        return len(attacking_figures) > 0, attacking_figures

    @staticmethod
    def is_king_checkmate(game: ChessGame, board: ChessBoard) -> bool:
        king_in_check, attacking_figures = MoveValidationService.is_king_in_check(game, board)

        if not king_in_check:
            return False

        king_pos = None
        for row in range(8):
            for col in range(8):
                figure = board.squares[row][col]
                if isinstance(figure, King) and figure.color == game.current_turn:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            raise ValueError("Kein König für den aktuellen Spieler gefunden!")

        for end_row in range(max(0, king_pos[0] - 1), min(8, king_pos[0] + 2)):
            for end_col in range(max(0, king_pos[1] - 1), min(8, king_pos[1] + 2)):
                if (end_row, end_col) != king_pos:
                    if MoveValidationService.is_move_valid(figure, king_pos, (end_row, end_col), board, game):
                        if not MoveValidationService.simulate_move_and_check(game, board, king_pos, (end_row, end_col)):
                            return False

        if len(attacking_figures) > 1:
            return True

        attacker_pos = attacking_figures[0][1]
        blocking_positions = MoveValidationService.get_positions_between(king_pos, attacker_pos)

        for row in range(8):
            for col in range(8):
                figure = board.squares[row][col]
                if figure and figure.color == game.current_turn:
                    start_pos = (row, col)

                    if MoveValidationService.is_move_valid(figure, start_pos, attacker_pos, board, game):
                        if not MoveValidationService.simulate_move_and_check(game, board, start_pos, attacker_pos):
                            return False

                    for block_pos in blocking_positions:
                        if MoveValidationService.is_move_valid(figure, start_pos, block_pos, board, game):
                            if not MoveValidationService.simulate_move_and_check(game, board, start_pos, block_pos):
                                return False

        return True

    @staticmethod
    def get_positions_between(start_pos, end_pos):
        positions = []
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                positions.append((start_row, col))
        elif start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                positions.append((row, start_col))
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if start_row < end_row else -1
            col_step = 1 if start_col < end_col else -1
            for i in range(1, abs(start_row - end_row)):
                positions.append((start_row + i * row_step, start_col + i * col_step))
        return positions
    
    @staticmethod
    def simulate_move_and_check(game: ChessGame, board: ChessBoard, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> bool:
        board_copy = deepcopy(board)

        figure = board_copy.squares[start_pos[0]][start_pos[1]]
        board_copy.squares[end_pos[0]][end_pos[1]] = figure
        board_copy.squares[start_pos[0]][start_pos[1]] = None

        return MoveValidationService.is_king_in_check(game, board_copy)[0]

    @staticmethod
    def is_stalemate(game: ChessGame, board: ChessBoard) -> bool:
        king_in_check, _ = MoveValidationService.is_king_in_check(game, board)
        if king_in_check:
            return False

        for row in range(8):
            for col in range(8):
                figure = board.squares[row][col]
                if figure and figure.color == game.current_turn:
                    start_pos = (row, col)
                    for end_row in range(8):
                        for end_col in range(8):
                            end_pos = (end_row, end_col)
                            if MoveValidationService.is_move_valid(figure, start_pos, end_pos, board, game):
                                if not MoveValidationService.simulate_move_and_check(game, board, start_pos, end_pos):
                                    return False

        return True

    @staticmethod
    def is_valid_castling(king: King, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard, game: ChessGame) -> bool:
        if king.has_moved:
            return False

        row, start_col = start_pos
        _, end_col = end_pos

        if end_col == 2:
            rook_col = 0
        elif end_col == 6:
            rook_col = 7
        else:
            return False

        rook = board.squares[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        step = 1 if rook_col > start_col else -1
        for col in range(start_col + step, rook_col, step):
            if board.squares[row][col] is not None:
                return False

        if MoveValidationService.is_king_in_check(game, board)[0]:
            return False

        for col in (start_col + step, start_col + 2 * step):
            if MoveValidationService.simulate_move_and_check(game, board, start_pos, (row, col)):
                return False

        return True

    @staticmethod
    def is_valid_en_passant(figure: Pawn, start_pos: tuple[int, int], end_pos: tuple[int, int], board: ChessBoard, game: ChessGame) -> bool:
        if not game.last_move:
            return False 

        last_move = game.last_move
        last_moved_figure = last_move["figure"]
        last_move_start, last_move_end = last_move["start"], last_move["end"]

        if (
            isinstance(last_moved_figure, Pawn)
            and last_move["two_square_pawn_move"]
            and abs(last_move_start[0] - last_move_end[0]) == 2
            and last_move_end[0] == start_pos[0]
            and last_move_end[1] == end_pos[1]
        ):
            return True

        return False
    