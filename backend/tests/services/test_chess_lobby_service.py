import pytest
from services.chess_lobby_service import ChessLobbyService
from repositories.chess_game_repo import ChessGameRepository
from models.lobby import Lobby, UserLobby
from models.user import UserLobby, PlayerColor, PlayerStatus
from models.chess_game import ChessGame, GameStatus

@pytest.fixture
def lobby_service():
    return ChessLobbyService()

user_create_1 = UserLobby(user_id="1234", username="Max", color=None, status="not_ready")
user_create_2 = UserLobby(user_id="5678", username="Anna", color=None, status="not_ready")
user_create_3 = UserLobby(user_id="9012", username="Fritz", color=None, status="not_ready")

def test_create_lobby_success_should_return_lobby_with_user(lobby_service):
    response = lobby_service.create_lobby(user_create_1)

    assert response.game_id in lobby_service.game_lobbies
    assert response.players[0].user_id == "1234"
    assert response.players[0].username == "Max"
    assert response.players[0].color is None
    assert response.players[0].status.value == "not_ready"

def test_create_lobby_fail_already_created_a_lobby(lobby_service):
    lobby_service.create_lobby(user_create_1)
    
    try:
        response = lobby_service.create_lobby(user_create_1)
    except ValueError as e:
        response = str(e)
    
    assert response == "Du hast bereits eine Lobby erstellt. Du darfst aber gerne einer anderen beitreten."
        
def test_list_lobbies_empty_should_return_empty_dict(lobby_service):
    response = lobby_service.list_lobbies()

    assert "lobbies" in response
    assert len(response["lobbies"]) == 0

def test_list_lobbies_with_lobbies_should_return_lobbies_with_users(lobby_service):
    lobby_service.create_lobby(user_create_1)
    lobby_service.create_lobby(user_create_2)

    response = lobby_service.list_lobbies()

    assert "lobbies" in response
    assert len(response["lobbies"]) == 2

    assert response["lobbies"][0]["game_id"] != response["lobbies"][1]["game_id"]
    
    assert response["lobbies"][0]["players"][0]["user_id"] == "1234"
    assert response["lobbies"][0]["players"][0]["username"] == "Max"

    assert response["lobbies"][1]["players"][0]["user_id"] == "5678"
    assert response["lobbies"][1]["players"][0]["username"] == "Anna"

