from chess_board import ChessBoard
from chess_exception import ChessException
from figures.figure import Figure, Bishop, Rook, Queen, Pawn, King, Knight
from user import User
import uuid

board = ChessBoard()

class ChessGame:
    def __init__(self, white_name: str, black_name: str):
        self.game_id = str(uuid.uuid4())
        self.board = ChessBoard()
        self.current_player = "white"
        self.last_move = None
        self.white_player = User(white_name)
        self.black_player = User(black_name)

        
    def reset_board(self):
        self.__init__()
        
    def get_game_state(self):
        return {
            "game_id": self.game_id,
            "board": self.board.get_board_state(),
            "current_player": self.current_player,
            "check_mate_status": self.get_check_mate_stalemate_status()
        }
        
    def get_check_mate_stalemate_status(self):
        status = "normal"
        if self.is_king_in_checkmate(self.current_player):
            status = "mate"
        elif self.is_king_in_check(self.current_player)[0]:
            status = "check"
        elif self.check_stalemate():
            status = "stalemate"
        return status

    def get_current_player(self):
        return self.white_player if self.current_player == "white" else self.black_player

    def switch_player(self):
        self.current_player = "black" if self.current_player == "white" else "white"
        if self.check_stalemate():
            raise(ChessException("Unentschieden! Patt!", 200))

    def check_stalemate(self):
        stalemate = self.is_stalemate(self.current_player)
        if stalemate:
            return True
        return False

    def convert_to_coordinates(self, pos):
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        row = 8 - pos[0]
        column = columns[pos[1]]
        return f"{column}{row}"
    
    def get_king_position(self, player_color):
        for row in range(8):
            for col in range(8):
                figure = self.board.squares[row][col]
                if isinstance(figure, King) and figure.color == player_color:
                    return (row, col)
        return None 

    def is_king_in_check(self, current_player):
        king_pos = self.get_king_position(current_player)
        if not king_pos:
            return False, []

        attacking_figures = []

        for row in range(8):
            for col in range(8):
                figure = self.board.squares[row][col]
                if figure and figure.color != current_player:
                    if figure.is_move_valid((row, col), king_pos, self.board.squares):
                        attacking_figures.append((figure, (row, col)))

        return len(attacking_figures) > 0, attacking_figures

    def is_king_in_checkmate(self, current_player):
        king_in_check, attacking_figures = self.is_king_in_check(current_player)
        if not king_in_check:
            return False

        king_pos = self.get_king_position(current_player)
        if not king_pos:
            return False

        king = self.board.squares[king_pos[0]][king_pos[1]]
        legal_moves = []

        for end_row in range(8):
            for end_col in range(8):
                if king and king.is_move_valid(king_pos, (end_row, end_col), self.board.squares):
                    if not self.simulate_move_and_check(current_player, king_pos, (end_row, end_col)):
                        legal_moves.append((end_row, end_col))

        if legal_moves:
            return False

        if len(attacking_figures) == 1:
            attacker_pos = attacking_figures[0][1]
            blocking_positions = self.get_positions_between(king_pos, attacker_pos)

            for row in range(8):
                for col in range(8):
                    figure = self.board.squares[row][col]
                    if figure and figure.color == current_player:
                        for block_pos in blocking_positions:
                            if figure.is_move_valid((row, col), block_pos, self.board.squares):
                                if not self.simulate_move_and_check(current_player, (row, col), block_pos):
                                    return False

        return True

    def simulate_move_and_check(self, current_player, start_pos, end_pos):
        temp_field = self.board.squares[end_pos[0]][end_pos[1]]
        figure = self.board.squares[start_pos[0]][start_pos[1]]

        self.board.squares[end_pos[0]][end_pos[1]] = figure
        self.board.squares[start_pos[0]][start_pos[1]] = None
        figure.position = end_pos

        in_check, _ = self.is_king_in_check(current_player)

        self.board.squares[start_pos[0]][start_pos[1]] = figure
        self.board.squares[end_pos[0]][end_pos[1]] = temp_field
        figure.position = start_pos

        return in_check

    def get_positions_between(self, start_pos, end_pos):
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

    def is_stalemate(self, current_player):
        king_in_check, _ = self.is_king_in_check(current_player)
        if king_in_check:
            return False
        
        for row in range(8):
            for col in range(8):
                figure = self.board.squares[row][col]
                if figure and figure.color == current_player:
                    start_pos = (row, col)
                    for end_row in range(8):
                        for end_col in range(8):
                            end_pos = (end_row, end_col)
                            if figure.is_move_valid(start_pos, end_pos, self.board.squares):
                                if not self.simulate_move_and_check(current_player, start_pos, end_pos):
                                    return False
        return True
    
    def promote_pawn(self, position, promotion_choice):
        #aktuell nur mit queen weil keine user eingabe
        pawn = self.board.squares[position[0]][position[1]]
        if not isinstance(pawn, Pawn):
            raise ValueError("Nur pawnn sollten umgewandelt werden können.")
        if promotion_choice == "queen":
            promoted_figure = Queen(pawn.color, position)
        elif promotion_choice == "rook":
            promoted_figure = Rook(pawn.color, position)
        elif promotion_choice == "bishop":
            promoted_figure = Bishop(pawn.color, position)
        elif promotion_choice == "knight":
            promoted_figure = Knight(pawn.color, position)
        else:
            raise ValueError(f"Fehlerhaft Auswahl: {promotion_choice}")

        promoted_figure.id = pawn.id

        self.board.squares[position[0]][position[1]] = promoted_figure

        move_notation = (
            f"pawn ({pawn.color}, UUID: {pawn.id}) auf {self.convert_to_coordinates(position)} "
            f"zu {promotion_choice}"
        )
        self.get_current_player().record_move(move_notation)
        return move_notation
    
    def handle_rochade(self, king, start_pos, end_pos):
        if abs(start_pos[1] - end_pos[1]) != 2:
            return False
        #kurze oder lange Rochade
        row = start_pos[0]
        direction = 1 if end_pos[1] > start_pos[1] else -1 
        rook_col = 7 if direction == 1 else 0
        rook_target_col = 5 if direction == 1 else 3

        rook = self.board.squares[row][rook_col]
        if not isinstance(rook, Rook):
            return False

        if king.has_moved or rook.has_moved:
            return False

        positions_between = self.get_positions_between(start_pos, (row, rook_col))
        for position in positions_between:
            if self.board.squares[position[0]][position[1]] is not None:
                return False

        for col in range(start_pos[1], end_pos[1] + direction, direction):
            temp_king_pos = (row, col)
            if self.simulate_move_and_check(king.color, start_pos, temp_king_pos):
                return False

        self.board.squares[row][rook_col] = None
        self.board.squares[row][rook_target_col] = rook
        rook.position = (row, rook_target_col)

        self.board.squares[start_pos[0]][start_pos[1]] = None
        self.board.squares[end_pos[0]][end_pos[1]] = king
        king.position = end_pos

        move_notation = (
            f"Rochade {'kurz' if direction == 1 else 'lang'}: "
            f"King ({king.color}, UUID: {king.id}) ({rook.color}, UUID: {rook.id})"
            f"von {self.convert_to_coordinates(start_pos)} auf {self.convert_to_coordinates(end_pos)}"
        )
        self.get_current_player().record_move(move_notation)
        return True

    def move_figure(self, start_pos, end_pos, figure_id=None):
        if start_pos == end_pos:
            raise ChessException("Ungültiger Zug: Nicht auf das gleiche Feld ziehen!", 400)
        figure = self.board.squares[start_pos[0]][start_pos[1]]
        target_field = self.board.squares[end_pos[0]][end_pos[1]]

        if figure is None:
            raise ChessException("Ungültiger Zug: Bitte kein leeres Feld auswählen!", 400)
        
        if figure_id and figure.id != figure_id:
            raise ChessException("interner Fehler: Figuren-ID stimmt nicht überein!", 400)
        
        if figure.color != self.current_player:
            raise ChessException(f"Es ist {self.current_player}'s Zug!", 403)
        
        if isinstance(figure, King) and abs(start_pos[1] - end_pos[1]) == 2:
            if self.handle_rochade(figure, start_pos, end_pos):
                self.switch_player()
                return f"Rochade erfolgreich von {start_pos} nach {end_pos}"
            else:
                raise ChessException(f"Ungültiger Zug: Rochade nicht erlaubt")
        
        if not figure.is_move_valid(start_pos, end_pos, self.board.squares, self.last_move):
            raise ChessException("Ungültiger Zug: Bewegung nicht erlaubt!", 400)
        
        if self.simulate_move_and_check(self.current_player, start_pos, end_pos):
            raise ChessException("Ungültiger Zug: Dein König steht im Schach!", 400)

        if target_field and target_field.color == figure.color:
            return "Ungültiger Zug! Zielfeld ist durch eine eigene Figur blockiert."
        
        id_validation_result = self.validate_target_id(target_field)
        # if id_validation_result:
        #     return id_validation_result

        en_passant_notation = self.handle_en_passant(figure, start_pos, end_pos, target_field)
        if en_passant_notation:
            return en_passant_notation
        
        move_notation = self.generate_move_notation(figure, target_field, start_pos, end_pos)
        self.execute_move(figure, start_pos, end_pos, move_notation)

        self.last_move = {
            "figure": figure,
            "start_pos": start_pos,
            "end_pos": end_pos,
            "two_square_pawn_move": isinstance(figure, Pawn) and abs(start_pos[0] - end_pos[0]) == 2,
        }
        return move_notation

    def validate_target_id(self, target_field):
        if target_field:
            last_move = self.get_last_move_or_set_start(target_field)
            if last_move and "UUID:" in last_move:
                uuid_start = last_move.find("UUID: ") + len("UUID: ")
                uuid_end = last_move.find(")", uuid_start)
                if uuid_start == -1 or uuid_end == -1:
                    return "Fehler: UUID nicht gefunden!"
                expected_target_uuid = last_move[uuid_start:uuid_end]
                if target_field.id != expected_target_uuid:
                    return "Fehler: UUID stimmen nicht überein!"
        return None

    def get_last_move_or_set_start(self, target_field):
        last_move = None
        if self.current_player == "black" and self.white_player.move_history:
            last_move = self.white_player.move_history[-1]
        elif self.current_player == "white" and self.black_player.move_history:
            last_move = self.black_player.move_history[-1]

        if not last_move or "UUID:" not in last_move:
            start_pos = target_field.position
            last_move = (
                f"{target_field.name} ({target_field.color}, UUID: {target_field.id}) "
                f"auf {self.convert_to_coordinates(start_pos)}"
            )
        return last_move

    def handle_en_passant(self, figure, start_pos, end_pos, target_field):
        if isinstance(figure, Pawn) and target_field is None:
            if abs(end_pos[1] - start_pos[1]) == 1: 
                captured_pawn_row = start_pos[0] 
                captured_pawn_col = end_pos[1]
                captured_pawn = self.board.squares[captured_pawn_row][captured_pawn_col]
                
                if (
                    isinstance(captured_pawn, Pawn)
                    and captured_pawn.color != figure.color
                    and self.last_move
                    and self.last_move["figure"] == captured_pawn
                    and self.last_move["two_square_pawn_move"]
                ):
                    self.board.squares[captured_pawn_row][captured_pawn_col] = None
                    
                    move_notation = (
                        f"{figure.name} ({figure.color}, UUID: {figure.id}) schlägt "
                        f"{captured_pawn.name} ({captured_pawn.color}, UUID: {captured_pawn.id}) "
                        f"auf {self.convert_to_coordinates((captured_pawn.position))} "
                        f"en passant von {self.convert_to_coordinates(start_pos)} auf {self.convert_to_coordinates(end_pos)}"
                    )
                    
                    self.execute_move(figure, start_pos, end_pos, move_notation)
                    return move_notation
        return None

    def generate_move_notation(self, figure, target_field, start_pos, end_pos):
        notation = None
        if target_field is None:
            notation = (
                f"{figure.name} ({figure.color}, UUID: {figure.id}) "
                f"von {self.convert_to_coordinates(start_pos)} auf {self.convert_to_coordinates(end_pos)}"
            )
        else:
            notation = (
                f"{figure.name} ({figure.color}, UUID: {figure.id}) schlägt "
                f"{target_field.name} ({target_field.color}, UUID: {target_field.id}) "
                f"von {self.convert_to_coordinates(start_pos)} auf {self.convert_to_coordinates(end_pos)}"
            )
        
        return notation

    def execute_move(self, figure, start_pos, end_pos, move_notation):
        if move_notation is None:
            return
        
        self.board.squares[end_pos[0]][end_pos[1]] = figure
        self.board.squares[start_pos[0]][start_pos[1]] = None
        figure.position = end_pos
        self.get_current_player().record_move(move_notation)
        figure.move_history.append(move_notation)
        
        if isinstance(figure, Pawn) and end_pos[0] in (0, 7):
            promotion_choice = self.get_current_player().choose_promotion()
            self.promote_pawn(end_pos, promotion_choice)
        
        self.switch_player()
