import pytest
import uuid
import copy
from unittest.mock import MagicMock
from services.chess_game_service import ChessGameService
from services.chess_board_service import ChessBoardService
from models.chess_game import ChessGame, GameStatus
from models.user import UserLobby, UserInGame, PlayerColor, PlayerStatus
from models.chess_board import ChessBoard
from models.figure import King, Queen, Knight, Rook, Pawn, FigureColor

@pytest.fixture
def game_service(scope="function"):
    service = ChessGameService()
    service.game_repo = MagicMock()
    return service

user_lobby_w = UserLobby(user_id="1234", username="Max", color=PlayerColor.WHITE.value, player_status=PlayerStatus.READY.value)
user_lobby_b = UserLobby(user_id="5678", username="Anna", color=PlayerColor.BLACK.value, player_status=PlayerStatus.READY.value)

chess_board_service = ChessBoardService()
initialized_board = chess_board_service.initialize_board()

@pytest.fixture(scope="function")
def empty_board():
    return ChessBoard.create_empty_board()

@pytest.fixture(autouse=True)
def reset_game_repo():
    chess_board_service = ChessBoardService()
    global initialized_board
    initialized_board = chess_board_service.initialize_board()


def test_initialize_game(game_service):
    game_id = str(uuid.uuid4())
    
    game_service.game_repo.insert_game.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=initialized_board,
        status=GameStatus.RUNNING
    )
    
    game = game_service.initialize_game(game_id, user_lobby_w, user_lobby_b)
    
    assert game.game_id == game_id
    assert game.player_white == UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[])
    assert game.player_black == UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[])
    assert game.current_turn == "white"
    assert game.status == GameStatus.RUNNING
    assert game.board == game_service.game_repo.insert_game.return_value.board
    game_service.game_repo.insert_game.assert_called_once_with(game)
    
def test_get_game_state_success_should_return_valid_game(game_service):
    game_id = str(uuid.uuid4())
    
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=initialized_board,
        status=GameStatus.RUNNING
    )
    
    game = game_service.get_game_state(game_id)
    
    assert game.game_id == game_id
    assert game.player_white == UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[])
    assert game.player_black == UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[])
    assert game.current_turn == "white"
    assert game.status == GameStatus.RUNNING
    assert game.board == initialized_board
    game_service.game_repo.find_game_by_id.assert_called_once_with(game_id)
    
def test_get_game_state_fail_should_raise_error(game_service):
    game_id = str(uuid.uuid4())
    
    game_service.game_repo.find_game_by_id.return_value = None
    
    with pytest.raises(ValueError) as e:
        game_service.get_game_state(game_id)
        
    assert str(e.value) == "Spiel nicht gefunden."
    
def test_move_figure_should_raise_error_for_empty_square():
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    start_pos = (4, 4)
    end_pos = (5, 0)
    
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=initialized_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Du hast ein leeres Feld ausgewählt!"
    
def test_move_figure_should_raise_error_for_game_already_ended():
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    start_pos = (6, 0)
    end_pos = (5, 0)
    
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=initialized_board,
        status=GameStatus.ENDED
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Spiel ist bereits beendet."
    
def test_move_figure_should_raise_error_for_wrong_turn():
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    start_pos = (6, 0)
    end_pos = (5, 0)
    
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=initialized_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Es ist black's Zug!"

def test_move_figure_should_raise_error_for_non_legal_move():
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    start_pos = (6, 0)
    end_pos = (5, 1)
    
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=initialized_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Ungültiger Zug!"
    
