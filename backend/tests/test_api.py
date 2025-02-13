import pytest
import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app
from chess_game import ChessGame
from figures.figure import Pawn


@pytest.fixture(autouse=True)
def reset_game(client):
    client.post("/game/reset")
    
@pytest.fixture
def fixed_uuid():
    return uuid.UUID("12345678-1234-5678-1234-567812345678")  

@pytest.fixture
def client():
    app.dependency_overrides[ChessGame] = lambda: ChessGame()  
    test_client = TestClient(app)
    test_client.post("/game/reset")  
    return test_client

def test_game_lifecycle_should_return_200OK(client):
    response = client.post("/game/new")
    assert response.status_code == 200
    game_id = response.json()["game_id"]
    
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    
    response = client.post(f"/game/{game_id}/move?start_pos=f2&end_pos=f3")
    assert response.status_code == 200
    
def test_get_board_should_return_200OK_and_correct_positions(client):
    response = client.post("/game/new")
    assert response.status_code == 200
    game_id = response.json()["game_id"]
    expected_board = {
        "game_id": game_id,
        "current_player": "white",
        "check_mate_status": "normal",
        "board": [
            [
                {"type": "rook", "color": "black", "position": "a8"},
                {"type": "knight", "color": "black", "position": "b8"},
                {"type": "bishop", "color": "black", "position": "c8"},
                {"type": "queen", "color": "black", "position": "d8"},
                {"type": "king", "color": "black", "position": "e8"},
                {"type": "bishop", "color": "black", "position": "f8"},
                {"type": "knight", "color": "black", "position": "g8"},
                {"type": "rook", "color": "black", "position": "h8"},
            ],
            [
                {"type": "pawn", "color": "black", "position": "a7"},
                {"type": "pawn", "color": "black", "position": "b7"},
                {"type": "pawn", "color": "black", "position": "c7"},
                {"type": "pawn", "color": "black", "position": "d7"},
                {"type": "pawn", "color": "black", "position": "e7"},
                {"type": "pawn", "color": "black", "position": "f7"},
                {"type": "pawn", "color": "black", "position": "g7"},
                {"type": "pawn", "color": "black", "position": "h7"},
            ],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [
                {"type": "pawn", "color": "white", "position": "a2"},
                {"type": "pawn", "color": "white", "position": "b2"},
                {"type": "pawn", "color": "white", "position": "c2"},
                {"type": "pawn", "color": "white", "position": "d2"},
                {"type": "pawn", "color": "white", "position": "e2"},
                {"type": "pawn", "color": "white", "position": "f2"},
                {"type": "pawn", "color": "white", "position": "g2"},
                {"type": "pawn", "color": "white", "position": "h2"},
            ],
            [
                {"type": "rook", "color": "white", "position": "a1"},
                {"type": "knight", "color": "white", "position": "b1"},
                {"type": "bishop", "color": "white", "position": "c1"},
                {"type": "queen", "color": "white", "position": "d1"},
                {"type": "king", "color": "white", "position": "e1"},
                {"type": "bishop", "color": "white", "position": "f1"},
                {"type": "knight", "color": "white", "position": "g1"},
                {"type": "rook", "color": "white", "position": "h1"},
            ],
        ]
    }
    
    response = client.get(f"/game/{game_id}/board")

    assert response.status_code == 200
    data = response.json()

    assert len(data["board"]) == 8
    assert all(len(row) == 8 for row in data["board"])

    assert data == expected_board

