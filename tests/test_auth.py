import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock

client = TestClient(app)

@pytest.fixture
def db_mock():
    mock = MagicMock()
    yield mock

@pytest.fixture
def redis_mock():
    mock = MagicMock()
    yield mock

@pytest.fixture
def token_manager_mock():
    mock = MagicMock()
    yield mock

def test_enter_email_existing_user(db_mock):
    db_mock.return_value.users.find_one.return_value = {"email": "test@example.com"}
    response = client.post("/enter-mail", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "User found, OTP sent", "is_new_user": False}

def test_enter_email_new_user(db_mock):
    db_mock.return_value.users.find_one.return_value = None
    response = client.post("/enter-mail", json={"email": "new@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created, OTP sent", "is_new_user": True}

def test_verify_otp(db_mock, redis_mock, token_manager_mock):
    db_mock.return_value.users.find_one.return_value = {"email": "test@example.com"}
    redis_mock.get_otp.return_value = b"1234"
    token_manager_mock.create_access_token.return_value = "access_token"
    token_manager_mock.create_refresh_token.return_value = "refresh_token"
    response = client.post("/verify-otp", json={"email": "test@example.com", "otp": 1234, "is_new_user": False})
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "token_type": "bearer",
        "is_new_user": False
    }

def test_resend_otp_existing_user(db_mock):
    db_mock.return_value.users.find_one.return_value = {"email": "test@example.com"}
    response = client.post("/resend-otp", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "OTP resent"}

def test_resend_otp_user_not_found(db_mock):
    db_mock.return_value.users.find_one.return_value = None
    response = client.post("/resend-otp", json={"email": "notfound@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_register_user(db_mock, token_manager_mock):
    db_mock.return_value.users.update_one.return_value.modified_count = 1
    token_manager_mock.validate_token.return_value = {"email": "test@example.com"}
    response = client.post("/register", json={"name": "New User"}, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "User information updated"}

def test_modify_user(db_mock, token_manager_mock):
    db_mock.return_value.users.update_one.return_value.modified_count = 1
    token_manager_mock.validate_token.return_value = {"email": "test@example.com"}
    response = client.put("/modify_user", json={"name": "Modified User"}, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "User information modified"}

def test_refresh_token(token_manager_mock):
    token_manager_mock.refresh_tokens.return_value = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token"
    }
    response = client.post("/refresh-token", json={"refresh_token": "valid_refresh_token"})
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "token_type": "bearer",
        "is_new_user": False
    }

def test_logout(token_manager_mock):
    token_manager_mock.validate_token.return_value = {"email": "test@example.com"}
    response = client.post("/logout", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

def test_verify_otp_invalid(db_mock, redis_mock):
    db_mock.return_value.users.find_one.return_value = {"email": "test@example.com"}
    redis_mock.get_otp.return_value = b"1234"
    response = client.post("/verify-otp", json={"email": "test@example.com", "otp": 5678, "is_new_user": False})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid OTP"}

def test_register_user_not_found(db_mock, token_manager_mock):
    db_mock.return_value.users.update_one.return_value.modified_count = 0
    token_manager_mock.validate_token.return_value = {"email": "test@example.com"}
    response = client.post("/register", json={"name": "New User"}, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_modify_user_not_found(db_mock, token_manager_mock):
    db_mock.return_value.users.update_one.return_value.modified_count = 0
    token_manager_mock.validate_token.return_value = {"email": "test@example.com"}
    response = client.put("/modify_user", json={"name": "Modified User"}, headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_refresh_token_invalid(token_manager_mock):
    token_manager_mock.refresh_tokens.return_value = None
    response = client.post("/refresh-token", json={"refresh_token": "invalid_refresh_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired refresh token"}

def test_protected_route_invalid_token(token_manager_mock):
    token_manager_mock.validate_token.return_value = None
    response = client.post("/logout", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired token"}