def test_move_figure_should_raise_message_leave_king_in_check(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    white_pawn = Pawn(color=FigureColor.WHITE, position=(6, 0))
    
    test_board.squares[7][4] = white_king
    test_board.squares[6][0] = white_pawn
    
    attaking_pawn = Pawn(color=FigureColor.BLACK, position=(6, 3))
    test_board.squares[6][3] = attaking_pawn
        
    start_pos = (6, 0)
    end_pos = (5, 0)
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Zug nicht möglich! Dein König steht im Schach!"
    
def test_move_figure_should_raise_message_for_unblock_check(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    white_rook = Rook(color=FigureColor.WHITE, position=(6, 4))
    
    test_board.squares[7][4] = white_king
    test_board.squares[6][4] = white_rook
    
    attaking_rook = Rook(color=FigureColor.BLACK, position=(0, 4))
    test_board.squares[0][4] = attaking_rook
        
    start_pos = (6, 4)
    end_pos = (6, 1)
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Zug nicht möglich! Dein König stünde im Schach!"
    
def test_move_figure_should_raise_message_for_moving_king_in_check(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    white_rook = Rook(color=FigureColor.WHITE, position=(6, 4))
    
    test_board.squares[7][4] = white_king
    test_board.squares[6][4] = white_rook
    
    attaking_rook = Rook(color=FigureColor.BLACK, position=(0, 3))
    test_board.squares[0][3] = attaking_rook
        
    start_pos = (7, 4)
    end_pos = (7, 3)
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)
        
    assert str(e.value) == "Zug nicht möglich! Dein König stünde im Schach!"
    
def test_move_figure_should_raise_message_for_check_for_next_current_player(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(7, 4))
    white_rook = Rook(color=FigureColor.WHITE, position=(6, 4))
    
    test_board.squares[7][4] = white_king
    test_board.squares[6][4] = white_rook
    
    attacking_king = King(color=FigureColor.BLACK, position=(0, 3))
    attacking_rook = Rook(color=FigureColor.BLACK, position=(0, 4))
    test_board.squares[0][3] = attacking_king
    test_board.squares[0][4] = attacking_rook
    
    start_pos = (0, 4)
    end_pos = (6, 4)
    
    expected_board = copy.deepcopy(test_board)
    moved_figure = expected_board.squares[start_pos[0]][start_pos[1]]
    expected_board.squares[end_pos[0]][end_pos[1]] = moved_figure
    expected_board.squares[start_pos[0]][start_pos[1]] = None
    moved_figure.position = end_pos
    moved_figure.has_moved = True
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)

    game_service.game_repo.insert_game.assert_called_once()
    
    inserted_game = game_service.game_repo.insert_game.call_args[0][0]
    assert inserted_game.board.squares == expected_board.squares
    assert str(e.value) == "Schach! white ist im Schach!"
    
def test_move_figure_should_raise_message_for_stalemate_number_one(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(6, 1))
    
    test_board.squares[6][1] = white_king
    
    attacking_king = King(color=FigureColor.BLACK, position=(0, 3))
    attacking_rook_1 = Rook(color=FigureColor.BLACK, position=(4, 2))
    attacking_rook_2 = Rook(color=FigureColor.BLACK, position=(7, 7))
    attacking_queen = Queen(color=FigureColor.BLACK, position=(2, 2))
    test_board.squares[0][3] = attacking_king
    test_board.squares[4][2] = attacking_rook_1
    test_board.squares[7][7] = attacking_rook_2
    test_board.squares[2][2] = attacking_queen
    
    start_pos = (2, 2)
    end_pos = (4, 0)
    
    expected_board = copy.deepcopy(test_board)
    moved_figure = expected_board.squares[start_pos[0]][start_pos[1]]
    expected_board.squares[end_pos[0]][end_pos[1]] = moved_figure
    expected_board.squares[start_pos[0]][start_pos[1]] = None
    moved_figure.position = end_pos
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)

    game_service.game_repo.insert_game.assert_called_once()
    
    inserted_game = game_service.game_repo.insert_game.call_args[0][0]
    
    assert inserted_game.board.squares == expected_board.squares
    assert inserted_game.status == GameStatus.ENDED
    
    assert str(e.value) == "Patt! Spiel endet unentschieden!"

def test_move_figure_should_raise_message_for_stalemate_number_two(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(0, 0))
    
    test_board.squares[0][0] = white_king
    
    attacking_king = King(color=FigureColor.BLACK, position=(1, 2))
    attacking_knight = Knight(color=FigureColor.BLACK, position=(4, 3))
    test_board.squares[1][2] = attacking_king
    test_board.squares[4][3] = attacking_knight
    
    start_pos = (4, 3)
    end_pos = (2, 2)
    
    expected_board = copy.deepcopy(test_board)
    moved_figure = expected_board.squares[start_pos[0]][start_pos[1]]
    expected_board.squares[end_pos[0]][end_pos[1]] = moved_figure
    expected_board.squares[start_pos[0]][start_pos[1]] = None
    moved_figure.position = end_pos
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)

    game_service.game_repo.insert_game.assert_called_once()
    
    inserted_game = game_service.game_repo.insert_game.call_args[0][0]
    
    assert inserted_game.board.squares == expected_board.squares
    assert inserted_game.status == GameStatus.ENDED
    
    assert str(e.value) == "Patt! Spiel endet unentschieden!"
    
