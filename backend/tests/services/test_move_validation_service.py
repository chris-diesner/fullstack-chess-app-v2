import pytest
from services.move_validation_service import MoveValidationService
from models.chess_game import ChessGame
from models.user import UserInGame, PlayerColor
from models.chess_board import ChessBoard
from models.figure import FigureColor, Pawn, Rook, Bishop, King, Queen, Knight

@pytest.fixture
def empty_board():
    return ChessBoard(squares=[[None for _ in range(8)] for _ in range(8)])

@pytest.fixture
def test_game(empty_board):
    return ChessGame(
        game_id="1234",
        time_stamp_start="2021-08-01T12:00:00",
        player_white=UserInGame(
            user_id="test_user1",
            username="test_user1",
            color=PlayerColor.WHITE.value,
            captured_figures=[],
            move_history=[]
        ),
        player_black=UserInGame(
            user_id="test_user2",
            username="test_user2",
            color=PlayerColor.BLACK.value,
            captured_figures=[],
            move_history=[]
        ),
        current_turn=FigureColor.WHITE.value,
        board=empty_board,
        status="running"
    )

def test_is_within_board_should_return_true_for_within_board_or_false_for_out_board():
    assert MoveValidationService.is_within_board((0, 0)) is True
    assert MoveValidationService.is_within_board((7, 7)) is True
    assert MoveValidationService.is_within_board((8, 8)) is False
    assert MoveValidationService.is_within_board((-1, 0)) is False
    assert MoveValidationService.is_within_board((0, -8)) is False

def test_is_move_valid_pawn_should_return_true_for_valid_moves(empty_board, test_game):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (4, 0), empty_board, test_game) is True

    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (3, 0), empty_board, test_game) is True

def test_is_move_valid_pawn_should_return_false_for_invalid_moves(empty_board, test_game):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (6, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (1, 1), empty_board, test_game) is False

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (7, 0), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (0, 0), empty_board, test_game) is False

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board, test_game) is False

def test_is_move_valid_pawn_should_return_true_for_valid_capture(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    empty_board.squares[5][1] = Pawn(color="black", position=(5, 1))
    empty_board.squares[2][1] = Pawn(color="white", position=(2, 1))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board, test_game) is True

def test_is_move_valid_pawn_should_return_false_for_invalid_capture_own_color(empty_board):
    white_pawn = Pawn(color="white", position=(6, 0))
    black_pawn = Pawn(color="black", position=(1, 0))

    empty_board.squares[5][1] = Pawn(color="white", position=(5, 1))
    empty_board.squares[2][1] = Pawn(color="black", position=(2, 1))

    assert MoveValidationService.is_move_valid(white_pawn, (6, 0), (5, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_pawn, (1, 0), (2, 1), empty_board, test_game) is False

def test_is_move_valid_rook_should_return_true_for_valid_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (4, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (7, 7), empty_board, test_game) is True

    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 4), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (6, 0), empty_board, test_game) is True
    
def test_is_move_valid_rook_should_return_false_for_invalid_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (0, 7), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (5, 3), empty_board, test_game) is False

    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (7, 7), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (2, 4), empty_board, test_game) is False
    
def test_is_move_valid_rook_should_return_false_for_blocked_moves(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))
    
    empty_board.squares[6][0] = Pawn(color="black", position=(6, 0))
    empty_board.squares[0][2] = Rook(color="white", position=(0, 2))
    
    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (4, 0), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 4), empty_board, test_game) is False

def test_is_move_valid_rook_should_return_true_for_capture_enemy(empty_board):
    white_rook = Rook(color=FigureColor.WHITE, position=(7, 0))
    black_rook = Rook(color=FigureColor.BLACK, position=(0, 0))

    empty_board.squares[6][0] = Pawn(color=FigureColor.BLACK, position=(6, 0))
    empty_board.squares[0][2] = Rook(color=FigureColor.WHITE, position=(0, 2))

    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (6, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 2), empty_board, test_game) is True
    
def test_is_move_valid_rook_should_return_false_for_capture_own_color(empty_board):
    white_rook = Rook(color="white", position=(6, 0))
    black_rook = Rook(color="black", position=(1, 0))
    
    empty_board.squares[6][0] = Pawn(color="white", position=(6, 0))
    empty_board.squares[0][2] = Rook(color="black", position=(0, 2))

    assert MoveValidationService.is_move_valid(white_rook, (7, 0), (6, 0), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_rook, (0, 0), (0, 2), empty_board, test_game) is False
    
