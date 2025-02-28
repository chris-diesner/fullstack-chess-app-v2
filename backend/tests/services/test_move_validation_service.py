import pytest
from services.move_validation_service import MoveValidationService
from models.chess_board import ChessBoard
from models.figure import FigureColor, Pawn, Rook, Bishop, King, Queen, Knight

@pytest.fixture
def empty_board():
    return ChessBoard(squares=[[None for _ in range(8)] for _ in range(8)])

def test_is_within_board_should_return_true_for_within_board_or_false_for_out_board():
    assert MoveValidationService.is_within_board((0, 0)) is True
    assert MoveValidationService.is_within_board((7, 7)) is True
    assert MoveValidationService.is_within_board((8, 8)) is False
    assert MoveValidationService.is_within_board((-1, 0)) is False
    assert MoveValidationService.is_within_board((0, -8)) is False

def test_is_move_valid_pawn_should_return_true_for_valid_moves(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (4, 0), empty_board) is True

    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (3, 0), empty_board) is True

def test_is_move_valid_pawn_should_return_false_for_invalid_moves(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (6, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (1, 1), empty_board) is False

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (7, 0), empty_board) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (0, 0), empty_board) is False

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board) is False

def test_is_move_valid_pawn_should_return_true_for_valid_capture(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    empty_board.squares[5][1] = Pawn(color="black", position=(5, 1))
    empty_board.squares[2][1] = Pawn(color="white", position=(2, 1))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board) is True
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board) is True

def test_is_move_valid_pawn_should_return_false_for_invalid_capture_own_color(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    empty_board.squares[5][1] = Pawn(color="white", position=(5, 1))
    empty_board.squares[2][1] = Pawn(color="black", position=(2, 1))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board) is False

def test_is_move_valid_rook_should_return_true_for_valid_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (4, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (7, 7), empty_board) is True

    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 4), empty_board) is True
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (6, 0), empty_board) is True
    
def test_is_move_valid_rook_should_return_false_for_invalid_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (0, 7), empty_board) is False
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (5, 3), empty_board) is False

    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (7, 7), empty_board) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (2, 4), empty_board) is False
    
def test_is_move_valid_rook_should_return_false_for_blocked_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    empty_board.squares[6][0] = Pawn(color="black", position=(6, 0))
    empty_board.squares[0][2] = Rook(color="white", position=(0, 2))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (4, 0), empty_board) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 4), empty_board) is False

def test_is_move_valid_rook_should_return_true_for_capture_enemy(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))

    empty_board.squares[6][0] = Pawn(color=FigureColor.BLACK, position=(6, 0))
    empty_board.squares[0][2] = Rook(color=FigureColor.WHITE, position=(0, 2))

    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (6, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 2), empty_board) 
    
def test_is_move_valid_rook_should_return_false_for_capture_own_color(empty_board):
    white_rook = Rook(color="white", position=(6, 0))
    black_rook = Rook(color="black", position=(1, 0))
    
    empty_board.squares[6][0] = Pawn(color="white", position=(6, 0))
    empty_board.squares[0][2] = Rook(color="black", position=(0, 2))

    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (6, 0), empty_board) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 2), empty_board) is False
    
def test_is_move_valid_bishop_should_return_true_for_valid_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 4), empty_board) is True
    
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 3), empty_board) is True
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 7), empty_board) is True
    
def test_is_move_valid_bishop_should_return_false_for_invalid_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 2), empty_board) is False
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (7, 7), empty_board) is False
    
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 5), empty_board) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (0, 0), empty_board) is False
    
def test_is_move_valid_bishop_should_return_false_for_blocked_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="black", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 0), empty_board) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 3), empty_board) is False
    
def test_is_move_valid_bishop_should_return_true_for_capture_enemy(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="black", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (6, 1), empty_board) is True
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (1, 4), empty_board) is True
    
def test_is_move_valid_bishop_should_return_false_for_capture_own_color(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="white", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="black", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (6, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (1, 4), empty_board) is False
    
def test_is_move_valid_king_should_return_true_for_valid_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board) is True
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (7, 5), empty_board) is True
    
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board) is True
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (0, 3), empty_board) is True
    
def test_is_move_valid_king_should_return_false_for_invalid_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (7, 6), empty_board) is False
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 6), empty_board) is False
    
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (0, 6), empty_board) is False
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 6), empty_board) is False
    
def test_is_move_valid_king_should_return_true_for_valid_capture_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[6][4] = Pawn(color="black", position=(6, 4))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board) is True
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board) is True
    
def test_is_move_valid_king_should_return_false_for_invalid_capture_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[6][4] = Pawn(color="white", position=(6, 4))
    empty_board.squares[1][4] = Rook(color="black", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board) is False
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board) is False
    
def test_is_move_valid_queen_should_return_true_for_valid_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 3), empty_board) is True
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (7, 7), empty_board) is True
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (3, 7), empty_board) is True
    
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (2, 3), empty_board) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (0, 7), empty_board) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (4, 7), empty_board) is True
    
def test_is_move_valid_queen_should_return_false_for_invalid_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 2), empty_board) is False
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 6), empty_board) is False
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (3, 6), empty_board) is False
    
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (2, 2), empty_board) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 6), empty_board) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (4, 6), empty_board) is False
    
def test_is_move_valid_queen_should_return_false_for_blocked_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 3), empty_board) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (3, 3), empty_board) is False
    
def test_is_move_valid_queen_should_return_true_for_capture_enemy(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 3), empty_board) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 3), empty_board) is True

def test_is_move_valid_queen_should_return_false_for_capture_own_color(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="white", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="black", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 3), empty_board) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 3), empty_board) is False
    
def test_is_move_valid_knight_should_return_true_for_valid_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 2), empty_board) is True
    
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 0), empty_board) is True
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 2), empty_board) is True
    
def test_is_move_valid_knight_should_return_false_for_invalid_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (7, 7), empty_board) is False
    
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 1), empty_board) is False
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (0, 7), empty_board) is False
    
def test_is_move_valid_knight_should_return_true_for_valid_capture_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (6, 3), empty_board) is True
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (1, 3), empty_board) is True
    
def test_is_move_valid_knight_should_return_false_for_invalid_capture_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    empty_board.squares[6][3] = Pawn(color="white", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="black", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (6, 3), empty_board) is False
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (1, 3), empty_board) is False
    