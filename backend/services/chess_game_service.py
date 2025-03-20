from models.chess_game import ChessGame, GameStatus
from models.user import UserInGame, PlayerColor, PlayerStatus
from models.figure import Figure, FigureColor, Pawn, Rook, Knight, Bishop, Queen, King
from repositories.chess_game_repo import ChessGameRepository
from services.chess_board_service import ChessBoardService
from models.figure import King, Queen, Bishop, Knight, Rook, Pawn, FigureColor
from services.move_validation_service import MoveValidationService
from services.chess_lobby_service import ChessLobbyService
from typing import Dict, List
from fastapi.websockets import WebSocket
from datetime import datetime
import copy
import asyncio

class ChessGameException(Exception):
    """Benutzerdefinierte Exception für Schachspiel-Fehler."""
    pass

LOBBY_NOT_FOUND_ERROR = "Lobby nicht gefunden."

class ChessGameService:
    def __init__(self):
        self.game_repo = ChessGameRepository()
        self.active_game_connections: Dict[str, List[WebSocket]] = {}
        self.lobby_service = ChessLobbyService()
        
        print(f"🕵️‍♂️ Instanz-Check ChessLobbyService in GameService: {id(self.lobby_service)}")
        
    async def connect(self, websocket: WebSocket, game_id: str):
        if game_id not in self.active_game_connections:
            self.active_game_connections[game_id] = []
        self.active_game_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_game_connections:
            self.active_game_connections[game_id].remove(websocket)
            if not self.active_game_connections[game_id]:
                del self.active_game_connections[game_id]

    async def broadcast(self, game_id: str, message: dict):
        
        if game_id in self.active_game_connections:
            
            for index, ws in enumerate(self.active_game_connections[game_id]):
                try:
                    await ws.send_json(message)
                except Exception as e:
                    print(f"Fehler beim Senden an WebSocket [{index+1}]: {e}")
        else:
            print(f"[BROADCAST] Keine aktiven WebSocket-Verbindungen für game_id={game_id}.")
                
    async def start_game(self, game_id: str, user_id: str) -> ChessGame:
        lobby = self.lobby_service.get_lobbies(game_id)
        if not lobby:
            raise ChessGameException("Lobby nicht gefunden.")

        if len(lobby.players) < 2:
            raise ChessGameException("Spiel braucht zwei Spieler.")

        if user_id != lobby.players[0].user_id:
            raise ChessGameException("Nur der Host kann das Spiel starten.")

        player_white = next((player for player in lobby.players if player.color == PlayerColor.WHITE), None)
        player_black = next((player for player in lobby.players if player.color == PlayerColor.BLACK), None)

        if not player_white or not player_black:
            raise ChessGameException("Beide Spieler müssen eine Farbe wählen.")

        if any(player.status != PlayerStatus.READY for player in lobby.players):
            raise ChessGameException("Beide Spieler müssen bereit sein.")

        chess_board_service = ChessBoardService()
        chess_board_service.initialize_board()
        chess_board = chess_board_service.board

        game = ChessGame(
            game_id=game_id,
            time_stamp_start=datetime.now(),
            player_white=UserInGame(
                user_id=player_white.user_id, 
                username=player_white.username, 
                color=player_white.color
            ),
            player_black=UserInGame(
                user_id=player_black.user_id, 
                username=player_black.username, 
                color=player_black.color
            ),
            current_turn=PlayerColor.WHITE,
            board=chess_board,
            status=GameStatus.RUNNING
        )

        if isinstance(game, dict):
            game = ChessGame(**game)

        self.game_repo.insert_game(game.model_dump())
        await self.lobby_service.notify_game_start(game.game_id)
        await asyncio.sleep(5)
        await self.broadcast(game_id, {"type": "game_state", "data": game.model_dump()})
        return game

    def get_game_state(self, game_id: str) -> ChessGame | None:
        game_data = self.game_repo.find_game_by_id(game_id)
        
        if not game_data:
            raise ValueError("Spiel nicht gefunden.")
        
        if isinstance(game_data, ChessGame):
            game_dict = game_data.model_dump()
        else:
            game_dict = game_data

        for row in game_dict["board"]["squares"]:
            for i, figure in enumerate(row):
                if figure:
                    row[i] = self.convert_figure(figure)

        return ChessGame(**game_dict)

    @staticmethod
    def convert_figure(figure_data: dict) -> Figure:
        if not isinstance(figure_data, dict):
            return figure_data

        figure_classes = {
            "pawn": Pawn, "rook": Rook, "knight": Knight,
            "bishop": Bishop, "queen": Queen, "king": King
        }
        
        figure_name = figure_data.get("name", "").lower()
        figure_class = figure_classes.get(figure_name, None)

        if figure_class:
            return figure_class(**figure_data)
        
        raise ValueError(f"Unbekannte Figur: {figure_data}")

    async def move_figure(self, start_pos: tuple[int, int], end_pos: tuple[int, int], game_id: str, user_id: str) -> ChessGame | None:
        game = self.get_game_state(game_id)        

        if (game.current_turn == PlayerColor.WHITE and user_id != game.player_white.user_id) or \
            (game.current_turn == PlayerColor.BLACK and user_id != game.player_black.user_id):
                raise ValueError("Nicht dein Zug!")

        if game.status != GameStatus.RUNNING:
            raise ValueError("Spiel ist bereits beendet.")

        figure = game.board.squares[start_pos[0]][start_pos[1]]
        figure = self.convert_figure(figure) if isinstance(figure, dict) else figure
        
        if figure is None:
            raise ValueError("Du hast ein leeres Feld ausgewählt!")
        
        if figure.color.value != game.current_turn:
            raise ValueError(f"Es ist {game.current_turn}'s Zug!")
        
        if not MoveValidationService.is_move_valid(figure, start_pos, end_pos, game.board, game):
            raise ValueError("Ungültiger Zug - from MoveValidationService!")
        
        if MoveValidationService.is_king_in_check(game, game.board)[0]:
            raise ValueError("Zug nicht möglich! Dein König steht im Schach!")
        
        if MoveValidationService.simulate_move_and_check(game, game.board, start_pos, end_pos):
            raise ValueError("Zug nicht möglich! Dein König stünde im Schach!")
        
        if captured_figure := game.board.squares[end_pos[0]][end_pos[1]]:
            capturing_player = game.player_black if captured_figure.color == FigureColor.WHITE else game.player_white
            capturing_player.captured_figures.append(copy.deepcopy(captured_figure))

        game.board.squares[end_pos[0]][end_pos[1]] = figure
        game.board.squares[start_pos[0]][start_pos[1]] = None
        figure.position = end_pos
                
        active_player = game.player_white if game.current_turn == PlayerColor.WHITE else game.player_black
        notation = f"{figure.position}{start_pos[1]}{start_pos[0]}{end_pos[1]}{end_pos[0]}"
        active_player.move_history.append(notation)
        
        game.last_move = {
            "figure": figure,
            "start": start_pos,
            "end": end_pos,
            "two_square_pawn_move": isinstance(figure, Pawn) and abs(start_pos[0] - end_pos[0]) == 2
        }
        
        if isinstance(figure, (King, Rook)):
            figure.has_moved = True
            
        if isinstance(figure, Pawn) and (end_pos[0] == 0 or end_pos[0] == 7):
            await self.promote_pawn(game_id, end_pos, "queen")

        game.current_turn = PlayerColor.BLACK if game.current_turn == PlayerColor.WHITE else PlayerColor.WHITE
                
        await self.broadcast(game_id, {"type": "game_state", "data": game.model_dump()})
        
        king_in_check, _ = MoveValidationService.is_king_in_check(game, game.board)
        
        if MoveValidationService.is_stalemate(game, game.board):
            game.status = GameStatus.ENDED
            self.game_repo.insert_game(game)
            raise ValueError("Patt! Spiel endet unentschieden!")

        if MoveValidationService.is_king_checkmate(game, game.board):
            game.status = GameStatus.ENDED
            self.game_repo.insert_game(game)
            winner = PlayerColor.WHITE if game.current_turn == PlayerColor.BLACK else PlayerColor.BLACK
            loser = game.current_turn
            
            await self.send_notification(game.game_id, f"Schachmatt! {winner} hat gewonnen! {loser} hat verloren!")
        
            raise ValueError(f"Schachmatt! {winner} hat gewonnen! {loser} hat verloren!")
        
        self.game_repo.insert_game(game)
        
        if king_in_check:
            raise ValueError(f"Schach! {game.current_turn.value} ist im Schach!")
        
        return game
    
    async def send_notification(self, game_id: str, message: str):
        await self.broadcast(game_id, {"type": "notification", "message": message})

    async def promote_pawn(self, game_id: str, position: tuple[int, int], promotion_choice: str) -> ChessGame:
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
    