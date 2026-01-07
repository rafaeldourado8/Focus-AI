import pytest
from src.infrastructure.auth.auth_service import AuthService

def test_hash_password():
    password = "Test123456"
    hashed = AuthService.hash_password(password)
    assert hashed != password
    assert len(hashed) > 0

def test_verify_password():
    password = "Test123456"
    hashed = AuthService.hash_password(password)
    assert AuthService.verify_password(password, hashed) is True
    assert AuthService.verify_password("wrong", hashed) is False

def test_validate_password_strength_valid():
    assert AuthService.validate_password_strength("Test1234") is True
    assert AuthService.validate_password_strength("MyPass123") is True

def test_validate_password_strength_too_short():
    assert AuthService.validate_password_strength("Test12") is False

def test_validate_password_strength_no_uppercase():
    assert AuthService.validate_password_strength("test1234") is False

def test_validate_password_strength_no_lowercase():
    assert AuthService.validate_password_strength("TEST1234") is False

def test_validate_password_strength_no_number():
    assert AuthService.validate_password_strength("TestTest") is False

def test_create_access_token():
    token = AuthService.create_access_token({"sub": "user123"})
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_token_valid():
    token = AuthService.create_access_token({"sub": "user123"})
    user_id = AuthService.verify_token(token)
    assert user_id == "user123"

def test_verify_token_invalid():
    user_id = AuthService.verify_token("invalid_token")
    assert user_id is None