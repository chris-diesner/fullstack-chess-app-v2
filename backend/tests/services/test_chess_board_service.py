import pytest
from services.chess_board_service import ChessBoardService
from models.chess_board import ChessBoard
from models.figure import FigureColor, Pawn, Rook, Knight, Bishop, Queen, King

@pytest.fixture
def empty_board():
    return ChessBoard(squares=[[None for _ in range(8)] for _ in range(8)])

def test_create_start_position_success_should_return_created_board():
    chess_board_service = ChessBoardService()
    result = chess_board_service.create_start_position()

    assert len(result) == 8
    assert all(len(row) == 8 for row in result)

    expected_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    for col, figure in enumerate(expected_row):
        assert isinstance(result[0][col], figure) and result[0][col].color == FigureColor.BLACK

    for col, figure in enumerate(expected_row):
        assert isinstance(result[7][col], figure) and result[7][col].color == FigureColor.WHITE

    for col in range(8):
        assert isinstance(result[1][col], Pawn) and result[1][col].color == FigureColor.BLACK
        assert isinstance(result[6][col], Pawn) and result[6][col].color == FigureColor.WHITE

def test_initialize_board_success_should_return_list_of_list_board():
    chess_board_service = ChessBoardService()
    chess_board_service.initialize_board()
    assert chess_board_service.board.squares == chess_board_service.create_start_position()