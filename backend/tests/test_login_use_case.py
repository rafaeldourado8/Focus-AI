import pytest
from unittest.mock import Mock
from src.application.use_cases.login_user import LoginUserUseCase
from src.domain.user import User
from src.infrastructure.auth.auth_service import AuthService

@pytest.fixture
def mock_user_repository():
    return Mock()

def test_login_user_success(mock_user_repository):
    password = "Test1234"
    hashed = AuthService.hash_password(password)
    
    mock_user_repository.get_by_email.return_value = User(
        id="user123",
        email="test@test.com",
        password_hash=hashed
    )
    
    use_case = LoginUserUseCase(mock_user_repository)
    result = use_case.execute("test@test.com", password)
    
    assert result["user_id"] == "user123"
    assert result["email"] == "test@test.com"
    assert "access_token" in result

def test_login_user_not_found(mock_user_repository):
    mock_user_repository.get_by_email.return_value = None
    
    use_case = LoginUserUseCase(mock_user_repository)
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.execute("test@test.com", "Test1234")

def test_login_user_wrong_password(mock_user_repository):
    password = "Test1234"
    hashed = AuthService.hash_password(password)
    
    mock_user_repository.get_by_email.return_value = User(
        id="user123",
        email="test@test.com",
        password_hash=hashed
    )
    
    use_case = LoginUserUseCase(mock_user_repository)
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        use_case.execute("test@test.com", "WrongPass123")