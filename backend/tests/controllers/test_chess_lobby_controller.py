import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from models.user import UserLobby
from models.lobby import Lobby
from repositories.chess_game_repo import ChessGameRepository
from services.chess_lobby_service import ChessLobbyService
from services.chess_game_service import ChessGameService
from models.chess_game import ChessGame
from models.user import UserInGame
from models.chess_game import GameStatus
from services.chess_board_service import ChessBoardService
from jsonschema import validate

client = TestClient(app)

@pytest.fixture
def mock_user_lobby():
    return UserLobby

@pytest.fixture
def mock_lobby_service(mocker):
    mocked_lobby_service = mocker.MagicMock(spec=ChessLobbyService)

    with patch("controllers.chess_lobby_controller.lobby_service", mocked_lobby_service):
        yield mocked_lobby_service
        
@pytest.fixture(scope="function", autouse=True)
def reset_lobby_service():
    from controllers.chess_lobby_controller import lobby_service
    lobby_service.__init__()

@pytest.fixture
def game_repo(mocker):
    """Mockt die ChessGameRepository, um DB-Schreibzugriffe zu verhindern."""
    mocker.patch.object(ChessGameRepository, "insert_game", return_value=None)
    service = ChessGameService()
    service.game_repo = MagicMock()
    return service

@pytest.fixture
def mock_chess_game_service(mocker):
    """Mockt den ChessGameService"""
    mock_service = mocker.MagicMock(spec=ChessGameService)
    mocker.patch("services.chess_game_service.ChessGameService", return_value=mock_service)
    return mock_service

def test_create_lobby_should_return_200_and_json_response(mock_lobby_service):
    user = UserLobby(user_id="1234", username="Max", color=None, status="not_ready")

    mock_lobby_service.create_lobby.return_value = Lobby(
        game_id="1234",
        players=[user]
    )

    lobby_schema = {
        "type": "object",
        "properties": {
            "game_id": {"type": "string"},
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "username": {"type": "string"},
                        "color": {"type": ["string", "null"]},
                        "status": {"type": "string"}
                    },
                    "required": ["user_id", "username", "status"]
                }
            }
        },
        "required": ["game_id", "players"]
    }

    response = client.post("lobby/create", json=user.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    validate(response.json(), lobby_schema)

    response_json = response.json()
    assert "game_id" in response_json
    assert isinstance(response_json["game_id"], str)
    assert len(response_json["players"]) == 1
    assert response_json["players"][0]["user_id"] == "1234"
    assert response_json["players"][0]["username"] == "Max"
    assert response_json["players"][0]["color"] is None
    assert response_json["players"][0]["status"] == "not_ready"
    
def test_create_lobby_should_return_400_and_error_message():
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    
    client.post("lobby/create", json=user)
    
    response = client.post("lobby/create", json=user)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Du hast bereits eine Lobby erstellt. Du darfst aber gerne einer anderen beitreten."}
    
def test_list_lobbies_should_return_200_and_json_response(mock_lobby_service):
    set_lobby_list = [
        {
            "game_id": "1234",
            "players": [
                {"user_id": "user_1", "username": "Max"},
                {"user_id": "user_2", "username": "Anna"}
            ]
        },
        {
            "game_id": "5678",
            "players": [
                {"user_id": "user_3", "username": "Max"},
                {"user_id": "user_4", "username": "Max"}
            ]
        }
    ]

    mock_lobby_service.list_lobbies.return_value = {"lobbies": set_lobby_list}

    response = client.get("/lobby/list")

    lobby_schema = {
        "type": "object",
        "properties": {
            "lobbies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "game_id": {"type": "string"},
                        "players": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "string"},
                                    "username": {"type": "string"}
                                },
                                "required": ["user_id", "username"]
                            }
                        }
                    },
                    "required": ["game_id", "players"]
                }
            }
        },
        "required": ["lobbies"]
    }

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    validate(response.json(), lobby_schema)

    assert response.json() == {"lobbies": set_lobby_list}
    
