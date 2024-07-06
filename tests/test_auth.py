import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
client = TestClient(app)

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.users = MagicMock()
    db.users.append({"email": "test@example.com"})
    return db

@pytest.fixture
def mock_user():
    return {"email": "test@example.com"}

@patch("app.utils.otp.send_otp")
def test_enter_email_existing_user(mock_send_otp, mock_db):
    mock_db.users.find_one.return_value = {"email": "test@example.com"}
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/enter-mail", json={"email": "test@example.com"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User found, OTP sent", "is_new_user": False}
    mock_send_otp.assert_called_once_with(email="test@example.com")

@patch("app.utils.otp.send_otp")
def test_enter_email_new_user(mock_send_otp, mock_db):
    mock_db.users.find_one.return_value = None
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/enter-mail", json={"email": "new@example.com"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "User created, OTP sent", "is_new_user": True}
    mock_send_otp.assert_called_once_with(email="new@example.com")
    mock_db.users.insert_one.assert_called_once()

@patch("app.utils.redis_client.get_otp")
@patch("app.utils.token.token_manager.create_access_token")
@patch("app.utils.token.token_manager.create_refresh_token")
def test_verify_otp_valid(mock_create_refresh_token, mock_create_access_token, mock_get_otp, mock_db, mock_user):
    mock_db.users.find_one.return_value = mock_user
    mock_get_otp.return_value = b"123456"
    mock_create_access_token.return_value = "access_token"
    mock_create_refresh_token.return_value = "refresh_token"
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/verify-otp", json={"email": "test@example.com", "otp": 123456, "is_new_user": False})
    
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "token_type": "bearer",
        "is_new_user": False
    }

@patch("app.utils.redis_client.get_otp")
def test_verify_otp_invalid(mock_get_otp, mock_db, mock_user):
    mock_db.users.find_one.return_value = mock_user
    mock_get_otp.return_value = b"123456"
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/verify-otp", json={"email": "test@example.com", "otp": 654321, "is_new_user": False})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid OTP"}

@patch("app.utils.otp.send_otp")
def test_resend_otp_existing_user(mock_send_otp, mock_db, mock_user):
    mock_db.users.find_one.return_value = mock_user
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/resend-otp", json={"email": "test@example.com"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "OTP resent"}
    mock_send_otp.assert_called_once_with(email="test@example.com")

def test_resend_otp_nonexistent_user(mock_db):
    mock_db.users.find_one.return_value = None
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/resend-otp", json={"email": "nonexistent@example.com"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

@patch("app.auth.routes.get_current_user")
def test_register_user(mock_get_current_user, mock_db):
    mock_get_current_user.return_value = {"email": "test@example.com"}
    mock_db.users.update_one.return_value = MagicMock(modified_count=1)
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.post("/auth/register", headers={"Authorization": "Bearer token"}, json={
            "first_name": "John",
            "last_name": "Doe"
        })
    
    assert response.status_code == 200
    assert response.json() == {"message": "User information updated"}

@patch("app.auth.routes.get_current_user")
def test_modify_user(mock_get_current_user, mock_db):
    mock_get_current_user.return_value = {"email": "test@example.com"}
    mock_db.users.update_one.return_value = MagicMock(modified_count=1)
    
    with patch("app.auth.routes.get_db", return_value=mock_db):
        response = client.put("/auth/modify_user", headers={"Authorization": "Bearer token"}, json={
            "first_name": "Jane",
            "last_name": "Doe"
        })
    
    assert response.status_code == 200
    assert response.json() == {"message": "User information modified"}

@patch("app.utils.token.token_manager.refresh_tokens")
def test_refresh_token(mock_refresh_tokens):
    mock_refresh_tokens.return_value = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token"
    }
    
    response = client.post("/auth/refresh-token", json={"refresh_token": "old_refresh_token"})
    
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "token_type": "bearer",
        "is_new_user": False
    }

@patch("app.auth.routes.get_current_user")
@patch("app.utils.token.token_manager.revoke_refresh_token")
def test_logout(mock_revoke_refresh_token, mock_get_current_user):
    mock_get_current_user.return_value = {"email": "test@example.com"}
    
    response = client.post("/auth/logout", headers={"Authorization": "Bearer token"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}
    mock_revoke_refresh_token.assert_called_once_with("test@example.com")