def test_move_figure_should_raise_message_for_checkmate(empty_board):
    game_service = ChessGameService()
    game_service.game_repo = MagicMock()
    
    game_id = str(uuid.uuid4())
    test_board = empty_board
    white_king = King(color=FigureColor.WHITE, position=(6, 1))
    
    test_board.squares[6][1] = white_king
    
    attacking_king = King(color=FigureColor.BLACK, position=(0, 3))
    attacking_rook_1 = Rook(color=FigureColor.BLACK, position=(6, 2))
    attacking_rook_2 = Rook(color=FigureColor.BLACK, position=(7, 7))
    attacking_queen = Queen(color=FigureColor.BLACK, position=(5, 7))
    test_board.squares[0][3] = attacking_king
    test_board.squares[6][2] = attacking_rook_1
    test_board.squares[7][7] = attacking_rook_2
    test_board.squares[5][7] = attacking_queen
    
    start_pos = (5, 7)
    end_pos = (5, 2)
    
    expected_board = copy.deepcopy(test_board)
    moved_figure = expected_board.squares[start_pos[0]][start_pos[1]]
    expected_board.squares[end_pos[0]][end_pos[1]] = moved_figure
    expected_board.squares[start_pos[0]][start_pos[1]] = None
    moved_figure.position = end_pos
        
    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="black",
        board=test_board,
        status=GameStatus.RUNNING
    )
    
    with pytest.raises(ValueError) as e:
        game_service.move_figure(start_pos, end_pos, game_id)

    game_service.game_repo.insert_game.assert_called_once()
    
    inserted_game = game_service.game_repo.insert_game.call_args[0][0]
    
    assert inserted_game.board.squares == expected_board.squares
    assert inserted_game.status == GameStatus.ENDED
    
    assert str(e.value) == "Schachmatt! black hat gewonnen! white hat verloren!"
    
def test_pawn_promotion_to_queen(game_service, empty_board):
    game_id = str(uuid.uuid4())

    test_board = empty_board
    white_pawn = Pawn(color=FigureColor.WHITE, position=(0, 3))

    test_board.squares[0][3] = white_pawn

    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(
            user_id=user_lobby_w.user_id,
            username=user_lobby_w.username,
            color=PlayerColor.WHITE.value,
            captured_figures=[],
            move_history=[]
        ),
        player_black=UserInGame(
            user_id=user_lobby_b.user_id,
            username=user_lobby_b.username,
            color=PlayerColor.BLACK.value,
            captured_figures=[],
            move_history=[]
        ),
        current_turn="white",
        board=test_board,
        status=GameStatus.RUNNING
    )

    updated_game = game_service.promote_pawn(game_id, (0, 3), "queen")

    assert isinstance(updated_game.board.squares[0][3], Queen)
    
    assert updated_game.board.squares[0][3].id == white_pawn.id

    game_service.game_repo.insert_game.assert_called_once_with(updated_game)

def test_move_figure_should_update_move_history(game_service):
    game_id = str(uuid.uuid4())
    start_pos = (6, 0)
    end_pos = (4, 0)

    initial_board = initialized_board
    updated_board = copy.deepcopy(initial_board)

    moved_figure = updated_board.squares[start_pos[0]][start_pos[1]]
    updated_board.squares[end_pos[0]][end_pos[1]] = moved_figure
    updated_board.squares[start_pos[0]][start_pos[1]] = None
    moved_figure.position = end_pos

    expected_notation = f"{moved_figure.position}{start_pos[1]}{start_pos[0]}{end_pos[1]}{end_pos[0]}"

    game_service.game_repo.find_game_by_id.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=UserInGame(user_id=user_lobby_w.user_id, username=user_lobby_w.username, color=PlayerColor.WHITE.value, captured_figures=[], move_history=[]),
        player_black=UserInGame(user_id=user_lobby_b.user_id, username=user_lobby_b.username, color=PlayerColor.BLACK.value, captured_figures=[], move_history=[]),
        current_turn="white",
        board=initial_board,
        status=GameStatus.RUNNING
    )

    updated_player_white = UserInGame(
        user_id=user_lobby_w.user_id,
        username=user_lobby_w.username,
        color=PlayerColor.WHITE.value,
        captured_figures=[],
        move_history=[expected_notation]
    )

    updated_player_black = UserInGame(
        user_id=user_lobby_b.user_id,
        username=user_lobby_b.username,
        color=PlayerColor.BLACK.value,
        captured_figures=[],
        move_history=[]
    )

    game_service.game_repo.insert_game.return_value = ChessGame(
        game_id=game_id,
        time_stamp_start=MagicMock(),
        player_white=updated_player_white,
        player_black=updated_player_black,
        current_turn="black",
        board=updated_board,
        status=GameStatus.RUNNING
    )

    game = game_service.move_figure(start_pos, end_pos, game_id)

    assert game.game_id == game_id
    assert game.current_turn == "black"
    assert game.status == GameStatus.RUNNING
    assert game.board.squares[end_pos[0]][end_pos[1]] == moved_figure
    assert game.board.squares[start_pos[0]][start_pos[1]] is None
    assert game.board.squares[end_pos[0]][end_pos[1]].position == end_pos

    assert game.player_white.move_history == [expected_notation]
    assert game.player_black.move_history == []