def test_join_lobby_should_return_200_and_json_response(mock_lobby_service):
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    lobby = {
        "game_id": "1234",
        "players": [
            {"user_id": "5678",
             "username": "Anna",
             "color": None,
             "status": "not_ready"
            }
        ]
    }
    
    mock_lobby_service.join_lobby.return_value = Lobby(
        game_id=lobby["game_id"],
        players=[UserLobby(**user), UserLobby(**lobby["players"][0])]
    )
    
    response = client.post(f"/lobby/join/{lobby['game_id']}", json=user)
    
    lobby_schema = {
        "type": "object",
        "properties": {
            "game_id": {"type": "string"},
            "players": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "username": {"type": "string"},
                        "color": {"type": ["string", "null"]},
                        "status": {"type": "string"}
                    },
                    "required": ["user_id", "username", "status"]
                }
            }
        },
        "required": ["game_id", "players"]
    }
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    validate(response.json(), lobby_schema)
    
    response_json = response.json()
    assert response_json == {
        "game_id": "1234",
        "players": [
            {"user_id": "1234",
             "username": "Max",
             "color": None,
             "status": "not_ready"
            },
            {"user_id": "5678",
             "username": "Anna",
             "color": None,
             "status": "not_ready"
            }
        ]
    }
    
def test_join_lobby_should_return_400_and_error_message_not_found():
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/join/1234", json=user)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Lobby existiert nicht."}
    
def test_join_lobby_should_return_400_and_error_message_already_in_lobby():
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    response = client.post(f"/lobby/join/{lobby}", json=user)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Du bist bereits in dieser Lobby."}
    
def test_join_lobby_should_return_400_and_error_message_lobby_full():
    user_1 = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    user_2 = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    user_3 = {
        "user_id": "9123",
        "username": "Fritz",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user_1)
    lobby = response.json().get("game_id")
    client.post(f"/lobby/join/{lobby}", json=user_2)
    
    response = client.post(f"/lobby/join/{lobby}", json=user_3)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Lobby ist bereits voll."}
    
def test_leave_lobby_should_return_200_and_json_none_for_empty_lobby(mock_lobby_service):
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    
    mock_lobby_service.create_lobby.return_value = Lobby(
        game_id="1234",
        players=[user]
    )
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    mock_lobby_service.leave_lobby.return_value = None
    
    response = client.post(f"/lobby/leave/{lobby}/{user['user_id']}")
    
    assert response.status_code == 200
    assert response.json() is None
    
def test_leave_lobby_should_return_200_and_json_response(mock_lobby_service):
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    lobby = {
        "game_id": "1234",
        "players": [
            {"user_id": "5678",
             "username": "Anna",
             "color": None,
             "status": "not_ready"
            }
        ]
    }
    
    mock_lobby_service.join_lobby.return_value = Lobby(
        game_id=lobby["game_id"],
        players=[UserLobby(**user), UserLobby(**lobby["players"][0])]
    )
    
    response = client.post(f"/lobby/join/{lobby['game_id']}", json=user)
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json == {
        "game_id": "1234",
        "players": [
            {"user_id": "1234",
             "username": "Max",
             "color": None,
             "status": "not_ready"
            },
            {"user_id": "5678",
             "username": "Anna",
             "color": None,
             "status": "not_ready"
            }
        ]
    }
    
    mock_lobby_service.leave_lobby.return_value = Lobby(
        game_id=lobby["game_id"],
        players=[UserLobby(**lobby["players"][0])]
    )
    
    response = client.post(f"/lobby/leave/{lobby['game_id']}/{user['user_id']}")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    response_json = response.json()
    assert response_json == {
        "game_id": "1234",
        "players": [
            {"user_id": "5678",
             "username": "Anna",
             "color": None,
             "status": "not_ready"
            }
        ]
    }
    
def test_leave_lobby_should_return_400_and_error_message_not_found():
    response = client.post("/lobby/leave/1234/1234")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Lobby nicht gefunden, oder bereits gelöscht."}
    
def test_leave_lobby_should_return_400_and_error_message_not_in_lobby():
    user = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    response = client.post(f"/lobby/leave/{lobby}/5678")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Du bist nicht mehr in dieser Lobby."}
    
