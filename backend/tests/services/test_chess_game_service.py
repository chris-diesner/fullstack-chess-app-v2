import pytest
import uuid
from unittest.mock import MagicMock
from services.chess_game_service import ChessGameService
from services.chess_board_service import ChessBoardService
from models.chess_game import ChessGame, GameStatus
from models.user import UserLobby, UserInGame, PlayerColor, PlayerStatus

@pytest.fixture
def game_service():
    service = ChessGameService()
    service.game_repo = MagicMock()
    return service

user_lobby_w = UserLobby(user_id="1234", username="Max", color=PlayerColor.WHITE.value, player_status=PlayerStatus.READY.value)
user_lobby_b = UserLobby(user_id="5678", username="Anna", color=PlayerColor.BLACK.value, player_status=PlayerStatus.READY.value)

chess_board_service = ChessBoardService()
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
    