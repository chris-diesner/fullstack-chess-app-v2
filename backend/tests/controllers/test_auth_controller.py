import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app
from models.user import UserCreate, UserResponse
from services.auth_service import AuthService
from jsonschema import validate
from datetime import timedelta

client = TestClient(app)

@pytest.fixture
def mock_user():
    return UserCreate(username="testuser", password="testpassword")

@pytest.fixture
def mock_auth_service(mocker):
    mock_service = mocker.MagicMock(spec=AuthService)

    with patch("controllers.auth_controller.auth_service", mock_service):
        yield mock_service

@pytest.fixture
def mock_token(mock_user):
    return AuthService.create_access_token(data={"sub": mock_user.username}, expires_delta=timedelta(minutes=30))

def test_login_success_should_return_200_and_access_token(mock_auth_service, mock_user, mock_token):
    mock_auth_service.authenticate_user.return_value = UserResponse(user_id="mock_id", username=mock_user.username)    
    mock_auth_service.create_access_token.return_value = mock_token

    form_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/auth/login", data=form_data, headers={"Content-Type": "application/x-www-form-urlencoded"})

    login_schema = {
        "type": "object",
        "properties": {
            "access_token": {"type": "string"},
            "token_type": {"type": "string"}
        },
        "required": ["access_token", "token_type"]
    }

    validate(instance=response.json(), schema=login_schema)
    assert response.status_code == 200
    assert response.json()["access_token"] == mock_token
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_password_should_return_401_and_error_message(mock_auth_service):
    mock_auth_service.authenticate_user.return_value = None

    form_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/auth/login", data=form_data)

    error_schema = {
        "type": "object",
        "properties": {
            "detail": {"type": "string"}
        },
        "required": ["detail"]
    }

    validate(instance=response.json(), schema=error_schema)
    assert response.status_code == 401
    assert response.json()["detail"] == "Username oder Passwort falsch"

def test_login_user_not_found_should_return_401_and_error_message(mock_auth_service):
    mock_auth_service.authenticate_user.return_value = None
    form_data = {"username": "nonexistentuser", "password": "password123"}
    response = client.post("/auth/login", data=form_data)

    error_schema = {
        "type": "object",
        "properties": {
            "detail": {"type": "string"}
        },
        "required": ["detail"]
    }

    validate(instance=response.json(), schema=error_schema)
    assert response.status_code == 401
    assert response.json()["detail"] == "Username oder Passwort falsch"

def test_logout_success_should_return_200_and_success_message(mock_auth_service, mock_token):
    mock_auth_service.logout.return_value = True  
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {mock_token}"})

    logout_schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }

    validate(instance=response.json(), schema=logout_schema)
    assert response.status_code == 200
    assert response.json()["message"] == "Logout erfolgreich"

def test_logout_unauthenticated_should_return_401_and_error_message(mock_auth_service):
    mock_auth_service.logout.return_value = None  
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer invalid_token"})

    error_schema = {
        "type": "object",
        "properties": {
            "detail": {"type": "string"}
        },
        "required": ["detail"]
    }

    validate(instance=response.json(), schema=error_schema)
    assert response.status_code == 401
    assert response.json()["detail"] == "Token ungültig oder bereits abgelaufen"