def test_set_player_color_should_return_200_and_json_response(mock_lobby_service):
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    
    mock_lobby_service.create_lobby.return_value = Lobby(
        game_id="1234",
        players=[user]
    )
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    updated_user = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "not_ready"
    }
    
    mock_lobby_service.set_player_color.return_value = Lobby(
        game_id=lobby,
        players=[updated_user]
    )
    
    response = client.post(f"/lobby/set_color/{lobby}/{user['user_id']}/white")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    response_json = response.json()
    
    assert response_json == {
        "game_id": lobby,
        "players": [
            {"user_id": "5678",
             "username": "Anna",
             "color": "white",
             "status": "not_ready"
            }
        ]
    }
    
def test_set_player_color_should_return_400_and_error_message_player_not_found():
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
        }
    
    user_2 = {
        "user_id": "1234"
    }
    
    lobby = client.post("/lobby/create", json=user).json().get("game_id")
    
    response = client.post(f"/lobby/set_color/{lobby}/{user_2['user_id']}/white")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Spieler nicht gefunden."}
    
def test_set_player_color_should_return_400_and_error_message_color_already_taken():
    user_1 = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "not_ready"
    }
    user_2 = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user_1)
    lobby = response.json().get("game_id")
    client.post(f"/lobby/join/{lobby}", json=user_2)
    
    client.post(f"/lobby/set_color/{lobby}/{user_2['user_id']}/white")
    response = client.post(f"/lobby/set_color/{lobby}/{user_1['user_id']}/white")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Farbe bereits vergeben."}
    
def test_set_player_status_should_return_200_and_json_response():
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    response = client.post(f"/lobby/set_status/{lobby}/5678/ready")
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    response_json = response.json()
    
    assert response_json == {
        "game_id": lobby,
        "players": [
            {"user_id": "5678",
             "username": "Anna",
             "color": "white",
             "status": "ready"
            }
        ]
    }
    
def test_set_player_status_should_return_400_and_error_message_player_not_found():
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    
    user_2 = {
        "user_id": "1234"
    }
    
    lobby = client.post("/lobby/create", json=user).json().get("game_id")
    
    response = client.post(f"/lobby/set_status/{lobby}/{user_2['user_id']}/ready")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Spieler nicht gefunden."}
    
def test_set_player_status_should_return_400_for_color_not_set():
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": None,
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    response = client.post(f"/lobby/set_status/{lobby}/5678/ready")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Wähle zuerst eine Farbe."}
    
