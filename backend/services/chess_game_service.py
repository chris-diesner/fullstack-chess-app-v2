from models.chess_game import ChessGame, GameStatus
from models.user import UserInGame, UserLobby, PlayerColor
from repositories.chess_game_repo import ChessGameRepository
from services.chess_board_service import ChessBoardService
from models.figure import Figure
from services.move_validation_service import MoveValidationService
from datetime import datetime

class ChessGameService:
    def __init__(self):
        self.game_repo = ChessGameRepository()
        
    def initialize_game(self, game_id: str, player_white: UserLobby, player_black: UserLobby) -> ChessGame | None:
        chess_board_service = ChessBoardService()
        chess_board_service.initialize_board()
        chess_board = chess_board_service.board

        
        game = ChessGame(
            game_id=game_id,
            time_stamp_start= datetime.now(),
            player_white=UserInGame(user_id=player_white.user_id, username=player_white.username, color=PlayerColor.WHITE),
            player_black=UserInGame(user_id=player_black.user_id, username=player_black.username, color=PlayerColor.BLACK),
            current_turn=PlayerColor.WHITE.value,
            board=chess_board,
            status=GameStatus.RUNNING
        )
        
        self.game_repo.insert_game(game)
        
        return game
    
    def get_game_state(self, game_id: str) -> ChessGame | None:
        game = self.game_repo.find_game_by_id(game_id)
        if not game:
            raise ValueError("Spiel nicht gefunden.")
        return game

    
    
    # def get_game_state(self) -> dict:
    #     return {
    #         "game_id": self.game.game_id,
    #         "board": self.game.board.get_board_state(),
    #         "current_turn": self.game.current_turn.value,
    #         "status": self.game.status.value,
    #         "move_history": self.game.move_history,
    #     }

    # def move_figure(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> str:
    #     if self.game.status != GameStatus.RUNNING:
    #         raise ValueError("Spiel ist bereits beendet.")

    #     figure = self.game.board.squares[start_pos[0]][start_pos[1]]
    #     if figure is None:
    #         raise ValueError("Kein Stein auf Startposition!")

    #     if figure.color != self.game.current_turn:
    #         raise ValueError(f"Es ist {self.game.current_turn.value}'s Zug!")

    #     # Prüfen, ob der Zug gültig ist
    #     if not MoveValidationService.is_move_valid(figure, start_pos, end_pos, self.game.board):
    #         raise ValueError("Ungültiger Zug!")

    #     # Prüfen, ob der Zug den König ins Schach setzt
    #     if self.simulate_move_and_check(start_pos, end_pos):
    #         raise ValueError("Ungültiger Zug: König wäre im Schach!")

    #     # Zug ausführen
    #     self.execute_move(figure, start_pos, end_pos)

    #     # Prüfen auf Schachmatt oder Patt
    #     if self.is_king_in_checkmate(self.game.current_turn):
    #         self.game.status = GameStatus.ENDED
    #         return f"Schachmatt! {self.game.current_turn.value} hat verloren."

    #     if self.is_stalemate(self.game.current_turn):
    #         self.game.status = GameStatus.ENDED
    #         return "Patt! Das Spiel endet unentschieden."

    #     # Spieler wechseln
    #     self.switch_turn()

    #     return f"Zug erfolgreich: {start_pos} -> {end_pos}"

    # def execute_move(self, figure: Figure, start_pos: tuple[int, int], end_pos: tuple[int, int]):
    #     self.game.board.squares[end_pos[0]][end_pos[1]] = figure
    #     self.game.board.squares[start_pos[0]][start_pos[1]] = None
    #     figure.position = end_pos

    #     move_notation = f"{figure.name} von {start_pos} nach {end_pos}"
    #     self.game.move_history.append(move_notation)

    # def switch_turn(self):
    #     """Wechselt den Spieler nach einem gültigen Zug."""
    #     self.game.current_turn = PlayerColor.BLACK if self.game.current_turn == PlayerColor.WHITE else PlayerColor.WHITE

    # def simulate_move_and_check(self, start_pos, end_pos) -> bool:
    #     """Simuliert einen Zug und prüft, ob der König danach im Schach steht."""
    #     figure = self.game.board.squares[start_pos[0]][start_pos[1]]
    #     temp_target = self.game.board.squares[end_pos[0]][end_pos[1]]

    #     # Temporär Zug ausführen
    #     self.game.board.squares[end_pos[0]][end_pos[1]] = figure
    #     self.game.board.squares[start_pos[0]][start_pos[1]] = None
    #     figure.position = end_pos

    #     # Prüfen, ob der König im Schach steht
    #     king_in_check = self.is_king_in_check(self.game.current_turn)

    #     # Zustand zurücksetzen
    #     self.game.board.squares[start_pos[0]][start_pos[1]] = figure
    #     self.game.board.squares[end_pos[0]][end_pos[1]] = temp_target
    #     figure.position = start_pos

    #     return king_in_check

    # def is_king_in_check(self, player_color: PlayerColor) -> bool:
    #     """Prüft, ob der eigene König im Schach steht."""
    #     king_pos = self.game.board.get_king_position(player_color)
    #     if not king_pos:
    #         return False

    #     for row in range(8):
    #         for col in range(8):
    #             enemy_figure = self.game.board.squares[row][col]
    #             if enemy_figure and enemy_figure.color != player_color:
    #                 if MoveValidationService.is_move_valid(enemy_figure, (row, col), king_pos, self.game.board):
    #                     return True
    #     return False