def test_is_move_valid_bishop_should_return_true_for_valid_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 4), empty_board, test_game) is True
    
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 3), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 7), empty_board, test_game) is True
    
def test_is_move_valid_bishop_should_return_false_for_invalid_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 2), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (7, 7), empty_board, test_game) is False
    
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 5), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (0, 0), empty_board, test_game) is False
    
def test_is_move_valid_bishop_should_return_false_for_blocked_moves(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="black", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (5, 0), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (2, 3), empty_board, test_game) is False
    
def test_is_move_valid_bishop_should_return_true_for_capture_enemy(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="black", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (6, 1), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (1, 4), empty_board, test_game) is True
    
def test_is_move_valid_bishop_should_return_false_for_capture_own_color(empty_board):
    white_bishop = Bishop(color=FigureColor.WHITE, position=(7, 2))
    black_bishop = Bishop(color=FigureColor.BLACK, position=(0, 5))
    
    empty_board.squares[6][1] = Pawn(color="white", position=(6, 1))
    empty_board.squares[1][4] = Rook(color="black", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_bishop, (7, 2), (6, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_bishop, (0, 5), (1, 4), empty_board, test_game) is False
    
def test_is_move_valid_king_should_return_true_for_valid_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (7, 5), empty_board, test_game) is True
    
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (0, 3), empty_board, test_game) is True
    
def test_is_move_valid_king_should_return_false_for_invalid_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (7, 6), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 6), empty_board, test_game) is False
    
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (0, 6), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 6), empty_board, test_game) is False
    
def test_is_move_valid_king_should_return_true_for_valid_capture_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[6][4] = Pawn(color="black", position=(6, 4))
    empty_board.squares[1][4] = Rook(color="white", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board, test_game) is True
    
def test_is_move_valid_king_should_return_false_for_invalid_capture_moves(empty_board):
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[6][4] = Pawn(color="white", position=(6, 4))
    empty_board.squares[1][4] = Rook(color="black", position=(1, 4))
    
    assert MoveValidationService.is_move_valid(white_king, (7, 4), (6, 4), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_king, (0, 4), (1, 4), empty_board, test_game) is False
    
def test_is_move_valid_queen_should_return_true_for_valid_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 3), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (7, 7), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (3, 7), empty_board, test_game) is True
    
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (2, 3), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (0, 7), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (4, 7), empty_board, test_game) is True
    
def test_is_move_valid_queen_should_return_false_for_invalid_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 2), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 6), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (3, 6), empty_board, test_game) is False
    
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (2, 2), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 6), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (4, 6), empty_board, test_game) is False
    
def test_is_move_valid_queen_should_return_false_for_blocked_moves(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (5, 3), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (3, 3), empty_board, test_game) is False
    
def test_is_move_valid_queen_should_return_true_for_capture_enemy(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 3), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 3), empty_board, test_game) is True

def test_is_move_valid_queen_should_return_false_for_capture_own_color(empty_board):
    white_queen = Queen(color=FigureColor.WHITE, position=(7, 3))
    black_queen = Queen(color=FigureColor.BLACK, position=(0, 3))
    
    empty_board.squares[6][3] = Pawn(color="white", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="black", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_queen, (7, 3), (6, 3), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_queen, (0, 3), (1, 3), empty_board, test_game) is False
    
def test_is_move_valid_knight_should_return_true_for_valid_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 2), empty_board, test_game) is True
    
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 0), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 2), empty_board, test_game) is True
    
def test_is_move_valid_knight_should_return_false_for_invalid_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (5, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (7, 7), empty_board, test_game) is False
    
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (2, 1), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (0, 7), empty_board, test_game) is False
    
def test_is_move_valid_knight_should_return_true_for_valid_capture_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    empty_board.squares[6][3] = Pawn(color="black", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="white", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (6, 3), empty_board, test_game) is True
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (1, 3), empty_board, test_game) is True
    
def test_is_move_valid_knight_should_return_false_for_invalid_capture_moves(empty_board):
    white_knight = Knight(color=FigureColor.WHITE, position=(7, 1))
    black_knight = Knight(color=FigureColor.BLACK, position=(0, 1))
    
    empty_board.squares[6][3] = Pawn(color="white", position=(6, 3))
    empty_board.squares[1][3] = Rook(color="black", position=(1, 3))
    
    assert MoveValidationService.is_move_valid(white_knight, (7, 1), (6, 3), empty_board, test_game) is False
    assert MoveValidationService.is_move_valid(black_knight, (0, 1), (1, 3), empty_board, test_game) is False
    