def test_post_fools_mate_should_return_200OK_and_updated_boards_after_every_move(client):
    response = client.post("/game/new")
    assert response.status_code == 200
    game_id = response.json()["game_id"]
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    initial_board = response.json()
    expected_initial_board = {
    "game_id": game_id,
    "current_player": "white",
    "check_mate_status": "normal",
    "board": [
        [
            {"type": "rook", "color": "black", "position": "a8"},
            {"type": "knight", "color": "black", "position": "b8"},
            {"type": "bishop", "color": "black", "position": "c8"},
            {"type": "queen", "color": "black", "position": "d8"},
            {"type": "king", "color": "black", "position": "e8"},
            {"type": "bishop", "color": "black", "position": "f8"},
            {"type": "knight", "color": "black", "position": "g8"},
            {"type": "rook", "color": "black", "position": "h8"},
        ],
        [
            {"type": "pawn", "color": "black", "position": "a7"},
            {"type": "pawn", "color": "black", "position": "b7"},
            {"type": "pawn", "color": "black", "position": "c7"},
            {"type": "pawn", "color": "black", "position": "d7"},
            {"type": "pawn", "color": "black", "position": "e7"},
            {"type": "pawn", "color": "black", "position": "f7"},
            {"type": "pawn", "color": "black", "position": "g7"},
            {"type": "pawn", "color": "black", "position": "h7"},
        ],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [
            {"type": "pawn", "color": "white", "position": "a2"},
            {"type": "pawn", "color": "white", "position": "b2"},
            {"type": "pawn", "color": "white", "position": "c2"},
            {"type": "pawn", "color": "white", "position": "d2"},
            {"type": "pawn", "color": "white", "position": "e2"},
            {"type": "pawn", "color": "white", "position": "f2"},
            {"type": "pawn", "color": "white", "position": "g2"},
            {"type": "pawn", "color": "white", "position": "h2"},
        ],
        [
            {"type": "rook", "color": "white", "position": "a1"},
            {"type": "knight", "color": "white", "position": "b1"},
            {"type": "bishop", "color": "white", "position": "c1"},
            {"type": "queen", "color": "white", "position": "d1"},
            {"type": "king", "color": "white", "position": "e1"},
            {"type": "bishop", "color": "white", "position": "f1"},
            {"type": "knight", "color": "white", "position": "g1"},
            {"type": "rook", "color": "white", "position": "h1"},
        ],
    ]
}

    assert initial_board == expected_initial_board

    client.post(f"/game/{game_id}/move?start_pos=f2&end_pos=f3")
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    expected_board_1 = {
    "game_id": game_id,
    "current_player": "black",
    "check_mate_status": "normal",
    "board": [
        [
            {"type": "rook", "color": "black", "position": "a8"},
            {"type": "knight", "color": "black", "position": "b8"},
            {"type": "bishop", "color": "black", "position": "c8"},
            {"type": "queen", "color": "black", "position": "d8"},
            {"type": "king", "color": "black", "position": "e8"},
            {"type": "bishop", "color": "black", "position": "f8"},
            {"type": "knight", "color": "black", "position": "g8"},
            {"type": "rook", "color": "black", "position": "h8"},
        ],
        [
            {"type": "pawn", "color": "black", "position": "a7"},
            {"type": "pawn", "color": "black", "position": "b7"},
            {"type": "pawn", "color": "black", "position": "c7"},
            {"type": "pawn", "color": "black", "position": "d7"},
            {"type": "pawn", "color": "black", "position": "e7"},
            {"type": "pawn", "color": "black", "position": "f7"},
            {"type": "pawn", "color": "black", "position": "g7"},
            {"type": "pawn", "color": "black", "position": "h7"},
        ],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "f3"},
            None,
            None,
        ],
        [
            {"type": "pawn", "color": "white", "position": "a2"},
            {"type": "pawn", "color": "white", "position": "b2"},
            {"type": "pawn", "color": "white", "position": "c2"},
            {"type": "pawn", "color": "white", "position": "d2"},
            {"type": "pawn", "color": "white", "position": "e2"},
            None,
            {"type": "pawn", "color": "white", "position": "g2"},
            {"type": "pawn", "color": "white", "position": "h2"},
        ],
        [
            {"type": "rook", "color": "white", "position": "a1"},
            {"type": "knight", "color": "white", "position": "b1"},
            {"type": "bishop", "color": "white", "position": "c1"},
            {"type": "queen", "color": "white", "position": "d1"},
            {"type": "king", "color": "white", "position": "e1"},
            {"type": "bishop", "color": "white", "position": "f1"},
            {"type": "knight", "color": "white", "position": "g1"},
            {"type": "rook", "color": "white", "position": "h1"},
        ],
    ]
}
    assert response.json() == expected_board_1

    client.post(f"/game/{game_id}/move?start_pos=e7&end_pos=e5")
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    expected_board_2 = {
    "game_id": game_id,
    "current_player": "white",
    "check_mate_status": "normal",
    "board": [
        [
            {"type": "rook", "color": "black", "position": "a8"},
            {"type": "knight", "color": "black", "position": "b8"},
            {"type": "bishop", "color": "black", "position": "c8"},
            {"type": "queen", "color": "black", "position": "d8"},
            {"type": "king", "color": "black", "position": "e8"},
            {"type": "bishop", "color": "black", "position": "f8"},
            {"type": "knight", "color": "black", "position": "g8"},
            {"type": "rook", "color": "black", "position": "h8"},
        ],
        [
            {"type": "pawn", "color": "black", "position": "a7"},
            {"type": "pawn", "color": "black", "position": "b7"},
            {"type": "pawn", "color": "black", "position": "c7"},
            {"type": "pawn", "color": "black", "position": "d7"},
            None,
            {"type": "pawn", "color": "black", "position": "f7"},
            {"type": "pawn", "color": "black", "position": "g7"},
            {"type": "pawn", "color": "black", "position": "h7"},
        ],
        [None] * 8,
        [
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "black", "position": "e5"},
            None,
            None,
            None,
        ],
        [None] * 8,
        [
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "f3"},
            None,
            None,
        ],
        [
            {"type": "pawn", "color": "white", "position": "a2"},
            {"type": "pawn", "color": "white", "position": "b2"},
            {"type": "pawn", "color": "white", "position": "c2"},
            {"type": "pawn", "color": "white", "position": "d2"},
            {"type": "pawn", "color": "white", "position": "e2"},
            None,
            {"type": "pawn", "color": "white", "position": "g2"},
            {"type": "pawn", "color": "white", "position": "h2"},
        ],
        [
            {"type": "rook", "color": "white", "position": "a1"},
            {"type": "knight", "color": "white", "position": "b1"},
            {"type": "bishop", "color": "white", "position": "c1"},
            {"type": "queen", "color": "white", "position": "d1"},
            {"type": "king", "color": "white", "position": "e1"},
            {"type": "bishop", "color": "white", "position": "f1"},
            {"type": "knight", "color": "white", "position": "g1"},
            {"type": "rook", "color": "white", "position": "h1"},
        ],
    ]
}

    assert response.json() == expected_board_2

    client.post(f"/game/{game_id}/move?start_pos=g2&end_pos=g4")
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    expected_board_3 = {
    "game_id": game_id,
    "current_player": "black",
    "check_mate_status": "normal",
    "board": [
        [
            {"type": "rook", "color": "black", "position": "a8"},
            {"type": "knight", "color": "black", "position": "b8"},
            {"type": "bishop", "color": "black", "position": "c8"},
            {"type": "queen", "color": "black", "position": "d8"},
            {"type": "king", "color": "black", "position": "e8"},
            {"type": "bishop", "color": "black", "position": "f8"},
            {"type": "knight", "color": "black", "position": "g8"},
            {"type": "rook", "color": "black", "position": "h8"},
        ],
        [
            {"type": "pawn", "color": "black", "position": "a7"},
            {"type": "pawn", "color": "black", "position": "b7"},
            {"type": "pawn", "color": "black", "position": "c7"},
            {"type": "pawn", "color": "black", "position": "d7"},
            None,
            {"type": "pawn", "color": "black", "position": "f7"},
            {"type": "pawn", "color": "black", "position": "g7"},
            {"type": "pawn", "color": "black", "position": "h7"},
        ],
        [None] * 8,
        [
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "black", "position": "e5"},
            None,
            None,
            None,
        ],
        [
            None,
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "g4"},
            None,
        ],
        [
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "f3"},
            None,
            None,
        ],
        [
            {"type": "pawn", "color": "white", "position": "a2"},
            {"type": "pawn", "color": "white", "position": "b2"},
            {"type": "pawn", "color": "white", "position": "c2"},
            {"type": "pawn", "color": "white", "position": "d2"},
            {"type": "pawn", "color": "white", "position": "e2"},
            None,
            None,
            {"type": "pawn", "color": "white", "position": "h2"},
        ],
        [
            {"type": "rook", "color": "white", "position": "a1"},
            {"type": "knight", "color": "white", "position": "b1"},
            {"type": "bishop", "color": "white", "position": "c1"},
            {"type": "queen", "color": "white", "position": "d1"},
            {"type": "king", "color": "white", "position": "e1"},
            {"type": "bishop", "color": "white", "position": "f1"},
            {"type": "knight", "color": "white", "position": "g1"},
            {"type": "rook", "color": "white", "position": "h1"},
        ],
    ]
}

    assert response.json() == expected_board_3

    client.post(f"/game/{game_id}/move?start_pos=d8&end_pos=h4")
    response = client.get(f"/game/{game_id}/board")
    assert response.status_code == 200
    expected_board_4 = {
    "game_id": game_id,
    "current_player": "white",
    "check_mate_status": "mate",
    "board": [
        [
            {"type": "rook", "color": "black", "position": "a8"},
            {"type": "knight", "color": "black", "position": "b8"},
            {"type": "bishop", "color": "black", "position": "c8"},
            None,
            {"type": "king", "color": "black", "position": "e8"},
            {"type": "bishop", "color": "black", "position": "f8"},
            {"type": "knight", "color": "black", "position": "g8"},
            {"type": "rook", "color": "black", "position": "h8"},
        ],
        [
            {"type": "pawn", "color": "black", "position": "a7"},
            {"type": "pawn", "color": "black", "position": "b7"},
            {"type": "pawn", "color": "black", "position": "c7"},
            {"type": "pawn", "color": "black", "position": "d7"},
            None,
            {"type": "pawn", "color": "black", "position": "f7"},
            {"type": "pawn", "color": "black", "position": "g7"},
            {"type": "pawn", "color": "black", "position": "h7"},
        ],
        [None] * 8,
        [
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "black", "position": "e5"},
            None,
            None,
            None,
        ],
        [
            None,
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "g4"},
            {"type": "queen", "color": "black", "position": "h4"},
        ],
        [
            None,
            None,
            None,
            None,
            None,
            {"type": "pawn", "color": "white", "position": "f3"},
            None,
            None,
        ],
        [
            {"type": "pawn", "color": "white", "position": "a2"},
            {"type": "pawn", "color": "white", "position": "b2"},
            {"type": "pawn", "color": "white", "position": "c2"},
            {"type": "pawn", "color": "white", "position": "d2"},
            {"type": "pawn", "color": "white", "position": "e2"},
            None,
            None,
            {"type": "pawn", "color": "white", "position": "h2"},
        ],
        [
            {"type": "rook", "color": "white", "position": "a1"},
            {"type": "knight", "color": "white", "position": "b1"},
            {"type": "bishop", "color": "white", "position": "c1"},
            {"type": "queen", "color": "white", "position": "d1"},
            {"type": "king", "color": "white", "position": "e1"},
            {"type": "bishop", "color": "white", "position": "f1"},
            {"type": "knight", "color": "white", "position": "g1"},
            {"type": "rook", "color": "white", "position": "h1"},
        ],
    ]
}

    assert response.json() == expected_board_4
    
