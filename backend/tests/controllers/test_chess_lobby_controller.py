import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from models.user import UserLobby
from models.lobby import Lobby
from repositories.chess_game_repo import ChessGameRepository
from services.chess_lobby_service import ChessLobbyService
from services.chess_game_service import ChessGameService
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
    from services.chess_lobby_service import ChessLobbyService
    ChessLobbyService().game_lobbies.clear()

@pytest.fixture
def game_repo(mocker):
    mocker.patch.object(ChessGameRepository, "insert_game", return_value=None)
    service = ChessGameService()
    service.game_repo = MagicMock()
    return service

@pytest.fixture
def mock_chess_game_service(mocker):
    mock_service = mocker.MagicMock(spec=ChessGameService)
    mocker.patch("services.chess_game_service.ChessGameService", return_value=mock_service)
    return mock_service

def test_websocket_lobby_should_return_200():
    with client.websocket_connect("/lobby/ws/1234") as websocket:
        websocket.send_json({"action": "refresh"})
        data = websocket.receive_json()
        assert data == {"message": "refresh_lobby"}

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