def test_is_king_in_check_should_return_true_and_list_of_attacker(empty_board, test_game):
    test_game.current_turn = FigureColor.WHITE.value

    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))

    empty_board.squares[7][4] = white_king
    empty_board.squares[0][4] = black_king

    attacking_pawn = Pawn(color=FigureColor.BLACK, position=(6, 3))
    attacking_rook = Rook(color=FigureColor.BLACK, position=(3, 4))

    empty_board.squares[6][3] = attacking_pawn
    empty_board.squares[3][4] = attacking_rook

    is_check_white, attackers_black = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_white is True
    assert (attacking_pawn, (6, 3)) in attackers_black
    assert (attacking_rook, (3, 4)) in attackers_black
    assert len(attackers_black) == 2

    test_game.current_turn = FigureColor.BLACK.value
    
    attacking_pawn = Pawn(color=FigureColor.WHITE, position=(1, 3))
    attacking_rook = Rook(color=FigureColor.WHITE, position=(3, 4))
    
    empty_board.squares[1][3] = attacking_pawn
    empty_board.squares[3][4] = attacking_rook

    is_check_black, attackers_white = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_black is True
    assert (attacking_pawn, (1, 3)) in attackers_white
    assert (attacking_rook, (3, 4)) in attackers_white
    assert len(attackers_white) == 2
    
def test_is_king_in_check_should_return_false_and_empty_list(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[7][4] = white_king
    empty_board.squares[0][4] = black_king
    
    is_check_white, attackers_white = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_white is False
    assert attackers_white == []
    
    test_game.current_turn = FigureColor.BLACK.value
    
    is_check_black, attackers_black = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_black is False
    assert attackers_black == []
    
def test_get_positions_between_should_return_list_of_positions_between_start_and_end():
    start = (0, 0)
    end = (7, 7)
    
    positions = MoveValidationService.get_positions_between(start, end)
    assert positions == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    
    start = (7, 7)
    end = (0, 0)
    
    positions = MoveValidationService.get_positions_between(start, end)
    assert positions == [(6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]
    
    start = (0, 7)
    end = (7, 0)
    
    positions = MoveValidationService.get_positions_between(start, end)
    assert positions == [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]
    
    start = (7, 0)
    end = (0, 7)
    
    positions = MoveValidationService.get_positions_between(start, end)
    assert positions == [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)]
    
def test_simulate_move_and_check_should_return_true_for_check(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[7][4] = white_king
    empty_board.squares[0][4] = black_king
    
    attacking_queen = Queen(color=FigureColor.BLACK, position=(6, 4))
    attacking_rook = Rook(color=FigureColor.BLACK, position=(3, 4))
    
    empty_board.squares[6][4] = attacking_queen
    empty_board.squares[3][4] = attacking_rook
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (7, 4), (6, 4))
    assert simulate_move is True
    
    test_game.current_turn = FigureColor.BLACK.value
    
    attacking_queen = Queen(color=FigureColor.WHITE, position=(1, 4))
    attacking_rook = Rook(color=FigureColor.WHITE, position=(3, 4))
    
    empty_board.squares[1][4] = attacking_queen
    empty_board.squares[3][4] = attacking_rook
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (0, 4), (1, 4))
    assert simulate_move is True
    
    test_game.current_turn = FigureColor.WHITE.value
    
    attacking_queen = Queen(color=FigureColor.BLACK, position=(3, 5))
    
    empty_board.squares[3][5] = attacking_queen
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (7, 4), (7, 5))
    assert simulate_move is True
    
    test_game.current_turn = FigureColor.BLACK.value	
    
    attacking_queen = Queen(color=FigureColor.WHITE, position=(3, 3))
    
    empty_board.squares[3][3] = attacking_queen
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (0, 4), (0, 3))
    assert simulate_move is True
    
