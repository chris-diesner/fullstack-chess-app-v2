import uuid
from fastapi.websockets import WebSocket
from models.lobby import Lobby
from models.user import UserLobby
from typing import Dict, List

LOBBY_NOT_FOND_ERROR = "Lobby nicht gefunden."

class ChessLobbyService:
    
    def __init__(self):
        if not hasattr(ChessLobbyService, "game_lobbies"):
            ChessLobbyService.game_lobbies = {}
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
    def get_lobbies(self):
        return ChessLobbyService.game_lobbies
        
    async def connect(self, websocket: WebSocket, game_id: str):
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
                
    async def broadcast(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            for ws in self.active_connections[game_id]:
                await ws.send_json(message)

    async def notify_lobby_update(self, game_id: str):
        if game_id in self.active_connections:
            lobby = self.game_lobbies.get(game_id)
            if lobby:
                data = {
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
                for connection in self.active_connections[game_id]:
                    await connection.send_json(data)

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

    async def join_lobby(self, game_id: str, user: UserLobby) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError("Lobby existiert nicht.")

        if any(player.user_id == user.user_id for player in lobby.players):
            raise ValueError("Du bist bereits in dieser Lobby.")

        if len(lobby.players) >= 2:
            raise ValueError("Lobby ist bereits voll.")

        lobby.players.append(user)
        
        await self.notify_lobby_update(game_id)

        return lobby

    async def leave_lobby(self, game_id: str, user_id: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError("Lobby nicht gefunden, oder bereits gelöscht.")

        if user_id not in [player.user_id for player in lobby.players]:
            raise ValueError("Du bist nicht mehr in dieser Lobby.")
        
        lobby.players.remove(next(player for player in lobby.players if player.user_id == user_id))

        if not lobby.players:
            del self.game_lobbies[game_id]
            return None
        
        await self.notify_lobby_update(game_id)

        return lobby
    
    async def set_player_color(self, game_id: str, user_id: str, color: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError(LOBBY_NOT_FOND_ERROR)

        player = next((player for player in lobby.players if player.user_id == user_id), None)
        if not player:
            raise ValueError("Spieler nicht gefunden.")
        
        if any(player.color == color for player in lobby.players if player.user_id != user_id):
            raise ValueError("Farbe bereits vergeben.")

        player.color = color
        
        await self.notify_lobby_update(game_id)

        return lobby
    
    async def set_player_status(self, game_id: str, user_id: str, status: str) -> Lobby:
        lobby = self.game_lobbies.get(game_id)
        if not lobby:
            raise ValueError(LOBBY_NOT_FOND_ERROR)
        
        player = next((player for player in lobby.players if player.user_id == user_id), None)
        if not player:
            raise ValueError("Spieler nicht gefunden.")
        if player.color == None:
            raise ValueError("Wähle zuerst eine Farbe.")
        player.status = status
        
        await self.notify_lobby_update(game_id)
        
        return lobby