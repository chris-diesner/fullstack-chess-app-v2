import uuid
from models.lobby import Lobby
from models.user import UserLobby, PlayerColor, PlayerStatus
from models.chess_game import ChessGame
from services.chess_game_service import ChessGameService
from typing import Dict

LOBBY_NOT_FOND_ERROR = "Lobby nicht gefunden."

class ChessLobbyService:
    
    def __init__(self):
        self.game_lobbies: Dict[str, Lobby] = {}

    def create_lobby(self, user: UserLobby) -> Lobby:
        for lobby in self.game_lobbies.values():
            if any(player.user_id == user.user_id for player in lobby.players):
                raise ValueError("Du hast bereits eine Lobby erstellt. Du darfst aber gerne einer anderen beitreten.")

        game_id = str(uuid.uuid4()) 

        new_lobby = Lobby(
            game_id=game_id,
            players=[user]
        )

        self.game_lobbies[game_id] = new_lobby
        return new_lobby

    def list_lobbies(self) -> dict:
        return {
            "lobbies": [
                {
                    "game_id": lobby.game_id,
                    "players": [
                        {
                            "user_id": user.user_id,
                            "username": user.username,
                            "color": user.color,
                            "status": user.status
                        }
                        for user in lobby.players
                    ]
                }
                for lobby in self.game_lobbies.values()
            ]
        }


    def join_lobby(self, game_id: str, user: UserLobby) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError("Lobby existiert nicht.")

        if any(player.user_id == user.user_id for player in lobby.players):
            raise ValueError("Du bist bereits in dieser Lobby.")

        if len(lobby.players) >= 2:
            raise ValueError("Lobby ist bereits voll.")

        lobby.players.append(user)

        return lobby

    def leave_lobby(self, game_id: str, user_id: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError("Lobby nicht gefunden, oder bereits gelöscht.")

        if user_id not in [player.user_id for player in lobby.players]:
            raise ValueError("Du bist nicht mehr in dieser Lobby.")
        
        lobby.players.remove(next(player for player in lobby.players if player.user_id == user_id))

        if not lobby.players:
            del self.game_lobbies[game_id]
            return None

        return lobby
    
    def set_player_color(self, game_id: str, user_id: str, color: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError(LOBBY_NOT_FOND_ERROR)

        player = next((player for player in lobby.players if player.user_id == user_id), None)
        if not player:
            raise ValueError("Spieler nicht gefunden.")
        
        if any(player.color == color for player in lobby.players if player.user_id != user_id):
            raise ValueError("Farbe bereits vergeben.")

        player.color = color

        return lobby
    
    def set_player_status(self, game_id: str, user_id: str, status: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError(LOBBY_NOT_FOND_ERROR)
        
        player = next((player for player in lobby.players if player.user_id == user_id), None)
        if not player:
            raise ValueError("Spieler nicht gefunden.")
        if player.color == None:
            raise ValueError("Wähle zuerst eine Farbe.")
        player.status = status
        
        return lobby
    
    def start_game(self, game_id, user_id) -> ChessGame:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError(LOBBY_NOT_FOND_ERROR)
        
        if len(lobby.players) < 2:
            raise ValueError("Spiel braucht zwei Spieler.")
        
        if user_id != lobby.players[0].user_id:
            raise ValueError("Nur der Host kann das Spiel starten.")
        
        player_white = next((player for player in lobby.players if player.color == PlayerColor.WHITE), None)
        player_black = next((player for player in lobby.players if player.color == PlayerColor.BLACK), None)
        
        if not player_white or not player_black:
            raise ValueError("Beide Spieler müssen eine Farbe wählen.")
        
        if any(player.status != PlayerStatus.READY for player in lobby.players):
            raise ValueError("Beide Spieler müssen bereit sein.")
        
        game_service = ChessGameService()
        game = game_service.initialize_game(game_id, player_white, player_black)
        
        return game
