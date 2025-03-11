import pytest
from unittest.mock import MagicMock
from datetime import timedelta
from models.user import UserDB, UserResponse
from services.auth_service import AuthService, token_blacklist, SECRET_KEY, ALGORITHM
import jwt

@pytest.fixture
def user_repo_mock():
    mock = MagicMock()
    return mock

def test_create_access_token_should_return_valid_token():
    data = {"sub": "testuser"}
    token = AuthService.create_access_token(data)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "testuser"

def test_get_current_user_should_return_user():
    data = {"sub": "testuser"}
    token = AuthService.create_access_token(data)
    user = AuthService.get_current_user(token)
    assert user == "testuser"

def test_get_current_user_expired_token_should_return_none():
    data = {"sub": "testuser"}
    token = AuthService.create_access_token(data, expires_delta=timedelta(seconds=-1000000000))
    user = AuthService.get_current_user(token)
    assert user is None

def test_hash_password_should_return_hashed_password():
    password = "password123"
    hashed_password = AuthService.hash_password(password)
    assert AuthService.verify_password(password, hashed_password)
    
def test_verify_password_should_return_true():
    password = "password123"
    hashed_password = AuthService.hash_password(password)
    assert AuthService.verify_password(password, hashed_password)
    
def test_verify_password_invalid_should_return_false():
    password = "password123"
    hashed_password = AuthService.hash_password(password)
    assert not AuthService.verify_password("invalidpassword", hashed_password)

def test_authenticate_user_should_return_user(user_repo_mock):
    mock_user = UserDB(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        username="testuser",
        password_hash=AuthService.hash_password("password123")
    )

    user_repo_mock.find_user_by_username.return_value = mock_user
    auth_service = AuthService(user_repo_mock)
    user = auth_service.authenticate_user("testuser", "password123")

    assert user is not None
    assert isinstance(user, UserResponse)
    assert user.username == "testuser"
    assert user.user_id == "123e4567-e89b-12d3-a456-426614174000"


def test_authenticate_user_invalid_password_should_return_none(user_repo_mock):
    mock_user = UserDB(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        username="testuser",
        password_hash=AuthService.hash_password("password123")
    )

    user_repo_mock.find_user_by_username.return_value = mock_user
    auth_service = AuthService(user_repo_mock)
    user = auth_service.authenticate_user("testuser", "wrongpassword")
    
    assert user is None

def test_authenticate_user_nonexistent_user_should_return_none(user_repo_mock):
    user_repo_mock.find_user_by_username.return_value = None
    auth_service = AuthService(user_repo_mock)
    user = auth_service.authenticate_user("nonexistentuser", "password123")
    
    assert user is None

def test_logout_should_add_token_to_blacklist():
    token = AuthService.create_access_token({"sub": "testuser"})
    AuthService.logout(token)
    assert token in token_blacklist

def test_is_token_revoked_should_return_true():
    token = AuthService.create_access_token({"sub": "testuser"})
    AuthService.logout(token)
    assert AuthService.is_token_revoked(token)
