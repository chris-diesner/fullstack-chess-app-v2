from models.chess_game import ChessGame, GameStatus
from models.user import UserInGame, UserLobby, PlayerColor
from repositories.chess_game_repo import ChessGameRepository
from services.chess_board_service import ChessBoardService
from models.figure import Figure, King, Queen, Bishop, Knight, Rook, Pawn, FigureColor
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

    def move_figure(self, start_pos: tuple[int, int], end_pos: tuple[int, int], game_id: str) -> ChessGame | None:
        game = self.get_game_state(game_id)
        if game.status != GameStatus.RUNNING:
            raise ValueError("Spiel ist bereits beendet.")

        figure = game.board.squares[start_pos[0]][start_pos[1]]
        
        if figure is None:
            raise ValueError("Du hast ein leeres Feld ausgewählt!")

        if figure.color.value != game.current_turn:
            raise ValueError(f"Es ist {game.current_turn}'s Zug!")

        if not MoveValidationService.is_move_valid(figure, start_pos, end_pos, game.board, game):
            raise ValueError("Ungültiger Zug!")
        
        if MoveValidationService.is_king_in_check(game, game.board)[0]:
            raise ValueError("Zug nicht möglich! Dein König steht im Schach!")
        
        if MoveValidationService.simulate_move_and_check(game, game.board, start_pos, end_pos):
            raise ValueError("Zug nicht möglich! Dein König stünde im Schach!")
        
        game.board.squares[end_pos[0]][end_pos[1]] = figure
        game.board.squares[start_pos[0]][start_pos[1]] = None
        figure.position = end_pos
        
        game.last_move = {
            "figure": figure,
            "start": start_pos,
            "end": end_pos,
            "two_square_pawn_move": isinstance(figure, Pawn) and abs(start_pos[0] - end_pos[0]) == 2
        }
        
        if isinstance(figure, (King, Rook)):
            figure.has_moved = True
            
        if isinstance(figure, Pawn) and (end_pos[0] == 0 or end_pos[0] == 7):
            self.promote_pawn(game_id, end_pos, "queen")

        game.current_turn = PlayerColor.BLACK.value if game.current_turn == PlayerColor.WHITE.value else PlayerColor.WHITE.value
                
        king_in_check, _ = MoveValidationService.is_king_in_check(game, game.board)
        
        if MoveValidationService.is_stalemate(game, game.board):
            game.status = GameStatus.ENDED
            self.game_repo.insert_game(game)
            raise ValueError("Patt! Spiel endet unentschieden!")

        if MoveValidationService.is_king_checkmate(game, game.board):
            game.status = GameStatus.ENDED
            self.game_repo.insert_game(game)
            winner = PlayerColor.WHITE.value if game.current_turn == PlayerColor.BLACK.value else PlayerColor.BLACK.value
            loser = game.current_turn
            
            self.send_notification(game, f"Schachmatt! {winner} hat gewonnen! {loser} hat verloren!")
        
            raise ValueError(f"Schachmatt! {winner} hat gewonnen! {loser} hat verloren!")
        
        self.game_repo.insert_game(game)
        
        if king_in_check:
            raise ValueError(f"Schach! {game.current_turn} ist im Schach!")
        
        return game
    
    # message handler - WIP - soll noch ausgelagert werden!
    def send_notification(self, game: ChessGame, message: str):
        player_white = game.player_white.username
        player_black = game.player_black.username

        print(f"🔔 Nachricht an {player_white}: {message}")
        print(f"🔔 Nachricht an {player_black}: {message}")

    
    def promote_pawn(self, game_id: str, position: tuple[int, int], promotion_choice: str) -> ChessGame:
        game = self.get_game_state(game_id)

        row, col = position
        figure = game.board.squares[row][col]

        if not isinstance(figure, Pawn):
            raise ValueError("Nur Bauern können umgewandelt werden.")

        promotion_row = 0 if figure.color == FigureColor.WHITE else 7
        if row != promotion_row:
            raise ValueError("Der Bauer hat die letzte Reihe noch nicht erreicht.")

        valid_choices = {
            "queen": Queen,
            "rook": Rook,
            "bishop": Bishop,
            "knight": Knight
        }

        chosen_figure = valid_choices.get(promotion_choice.lower())
        if chosen_figure is None:
            raise ValueError("Ungültige Umwandlungsfigur. Wähle: 'queen', 'rook', 'bishop' oder 'knight'.")

        promoted_figure = chosen_figure(color=figure.color, position=position, id=figure.id)
        game.board.squares[row][col] = promoted_figure

        self.game_repo.insert_game(game)

        return game