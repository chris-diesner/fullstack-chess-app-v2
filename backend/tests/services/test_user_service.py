import pytest
from unittest.mock import MagicMock
from services.user_service import UserService
from models.user import UserCreate, UserResponse
import uuid

@pytest.fixture
def user_service():
    service = UserService()
    service.user_repo = MagicMock()
    return service

def test_create_user_should_return_created_username(user_service):
    user_data = UserCreate(username="testuser", password="securepassword")

    user_service.user_repo.find_user_by_username.return_value = None

    mock_created_user = UserResponse(id=str(uuid.uuid4()), username=user_data.username)
    user_service.user_repo.insert_user.return_value = mock_created_user

    created_user = user_service.create_user(user_data)

    assert created_user.username == user_data.username
    assert isinstance(created_user.id, str)
    assert len(created_user.id) == 36
    
def test_create_user_existing_should_return_none(user_service):
    user_data = UserCreate(username="existinguser", password="securepassword")
    user_service.user_repo.find_user_by_username = MagicMock(return_value={"username": user_data.username})
    
    created_user = user_service.create_user(user_data)
    
    assert created_user is None
    user_service.user_repo.find_user_by_username.assert_called_once_with(user_data.username)

def test_get_user_by_username_should_return_created_username_and_its_id(user_service):
    username = "testuser"
    mock_user = UserResponse(id="123e4567-e89b-12d3-a456-426614174000", username=username)

    user_service.user_repo.find_user_by_username = MagicMock(return_value=mock_user.model_dump(by_alias=True))

    user = user_service.get_user_by_username(username)
    
    assert user.username == username
    assert isinstance(user.id, str)
    assert len(user.id) == 36
    assert user.id == "123e4567-e89b-12d3-a456-426614174000"

def test_get_user_by_username_not_found_should_return_none(user_service):
    username = "nonexistentuser"
    user_service.user_repo.find_user_by_username = MagicMock(return_value=None)
    
    user = user_service.get_user_by_username(username)
    
    assert user is None
    user_service.user_repo.find_user_by_username.assert_called_once_with(username)

def test_get_user_by_id_should_return_created_username_and_its_id(user_service):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_user = UserResponse(id=user_id, username="testuser")

    user_service.user_repo.find_user_by_id = MagicMock(return_value=mock_user.model_dump(by_alias=True))

    user = user_service.get_user_by_id(user_id)
    
    assert user.username == mock_user.username
    assert isinstance(user.id, str)
    assert len(user.id) == 36
    assert user.id == user_id
    
def test_get_user_by_id_not_found_should_return_none(user_service):
    user_id = "nonexistentid"
    user_service.user_repo.find_user_by_id = MagicMock(return_value=None)

    user = user_service.get_user_by_id(user_id)
    
    assert user is None
    user_service.user_repo.find_user_by_id.assert_called_once_with(user_id)
    
def test_update_user_should_return_updated_username(user_service):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    new_username = "updateduser"
    mock_user = UserResponse(id=user_id, username=new_username)

    user_service.user_repo.update_user = MagicMock(return_value=mock_user.model_dump(by_alias=True))

    updated_user = user_service.update_user(user_id, username=new_username)
    
    assert updated_user.username == new_username
    assert isinstance(updated_user.id, str)
    assert len(updated_user.id) == 36
    assert updated_user.id == user_id

def test_update_user_should_return_updated_password(user_service):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    new_password = "newsecurepassword"
    mock_user = UserResponse(id=user_id, username="testuser")

    user_service.user_repo.update_user = MagicMock(return_value=mock_user.model_dump(by_alias=True))

    updated_user = user_service.update_user(user_id, password=new_password)
    
    assert updated_user.username == mock_user.username
    assert isinstance(updated_user.id, str)
    assert len(updated_user.id) == 36
    assert updated_user.id == user_id

def test_update_user_not_found_should_return_none(user_service):
    user_id = "nonexistentid"
    user_service.user_repo.update_user = MagicMock(return_value=None)

    updated_user = user_service.update_user(user_id, username="updateduser")
    
    assert updated_user is None
    user_service.user_repo.update_user.assert_called_once_with(user_id, {"username": "updateduser"})
    
def test_delete_user_should_return_true_when_user_is_deleted(user_service):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    user_service.user_repo.delete_user = MagicMock(return_value=True)

    result = user_service.delete_user(user_id)
    
    assert result is True
    user_service.user_repo.delete_user.assert_called_once_with(user_id)

def test_delete_user_should_return_false_when_user_is_not_found(user_service):
    user_id = "nonexistentid"
    user_service.user_repo.delete_user = MagicMock(return_value=False)

    result = user_service.delete_user(user_id)
    
    assert result is False
    user_service.user_repo.delete_user.assert_called_once_with(user_id)