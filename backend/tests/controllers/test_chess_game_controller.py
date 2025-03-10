import pytest
import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app
from services.chess_game_service import ChessGameService

client = TestClient(app)

@pytest.fixture
def mock_db(mocker):
    mock_repo = mocker.patch("repositories.chess_game_repo.ChessGameRepository")
    mock_repo.find_game_by_id = MagicMock()
    mock_repo.insert_game = MagicMock()
    return mock_repo

@pytest.fixture
def initialized_game():
    game_id = str(uuid.uuid4())

    game = {
        "game_id": game_id,
        "time_stamp_start": "2024-03-06T12:00:00Z",
        "player_white": {
            "user_id": "1234",
            "username": "Max",
            "color": "white",
            "captured_figures": [],
            "move_history": []
        },
        "player_black": {
            "user_id": "5678",
            "username": "Anna",
            "color": "black",
            "captured_figures": [],
            "move_history": []
        },
        "current_turn": "white",
        "board": {
            "squares": [
                [{"type": "rook", "color": "black", "position": [0, 0]}, None, None, None, None, None, None, {"type": "rook", "color": "black", "position": [0, 7]}],
                [{"type": "pawn", "color": "black", "position": [1, 0]}, None, None, None, None, None, None, {"type": "pawn", "color": "black", "position": [1, 7]}],
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [None] * 8,
                [{"type": "pawn", "color": "white", "position": [6, 0]}, None, None, None, None, None, None, {"type": "pawn", "color": "white", "position": [6, 7]}],
                [{"type": "rook", "color": "white", "position": [7, 0]}, None, None, None, None, None, None, {"type": "rook", "color": "white", "position": [7, 7]}]
            ]
        },
        "status": "running",
        "last_move": None
    }

    return game

def test_move_figure_should_return_200_and_update_game_blablub(mocker, mock_db, initialized_game):
    
    game_id = initialized_game["game_id"]
    user_white_id = initialized_game["player_white"]["user_id"]
    user_black_id = initialized_game["player_black"]["user_id"]

    mock_db.find_game_by_id.return_value = initialized_game

    mocker.patch.object(ChessGameService, "move_figure", return_value=initialized_game)

    move_white = {"start_pos": [6, 0], "end_pos": [5, 0]}
    response = client.post(f"/game/move/{game_id}/{user_white_id}", json=move_white)
    assert response.status_code == 200
