import pytest
from unittest.mock import patch, MagicMock, Mock
from fastapi.testclient import TestClient
from services.user_service import UserService
from services.auth_service import AuthService
from models.user import UserCreate, UserResponse
from datetime import timedelta
from app import app
from jsonschema import validate

client = TestClient(app)

@pytest.fixture
def mock_user():
    return UserCreate(username="testuser", password="testpassword")

@pytest.fixture
def mock_user_response():
    return UserResponse(id="12345678-1234-5678-1234-567812345678", username="testuser", captured_figures=[], move_history=[])

@pytest.fixture
def mock_existing_user():
    return UserResponse(id="123e4567-e89b-12d3-a456-426614174000", username="testuser", captured_figures=[],move_history=[],)

@pytest.fixture
def mock_user_service(mocker):
    mock_service = mocker.MagicMock(spec=UserService)

    with patch("controllers.user_controller.user_service", mock_service):
        yield mock_service
        
@pytest.fixture
def mock_auth_service(mocker):
    mock_service = mocker.MagicMock(spec=AuthService)

    with patch("controllers.auth_controller.auth_service", mock_service):
        yield mock_service
        
@pytest.fixture
def mock_token():
    return AuthService.create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))

def test_register_user_schema_should_return_200_and_valid_user(mock_user_service, mock_user, mock_user_response):
    mock_user_service.create_user.return_value = mock_user_response

    response = client.post("/users/register", json=mock_user.model_dump())

    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "username": {"type": "string"},
            "captured_figures": {"type": "array"},
            "move_history": {"type": "array"},
        },
        "required": ["id", "username"]
    }

    validate(instance=response.json(), schema=user_schema)
    assert response.status_code == 200
    assert response.json()["username"] == mock_user.username

def test_register_existing_user_should_return_400_and_error_message(mock_user_service, mock_existing_user, mock_user):
    mock_user_service.get_user_by_username.return_value = mock_existing_user

    mock_user_service.create_user.return_value = None

    response = client.post("/users/register", json=mock_user.model_dump())

    assert response.status_code == 400
    assert response.json()["detail"] == "Username existiert bereits"

def test_get_current_user_should_return_200_and_valid_user(mock_user_service, mock_user, mock_token):
    mock_user_service.get_user_by_username.return_value = mock_user

    headers = {"Authorization": f"Bearer {mock_token}"}
    response = client.get("/users/me", headers=headers)

    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "username": {"type": "string"},
            "captured_figures": {"type": "array"},
            "move_history": {"type": "array"},
        },
        "required": ["id", "username"]
    }

    validate(instance=response.json(), schema=user_schema)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    
def test_get_current_user_unauthenticated_should_return_401_and_error_message(mock_user_service, mock_user):
    mock_user_service = Mock()
    mock_user_service.get_user_by_username.return_value = mock_user

    headers = {"Authorization": f"Bearer invalid_token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Nicht authentifiziert"
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Nicht authentifiziert"

def test_update_user_username_should_return_200_and_updated_user(mock_user_service, mock_user):
    mock_user_service.create_user.return_value = UserResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        username="testuser",
        captured_figures=[],
        move_history=[]
    )
    mock_user_service.get_user_by_id.return_value = mock_user
    mock_user_service.update_user.return_value = UserResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        username="testuser_edited",
        captured_figures=[],
        move_history=[]
    )

    response = client.put(f"/users/update/{id}", json=mock_user.model_dump())

    user_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "username": {"type": "string"},
            "captured_figures": {"type": "array"},
            "move_history": {"type": "array"},
        },
        "required": ["id", "username"]
    }

    validate(instance=response.json(), schema=user_schema)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser_edited"

def test_update_user_password_should_return_200_and_new_hashed_password(mock_user_service, mock_user, mock_auth_service, mock_token):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    new_password = "newpassword"
    mock_auth_service = MagicMock()
    mock_auth_service.authenticate_user.return_value = {"username": "testuser", "password": new_password}
    mock_auth_service.create_access_token.return_value = mock_token
    mock_user_service.get_user_by_id.return_value = mock_user

    def mock_update_user(user_id, username=None, password=None):
        assert AuthService.verify_password(new_password, password)

        return UserResponse(
            id=user_id,
            username="testuser",
            captured_figures=[],
            move_history=[]
        )

    mock_user_service.update_user.side_effect = mock_update_user

    response = client.put(f"/users/update/{user_id}", json={"password": new_password})

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    mock_user_service.update_user.assert_called_once()
    called_args, called_kwargs = mock_user_service.update_user.call_args

    assert "password" in called_kwargs
    
    stored_password_hash = called_kwargs["password"]

    assert AuthService.verify_password(new_password, stored_password_hash)
    
def test_delete_user_success_should_return_200_and_success_message(mock_user_service):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_user_service.delete_user.return_value = True

    response = client.delete(f"/users/delete/{user_id}")

    delete_response_schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }

    validate(instance=response.json(), schema=delete_response_schema)
    assert response.status_code == 200
    assert response.json() == {"message": "Benutzer erfolgreich gelöscht"}

    mock_user_service.delete_user.assert_called_once_with(user_id)

def test_delete_user_not_found_should_return_404_and_error_message(mock_user_service):
    user_id = "nonexistent-user-id"

    mock_user_service.delete_user.return_value = False

    response = client.delete(f"/users/delete/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Benutzer nicht gefunden"}

    mock_user_service.delete_user.assert_called_once_with(user_id)