def test_start_game_should_return_200_and_json_response_chess_game(mocker):
    lobby = {
        "game_id": "1234",
        "players": [
            {"user_id": "5678", "username": "Anna", "color": "white", "status": "ready"},
            {"user_id": "1234", "username": "Max", "color": "black", "status": "ready"}
        ]
    }

    mocker.patch.object(ChessLobbyService, "start_game", return_value=ChessGame(
        game_id="1234",
        time_stamp_start="2024-01-01T12:00:00",
        player_white=UserInGame(
            user_id="5678",
            username="Anna",
            color="white",
            captured_figures=[],
            move_history=[]
        ),
        player_black=UserInGame(
            user_id="1234",
            username="Max",
            color="black",
            captured_figures=[],
            move_history=[]
        ),
        current_turn="white",
        board=ChessBoardService().initialize_board(),
        status=GameStatus.RUNNING
    ))
    
    game_schema = {
    "type": "object",
        "properties": {
            "game_id": {"type": "string"},
            "time_stamp_start": {"type": "string", "format": "date-time"},
            "player_white": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "username": {"type": "string"},
                    "color": {"type": "string", "enum": ["white", "black"]},
                    "captured_figures": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "move_history": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["user_id", "username", "color", "captured_figures", "move_history"]
            },
            "player_black": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "username": {"type": "string"},
                    "color": {"type": "string", "enum": ["white", "black"]},
                    "captured_figures": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "move_history": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["user_id", "username", "color", "captured_figures", "move_history"]
            },
            "current_turn": {"type": "string", "enum": ["white", "black"]},
            "board": {
                "type": "object",
                "properties": {
                    "squares": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "oneOf": [
                                    {"type": "null"},
                                    {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "name": {"type": "string", "enum": ["pawn", "rook", "knight", "bishop", "queen", "king"]},
                                            "color": {"type": "string", "enum": ["white", "black"]},
                                            "position": {
                                                "type": "array",
                                                "items": {"type": "integer"},
                                                "minItems": 2,
                                                "maxItems": 2
                                            },
                                            "has_moved": {"type": "boolean"}
                                        },
                                        "required": ["id", "name", "color", "position"]
                                    }
                                ]
                            }
                        }
                    }
                },
                "required": ["squares"]
            },
            "status": {"type": "string", "enum": ["running", "ended", "aborted"]}
        },
        "required": ["game_id", "time_stamp_start", "player_white", "player_black", "current_turn", "board", "status"]
    }

    mocker.patch.object(ChessGameRepository, "insert_game", return_value=None)

    response = client.post(f"/lobby/start_game/{lobby['game_id']}/1234")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    validate(response.json(), game_schema)

    response_json = response.json()
    
    assert response_json["game_id"] == "1234"
    assert response_json["time_stamp_start"] == "2024-01-01T12:00:00"
    assert response_json["player_white"]["user_id"] == "5678"
    assert response_json["player_black"]["user_id"] == "1234"
    assert response_json["player_white"]["color"] == "white"
    assert response_json["player_black"]["color"] == "black"
    assert response_json["status"] == "running"
    assert response_json["current_turn"] == "white"

    assert "board" in response_json
    assert isinstance(response_json["board"], dict)
    assert "squares" in response_json["board"]
    assert isinstance(response_json["board"]["squares"], list)

    for row in response_json["board"]["squares"]:
        assert isinstance(row, list)
        for square in row:
            if square is not None:
                assert "id" in square
                assert "name" in square
                assert "color" in square
                assert "position" in square
                assert square["name"] in ["pawn", "rook", "knight", "bishop", "queen", "king"]
                assert square["color"] in ["white", "black"]
                assert isinstance(square["position"], list)
                assert len(square["position"]) == 2
                assert all(isinstance(pos, int) for pos in square["position"])
    
def test_start_game_should_return_400_and_error_message_lobby_not_full():
    user = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "ready"
    }
    
    response = client.post("/lobby/create", json=user)
    lobby = response.json().get("game_id")
    
    response = client.post(f"/lobby/start_game/{lobby}/5678")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Spiel braucht zwei Spieler."}

def test_start_game_should_return_400_and_error_message_lobby_not_found():
    response = client.post("/lobby/start_game/invalid_game_id/5678")

    assert response.status_code == 400
    assert response.json() == {"detail": "Lobby nicht gefunden."}

def test_start_game_should_return_400_and_error_message_only_host_can_start():
    user_1 = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "ready"
    }
    user_2 = {
        "user_id": "1234",
        "username": "Max",
        "color": "black",
        "status": "ready"
    }
    
    response = client.post("/lobby/create", json=user_1)
    lobby = response.json().get("game_id")
    client.post(f"/lobby/join/{lobby}", json=user_2)

    response = client.post(f"/lobby/start_game/{lobby}/1234")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Nur der Host kann das Spiel starten."}

def test_start_game_should_return_400_and_error_message_players_must_choose_color():
    user_1 = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "ready"
    }
    user_2 = {
        "user_id": "1234",
        "username": "Max",
        "color": None,
        "status": "ready"
    }
    
    response = client.post("/lobby/create", json=user_1)
    lobby = response.json().get("game_id")
    response = client.post(f"/lobby/join/{lobby}", json=user_2)
    assert response.status_code == 200

    response = client.post(f"/lobby/start_game/{lobby}/5678")  
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Beide Spieler müssen eine Farbe wählen."}

def test_start_game_should_return_400_and_error_message_players_not_ready():
    user_1 = {
        "user_id": "5678",
        "username": "Anna",
        "color": "white",
        "status": "ready"
    }
    user_2 = {
        "user_id": "1234",
        "username": "Max",
        "color": "black",
        "status": "not_ready"
    }
    
    response = client.post("/lobby/create", json=user_1)
    lobby = response.json().get("game_id")
    client.post(f"/lobby/join/{lobby}", json=user_2)

    response = client.post(f"/lobby/start_game/{lobby}/5678")  
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Beide Spieler müssen bereit sein."}