def test_simulate_move_and_check_should_return_false_for_possible_escape(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[7][4] = white_king
    empty_board.squares[0][4] = black_king
    
    attacking_queen = Queen(color=FigureColor.BLACK, position=(6, 4))
    
    empty_board.squares[6][4] = attacking_queen
    
    is_check_white, attackers_black = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_white is True
    assert (attacking_queen, (6, 4)) in attackers_black
    assert len(attackers_black) == 1
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (7, 4), (6, 4))
    assert simulate_move is False
    
    test_game.current_turn = FigureColor.BLACK.value
    
    attacking_queen = Queen(color=FigureColor.WHITE, position=(5, 4))
    
    empty_board.squares[5][4] = attacking_queen
    
    is_check_black, attackers_white = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_black is True
    assert (attacking_queen, (5, 4)) in attackers_white
    assert len(attackers_white) == 1
    
    simulate_move = MoveValidationService.simulate_move_and_check(test_game, empty_board, (0, 4), (1, 3))
    assert simulate_move is False
    
def test_is_king_checkmate_should_return_true_for_no_possible_moves_and_one_covered_attacker(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    black_king = King(color=FigureColor.BLACK, position=(0, 4))
    
    empty_board.squares[7][4] = white_king
    empty_board.squares[0][4] = black_king
    
    attacking_queen = Queen(color=FigureColor.BLACK, position=(6, 4))
    attacking_rook = Rook(color=FigureColor.BLACK, position=(3, 4))
    
    empty_board.squares[6][4] = attacking_queen
    empty_board.squares[3][4] = attacking_rook
    
    is_check_white, attackers_black = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_white is True
    assert (attacking_queen, (6, 4)) in attackers_black
    assert len(attackers_black) == 1
    
    is_checkmate_white = MoveValidationService.is_king_checkmate(test_game, empty_board)
    assert is_checkmate_white is True
    
    test_game.current_turn = FigureColor.BLACK.value
    
    attacking_queen = Queen(color=FigureColor.WHITE, position=(1, 4))
    attacking_rook = Rook(color=FigureColor.WHITE, position=(3, 4))
    
    empty_board.squares[1][4] = attacking_queen
    empty_board.squares[3][4] = attacking_rook
    
    is_check_black, attackers_white = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_black is True
    assert (attacking_queen, (1, 4)) in attackers_white
    assert len(attackers_white) == 1
    
    is_checkmate_black = MoveValidationService.is_king_checkmate(test_game, empty_board)
    assert is_checkmate_black is True
    
def test_is_king_checkmate_should_return_false_for_no_legal_king_moves_but_possible_blocker(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(7, 0))
    white_rook = Rook(color=FigureColor.WHITE, position=(6, 7))
    
    empty_board.squares[7][0] = white_king
    empty_board.squares[6][7] = white_rook
    
    attacking_queen = Queen(color=FigureColor.BLACK, position=(4, 0))
    passive_rook_1 = Rook(color=FigureColor.BLACK, position=(4, 1))
    passive_rook_2 = Rook(color=FigureColor.BLACK, position=(4, 2))
    
    empty_board.squares[4][0] = attacking_queen
    empty_board.squares[4][1] = passive_rook_1
    empty_board.squares[4][2] = passive_rook_2
    
    is_check_white, attackers_black = MoveValidationService.is_king_in_check(test_game, empty_board)
    assert is_check_white is True
    assert (attacking_queen, (4, 0)) in attackers_black
    assert len(attackers_black) == 1
    
    is_checkmate_white = MoveValidationService.is_king_checkmate(test_game, empty_board)
    assert is_checkmate_white is False
    
def test_is_stalemate_should_return_true_for_no_legal_moves_and_no_check(empty_board):
    test_game.current_turn = FigureColor.WHITE.value
    
    white_king = King(color=FigureColor.WHITE, position=(0, 0))
    black_king = King(color=FigureColor.BLACK, position=(1, 2))
    black_knight = Knight(color=FigureColor.BLACK, position=(2, 2))
    
    empty_board.squares[0][0] = white_king
    empty_board.squares[1][2] = black_king
    empty_board.squares[2][2] = black_knight
    
    is_stalemate = MoveValidationService.is_stalemate(test_game, empty_board)
    assert is_stalemate is True
    
def test_is_valid_castling_should_return_true_for_valid_castling(empty_board, test_game):
    white_king = King(color=FigureColor.WHITE, position=(7, 4), has_moved=False)
    white_rook_kingside = Rook(color=FigureColor.WHITE, position=(7, 7), has_moved=False)

    empty_board.squares[7][4] = white_king
    empty_board.squares[7][7] = white_rook_kingside

    assert MoveValidationService.is_valid_castling(white_king, (7, 4), (7, 6), empty_board, test_game) is True

    white_rook_queenside = Rook(color=FigureColor.WHITE, position=(7, 0), has_moved=False)
    empty_board.squares[7][0] = white_rook_queenside

    assert MoveValidationService.is_valid_castling(white_king, (7, 4), (7, 2), empty_board, test_game) is True

    black_king = King(color=FigureColor.BLACK, position=(0, 4), has_moved=False)
    black_rook_kingside = Rook(color=FigureColor.BLACK, position=(0, 7), has_moved=False)

    empty_board.squares[0][4] = black_king
    empty_board.squares[0][7] = black_rook_kingside

    assert MoveValidationService.is_valid_castling(black_king, (0, 4), (0, 6), empty_board, test_game) is True

    black_rook_queenside = Rook(color=FigureColor.BLACK, position=(0, 0), has_moved=False)
    empty_board.squares[0][0] = black_rook_queenside

    assert MoveValidationService.is_valid_castling(black_king, (0, 4), (0, 2), empty_board, test_game) is True

def test_is_valid_castling_should_return_false_for_invalid_castling(empty_board, test_game):
    moved_king = King(color=FigureColor.WHITE, position=(7, 4), has_moved=True)
    unmoved_rook = Rook(color=FigureColor.WHITE, position=(7, 7), has_moved=False)

    empty_board.squares[7][4] = moved_king
    empty_board.squares[7][7] = unmoved_rook

    assert MoveValidationService.is_valid_castling(moved_king, (7, 4), (7, 6), empty_board, test_game) is False

    unmoved_king = King(color=FigureColor.WHITE, position=(7, 4), has_moved=False)
    moved_rook = Rook(color=FigureColor.WHITE, position=(7, 7), has_moved=True)

    empty_board.squares[7][4] = unmoved_king
    empty_board.squares[7][7] = moved_rook

    assert MoveValidationService.is_valid_castling(unmoved_king, (7, 4), (7, 6), empty_board, test_game) is False

    blocking_piece = Knight(color=FigureColor.WHITE, position=(7, 5))
    empty_board.squares[7][4] = unmoved_king
    empty_board.squares[7][7] = unmoved_rook
    empty_board.squares[7][5] = blocking_piece

    assert MoveValidationService.is_valid_castling(unmoved_king, (7, 4), (7, 6), empty_board, test_game) is False

    attacking_queen = Queen(color=FigureColor.BLACK, position=(5, 4))
    empty_board.squares[7][5] = None 
    empty_board.squares[5][4] = attacking_queen

    assert MoveValidationService.is_valid_castling(unmoved_king, (7, 4), (7, 6), empty_board, test_game) is False

    attacking_rook = Rook(color=FigureColor.BLACK, position=(5, 5))
    empty_board.squares[5][4] = None
    empty_board.squares[5][5] = attacking_rook

    assert MoveValidationService.is_valid_castling(unmoved_king, (7, 4), (7, 6), empty_board, test_game) is False

def test_is_valid_en_passant_should_return_true_for_valid_en_passant(empty_board, test_game):
    white_pawn = Pawn(color=FigureColor.WHITE, position=(4, 3))
    black_pawn = Pawn(color=FigureColor.BLACK, position=(4, 2))

    empty_board.squares[4][3] = white_pawn
    empty_board.squares[4][2] = black_pawn

    test_game.last_move = {
        "figure": black_pawn,
        "start": (6, 2),
        "end": (4, 2),
        "two_square_pawn_move": True
    }

    assert MoveValidationService.is_valid_en_passant(white_pawn, (4, 3), (5, 2), empty_board, test_game) is True

def test_is_valid_en_passant_should_return_false_for_invalid_en_passant(empty_board, test_game):
    white_pawn = Pawn(color=FigureColor.WHITE, position=(4, 3))
    black_pawn = Pawn(color=FigureColor.BLACK, position=(4, 2))

    empty_board.squares[4][3] = white_pawn
    empty_board.squares[4][2] = black_pawn

    test_game.last_move = {
        "figure": Knight(color=FigureColor.BLACK, position=(6, 2)),
        "start": (6, 2),
        "end": (4, 1),
        "two_square_pawn_move": False
    }

    assert MoveValidationService.is_valid_en_passant(white_pawn, (4, 3), (5, 2), empty_board, test_game) is False
