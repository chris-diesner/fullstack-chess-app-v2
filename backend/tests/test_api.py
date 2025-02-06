import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture
def expected_board():
    return {
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
            [{"type": "pawn", "color": "black", "position": f"{chr(97 + i)}7"} for i in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [{"type": "pawn", "color": "white", "position": f"{chr(97 + i)}2"} for i in range(8)],
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

def test_get_board_should_return_200OK_and_correct_positions(expected_board):
    response = client.get("/game/board")
    
    assert response.status_code == 200
    data = response.json()

    assert len(data["board"]) == 8
    assert all(len(row) == 8 for row in data["board"])

    assert data == expected_board