@pytest.mark.asyncio
async def test_join_lobby_success_should_return_existing_lobby_with_joined_player(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    response = await lobby_service.join_lobby(game_id, user_create_2)

    assert response.game_id == game_id
    assert len(response.players) == 2
    assert response.players[0].user_id == "1234"
    assert response.players[1].user_id == "5678"
    assert response.players[0].username == "Max"
    assert response.players[1].username == "Anna"
    assert response.players[0].color == None
    assert response.players[1].color == None
    assert response.players[0].status.value == "not_ready"
    assert response.players[1].status.value == "not_ready"
    
@pytest.mark.asyncio
async def test_join_lobby_fail_not_found(lobby_service):
    lobby_service.create_lobby(user_create_1)
    
    try:
        response = await lobby_service.join_lobby("1234", user_create_2)
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby existiert nicht."
    
@pytest.mark.asyncio
async def test_join_lobby_fail_already_in_lobby(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    try:
        response = await lobby_service.join_lobby(game_id, user_create_1)
    except ValueError as e:
        response = str(e)
    
    assert response == "Du bist bereits in dieser Lobby."
    
@pytest.mark.asyncio
async def test_join_lobby_fail_lobby_full(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    await lobby_service.join_lobby(game_id, user_create_2)
    try:
        response = await lobby_service.join_lobby(game_id, user_create_3)
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby ist bereits voll."
    
@pytest.mark.asyncio
async def test_leave_lobby_success_should_return_lobby_for_other_player_in_lobby(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    await lobby_service.join_lobby(game_id, user_create_2)
    
    assert len(lobby_service.game_lobbies[game_id].players) == 2
    assert lobby_service.game_lobbies[game_id].players[0].user_id == "1234"
    assert lobby_service.game_lobbies[game_id].players[1].user_id == "5678"
    
    response = await lobby_service.leave_lobby(game_id, user_create_1.user_id)

    assert response.game_id == game_id
    assert len(response.players) == 1
    assert response.players[0].user_id == "5678"
    assert response.players[0].username == "Anna"
    assert response.players[0].color == None
    assert response.players[0].status.value == "not_ready"
    
@pytest.mark.asyncio
async def test_leave_lobby_success_should_return_none_for_empty_lobby(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    
    assert len(lobby_service.game_lobbies[game_id].players) == 1
    assert lobby_service.game_lobbies[game_id].players[0].user_id == "1234"
    
    response = await lobby_service.leave_lobby(game_id, user_create_1.user_id)

    assert response == None
    assert game_id not in lobby_service.game_lobbies
    
@pytest.mark.asyncio
async def test_leave_lobby_fail_not_found(lobby_service):
    try:
        response = await lobby_service.leave_lobby("1234", user_create_2.user_id)
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby nicht gefunden, oder bereits gelöscht."
    
@pytest.mark.asyncio
async def test_leave_lobby_fail_not_in_lobby(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    
    try:
        response = await lobby_service.leave_lobby(lobby.game_id, user_create_2.user_id)
    except ValueError as e:
        response = str(e)
    
    assert response == "Du bist nicht mehr in dieser Lobby."
    
@pytest.mark.asyncio
async def test_set_player_color_success_should_return_lobby_with_updated_player(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    user_id = lobby.players[0].user_id
    
    response = await lobby_service.set_player_color(game_id, user_id, "white")
    
    assert response.game_id == game_id
    assert response.players[0].user_id == user_id
    assert response.players[0].color == "white"
    
@pytest.mark.asyncio
async def test_set_player_color_fail_lobby_not_found(lobby_service):
    try:
        response = await lobby_service.set_player_color("1234", user_create_1.user_id, "white")
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby nicht gefunden."
    
@pytest.mark.asyncio
async def test_set_player_color_fail_player_not_found(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    
    try:
        response = await lobby_service.set_player_color(game_id, "5678", "white")
    except ValueError as e:
        response = str(e)
        
    assert response == "Spieler nicht gefunden."
    
@pytest.mark.asyncio
async def test_set_player_color_fail_color_already_taken(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    lobby.players.append(user_create_2)
    
    lobby = await lobby_service.set_player_color(game_id, user_create_1.user_id, "white")
    try:
        response = await lobby_service.set_player_color(game_id, user_create_2.user_id, "white")
    except ValueError as e:
        response = str(e)
        
    assert response == "Farbe bereits vergeben."
    
@pytest.mark.asyncio
async def test_set_player_status_success_should_return_new_status(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    user_id = lobby.players[0].user_id
    await lobby_service.set_player_color(game_id, user_create_1.user_id, "white")
    
    response = await lobby_service.set_player_status(game_id, user_create_1.user_id, "ready")
    
    assert response.game_id == game_id
    assert response.players[0].user_id == user_id
    assert response.players[0].color == "white"
    assert response.players[0].status == "ready"
    
@pytest.mark.asyncio
async def test_set_player_status_fail_lobby_not_found(lobby_service):
    try:
        response = await lobby_service.set_player_status("1234", user_create_1.user_id, "white")
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby nicht gefunden."
    
@pytest.mark.asyncio
async def test_set_player_status_fail_player_not_found(lobby_service):
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    
    try:
        response = await lobby_service.set_player_status(game_id, "5678", "white")
    except ValueError as e:
        response = str(e)
        
    assert response == "Spieler nicht gefunden." 
    
@pytest.mark.asyncio
async def test_set_player_status_fail_color_not_set(lobby_service):
    user_create_1 = UserLobby(user_id="1234", username="Max", color=None, status="not_ready")
    lobby = lobby_service.create_lobby(user_create_1)
    game_id = lobby.game_id
    
    try:
        response = await lobby_service.set_player_status(game_id, user_create_1.user_id, "ready")
    except ValueError as e:
        response = str(e)
    
    assert response == "Wähle zuerst eine Farbe."
    
def test_start_game_success_should_return_chess_game(lobby_service, mocker):
    lobby = Lobby(
        game_id="1234",
        players=[
            UserLobby(
                user_id="1234",
                username="Max",
                color=PlayerColor.WHITE,
                status=PlayerStatus.READY
            ),
            UserLobby(
                user_id="5678",
                username="Anna",
                color=PlayerColor.BLACK,
                status=PlayerStatus.READY
            )
        ]
    )
    
    print(lobby.players)
    
    lobby_service.game_lobbies["1234"] = lobby
    
    mocker.patch.object(ChessGameRepository, "insert_game", return_value=None)

    game = lobby_service.start_game("1234", "1234")

    assert isinstance(game, ChessGame)
    assert game.game_id == "1234"
    assert game.player_white.user_id == "1234"
    assert game.player_black.user_id == "5678"
    assert game.player_white.color == PlayerColor.WHITE.value
    assert game.player_black.color == PlayerColor.BLACK.value
    assert game.status == GameStatus.RUNNING
    assert game.current_turn == PlayerColor.WHITE.value
    assert game.board is not None

    ChessGameRepository.insert_game.assert_called_once()

def test_start_game_fail_not_found(lobby_service):
    try:
        response = lobby_service.start_game("1234", "1234")
    except ValueError as e:
        response = str(e)
    
    assert response == "Lobby nicht gefunden."
    
def test_start_game_fail_not_enough_players(lobby_service):
    lobby = Lobby(
        game_id="1234",
        players=[
            UserLobby(
                user_id="1234",
                username="Max",
                color=PlayerColor.WHITE,
                status=PlayerStatus.READY
            )
        ]
    )
    
    lobby_service.game_lobbies["1234"] = lobby
    
    try:
        response = lobby_service.start_game("1234", "1234")
    except ValueError as e:
        response = str(e)
        
    assert response == "Spiel braucht zwei Spieler."
    
def test_start_game_fail_not_host(lobby_service):
    lobby = Lobby(
        game_id="1234",
        players=[
            UserLobby(
                user_id="1234",
                username="Max",
                color=PlayerColor.WHITE,
                status=PlayerStatus.READY
            ),
            UserLobby(
                user_id="5678",
                username="Anna",
                color=PlayerColor.BLACK,
                status=PlayerStatus.READY
            )
        ]
    )
    
    lobby_service.game_lobbies["1234"] = lobby
    
    try:
        response = lobby_service.start_game("1234", "5678")
    except ValueError as e:
        response = str(e)
        
    assert response == "Nur der Host kann das Spiel starten."
    
def test_start_game_fail_not_all_colors_set(lobby_service):
    lobby = Lobby(
        game_id="1234",
        players=[
            UserLobby(
                user_id="1234",
                username="Max",
                color=None,
                status=PlayerStatus.READY
            ),
            UserLobby(
                user_id="5678",
                username="Anna",
                color=PlayerColor.BLACK,
                status=PlayerStatus.READY
            )
        ]
    )
    
    lobby_service.game_lobbies["1234"] = lobby
    
    try:
        response = lobby_service.start_game("1234", "1234")
    except ValueError as e:
        response = str(e)
        
    assert response == "Beide Spieler müssen eine Farbe wählen."
    
def test_start_game_fail_not_all_ready(lobby_service):
    lobby = Lobby(
        game_id="1234",
        players=[
            UserLobby(
                user_id="1234",
                username="Max",
                color=PlayerColor.WHITE,
                status=PlayerStatus.NOT_READY
            ),
            UserLobby(
                user_id="5678",
                username="Anna",
                color=PlayerColor.BLACK,
                status=PlayerStatus.READY
            )
        ]
    )
    
    lobby_service.game_lobbies["1234"] = lobby
    
    try:
        response = lobby_service.start_game("1234", "1234")
    except ValueError as e:
        response = str(e)
        
    assert response == "Beide Spieler müssen bereit sein."