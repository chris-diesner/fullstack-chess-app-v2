import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from router.auth import auth_router, create_access_token, token_blacklist
from user import User, UserResponse
from fastapi import FastAPI
from datetime import timedelta, datetime
import jwt

app = FastAPI()
app.include_router(auth_router)

client = TestClient(app)

@pytest.fixture
def mock_user_db():
    return {
        "id": "12345678-1234-5678-1234-567812345678",
        "username": "testuser",
        "password_hash": "hashedpassword123",
        "captured_figures": [],
        "move_history": []
    }

@pytest.fixture
def mock_user():
    return UserResponse(
        id="12345678-1234-5678-1234-567812345678",
        username="testuser",
        captured_figures=[],
        move_history=[]
    )

@pytest.fixture
def mock_db():
    find_mock = MagicMock()
    insert_mock = MagicMock()

    find_mock.return_value = {
        "id": "12345678-1234-5678-1234-567812345678",
        "username": "testuser",
        "password_hash": "hashedpassword123",
        "captured_figures": [],
        "move_history": []
    }

    with patch("database.users_collection.find_one", find_mock), \
         patch("database.users_collection.insert_one", insert_mock):
        yield find_mock, insert_mock

@pytest.fixture
def mock_token(mock_user):
    return create_access_token(data={"sub": mock_user.username}, expires_delta=timedelta(minutes=30))

def test_register_user_success_should_return_200_and_string_success(mock_db, mock_user):
    find_mock, insert_mock = mock_db
    find_mock.return_value = None

    response = client.post("/register", json={"username": mock_user.username, "password": "testPassw0rd"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}
    insert_mock.assert_called_once()

def test_register_user_already_exists_should_return_400_and_string_already_excists(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user_db

    response = client.post("/register", json={"username": mock_user.username, "password": "testpassword"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}
    
def test_register_user_password_too_short_should_return_400_and_string_password_too_short(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = None

    response = client.post("/register", json={"username": mock_user.username, "password": "short"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must be at least 8 characters long"}
    
def test_register_user_password_no_uppercase_should_return_400_and_string_password_no_uppercase(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = None

    response = client.post("/register", json={"username": mock_user.username, "password": "alllowercase"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must contain at least one uppercase letter"}
    
def test_register_user_password_no_number_should_return_400_and_string_password_no_number(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = None
    
    response = client.post("/register", json={"username": mock_user.username, "password": "NoNumber"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must contain at least one number"}

def test_login_success_should_return_200_and_valid_token(mock_db, mock_user_db):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user_db

    with patch.object(User, "verify_password", return_value=True):
        response = client.post("/login", data={"username": mock_user_db["username"], "password": "testpassword"})
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_user_not_found_should_return_401_and_string_invalid_user(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = None

    with patch.object(User, "verify_password", return_value=True):
        response = client.post("/login", data={"username": mock_user.username, "password": "testpassword"})
            
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}

def test_login_invalid_password_should_return_401_and_string_invalid_user(mock_db, mock_user_db):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user_db

    with patch.object(User, "verify_password", return_value=False):
        response = client.post("/login", data={"username": mock_user_db["username"], "password": "wrongpassword"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}

def test_get_current_user_success_should_return_200_and_string_current_user(mock_db, mock_user, mock_token):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user.dict()

    response = client.get("/users/me", headers={"Authorization": f"Bearer {mock_token}"})
    
    assert response.status_code == 200
    assert response.json()["username"] == mock_user.username
    assert response.json() == {"id": mock_user.id, "username": mock_user.username, "captured_figures": [], "move_history": []}

def test_get_current_user_no_token_should_return_401_and_sting_not_authenticated():
    response = client.get("/users/me")
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_current_user_invalid_token_should_return_401_and_sting_ivalid_token():
    invalid_token = jwt.encode({"sub": "testuser"}, "wrongsecret", algorithm="HS256")
    
    response = client.get("/users/me", headers={"Authorization": f"Bearer {invalid_token}"})
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_register_user_invalid_data_should_return_422():
    response = client.post("/register", data={"username": "", "password": ""})
    
    assert response.status_code == 422

def test_login_missing_username_should_return_422_and_string_required_username():
    response = client.post("/login", data={"username": "", "password": "testpassword"})
    
    assert response.status_code == 422
    assert response.json() == {"detail": "Username is required"}

def test_login_missing_password_should_return_422_and_string_required_password():
    response = client.post("/login", data={"username": "testuser", "password": ""})
    
    assert response.status_code == 422
    assert response.json() == {"detail": "Password is required"}

def test_get_current_user_expired_token_should_return_401_and_sting_expired_token(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user.dict()

    expired_token = create_access_token(data={"sub": mock_user.username}, expires_delta=timedelta(seconds=-100000000))

    response = client.get("/users/me", headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Token expired"}

def test_get_current_user_no_user_should_return_404_and_sting_not_found(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = None
    
    valid_token = create_access_token(data={"sub": mock_user.username})
    
    response = client.get("/users/me", headers={"Authorization": f"Bearer {valid_token}"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    
def test_get_current_user_revoked_token_should_return_401_and_sting_token_revoked(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user.dict()
    
    valid_token = create_access_token(data={"sub": mock_user.username})
    
    with patch("router.auth.token_blacklist", set()) as mock_blacklist:
        mock_blacklist.add(valid_token)
    
        response = client.get("/users/me", headers={"Authorization": f"Bearer {valid_token}"})
    
        assert response.status_code == 401
        assert response.json() == {"detail": "Token has been revoked"}

def test_logout_user_success_should_return_200_and_sting_success(mock_db, mock_user):
    find_mock, _ = mock_db
    find_mock.return_value = mock_user.dict()
    
    valid_token = create_access_token(data={"sub": mock_user.username})
    
    response = client.post("/logout", headers={"Authorization": f"Bearer {valid_token}"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}
    
def test_logout_user_already_expired_token_should_return_401_and_sting_expired():
    expired_token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(seconds=-100000000))
    
    response = client.post("/logout", headers={"Authorization": f"Bearer {expired_token}"})
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Token already expired"}