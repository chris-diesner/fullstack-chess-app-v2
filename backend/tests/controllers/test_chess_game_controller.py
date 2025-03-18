import pytest
import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from services.chess_game_service import ChessGameService
from services.chess_board_service import ChessBoardService
from repositories.chess_game_repo import ChessGameRepository
from models.chess_game import ChessGame
from models.user import UserInGame
from models.chess_game import GameStatus
from jsonschema import validate

client = TestClient(app)

@pytest.fixture
def mock_db(mocker):
    mock_repo = mocker.patch("repositories.chess_game_repo.ChessGameRepository")
    mock_repo.find_game_by_id = MagicMock()
    mock_repo.insert_game = MagicMock()
    return mock_repo

@pytest.fixture
def initialized_game(mocker):
    game_id = str(uuid.uuid4())

    game = ChessGame(
        game_id=game_id,
        time_stamp_start="2024-03-06T12:00:00Z",
        player_white=UserInGame(
            user_id="1234",
            username="Max",
            color="white",
            captured_figures=[],
            move_history=[]
        ),
        player_black=UserInGame(
            user_id="5678",
            username="Anna",
            color="black",
            captured_figures=[],
            move_history=[]
        ),
        current_turn="white",
        board=ChessBoardService().initialize_board(),
        status=GameStatus.RUNNING
    )

    mocker.patch.object(
        ChessGameRepository,
        "find_game_by_id",
        return_value=game
    )

    return game

def test_websocket_connect_should_return_broadcast_initial_game_state_message(initialized_game):
    game_id = initialized_game.game_id

    with client.websocket_connect(f"game/ws/{game_id}") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "game_state"

def test_websocket_move_success_should_return_broadcast_new_game_state(initialized_game):
    game_id = initialized_game.game_id
    user_id = "1234"

    move_data = {
        "action": "move",
        "game_id": game_id,
        "start_pos": [6, 0],
        "end_pos": [5, 0],
        "user_id": user_id
    }

    with client.websocket_connect(f"game/ws/{game_id}") as websocket:
        websocket.send_json(move_data)

        for _ in range(5):
            data = websocket.receive_json()

            if data["type"] == "game_state" and data["data"]["current_turn"] == "black":
                break
        else:
            pytest.fail("Timeout!")
            
        assert data["type"] == "game_state"
        assert "data" in data

        game_state = data["data"]

        assert game_state["current_turn"] == "black"

        board = game_state["board"]["squares"]

        assert board[6][0] is None

        moved_figure = board[5][0]
        assert moved_figure is not None
        assert moved_figure["name"] == "pawn"
        assert moved_figure["color"] == "white"
        assert moved_figure["position"] == [5, 0]
        assert "last_move" in game_state
        last_move = game_state["last_move"]
        assert last_move["start"] == [6, 0]
        assert last_move["end"] == [5, 0]

        assert game_state["status"] == "running"

def test_start_game_should_return_200_and_json_response_chess_game(mocker):
    lobby = {
        "game_id": "1234",
        "players": [
            {"user_id": "5678", "username": "Anna", "color": "white", "status": "ready"},
            {"user_id": "1234", "username": "Max", "color": "black", "status": "ready"}
        ]
    }

    mocker.patch.object(ChessGameService, "start_game", return_value=ChessGame(
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

    response = client.post(f"/game/start_game/{lobby['game_id']}/1234")

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
    