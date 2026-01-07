import pytest
from src.domain.user import User
from pydantic import ValidationError

def test_user_creation():
    user = User(email="test@test.com", password_hash="hashed123")
    assert user.email == "test@test.com"
    assert user.password_hash == "hashed123"
    assert user.id is None
    assert user.created_at is None

def test_user_with_id():
    user = User(id="123", email="test@test.com", password_hash="hashed123")
    assert user.id == "123"

def test_user_invalid_email():
    with pytest.raises(ValidationError):
        User(email="invalid-email", password_hash="hashed123")

def test_user_with_career_stage():
    user = User(email="test@test.com", password_hash="hashed123", career_stage="Junior")
    assert user.career_stage == "Junior"