def test_get_history_should_return_200OK_and_empty_history(client):
    response = client.post("/game/new")
    assert response.status_code == 200
    game_id = response.json()["game_id"]
    response = client.get(f"/game/{game_id}/history")
    assert response.status_code == 200
    assert response.json() == {"white_moves": [], "black_moves": []}

@patch("uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678"))
def test_get_history_should_return_200OK_and_history_after_moves(mock_uuid, client):
    response = client.post("/game/new")
    assert response.status_code == 200
    game_id = response.json()["game_id"]

    client.post(f"/game/{game_id}/move?start_pos=f2&end_pos=f3")
    client.post(f"/game/{game_id}/move?start_pos=e7&end_pos=e5")
    client.post(f"/game/{game_id}/move?start_pos=g2&end_pos=g4")

    response = client.get(f"/game/{game_id}/history")
    assert response.status_code == 200

    expected_response = {
        "white_moves": [
            "pawn (white, UUID: 12345678-1234-5678-1234-567812345678) von F2 auf F3",
            "pawn (white, UUID: 12345678-1234-5678-1234-567812345678) von G2 auf G4"
        ],
        "black_moves": [
            "pawn (black, UUID: 12345678-1234-5678-1234-567812345678) von E7 auf E5"
        ]
    }

    assert response.json() == expected_response