import pytest
from unittest.mock import Mock
from src.application.use_cases.register_user import RegisterUserUseCase
from src.domain.user import User

@pytest.fixture
def mock_user_repository():
    return Mock()

def test_register_user_success(mock_user_repository):
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.return_value = User(
        id="user123",
        email="test@test.com",
        password_hash="hashed"
    )
    
    use_case = RegisterUserUseCase(mock_user_repository)
    result = use_case.execute("test@test.com", "Test1234")
    
    assert result["user_id"] == "user123"
    assert result["email"] == "test@test.com"
    assert "access_token" in result
    mock_user_repository.create.assert_called_once()

def test_register_user_weak_password(mock_user_repository):
    use_case = RegisterUserUseCase(mock_user_repository)
    
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        use_case.execute("test@test.com", "weak")

def test_register_user_email_exists(mock_user_repository):
    mock_user_repository.get_by_email.return_value = User(
        id="existing",
        email="test@test.com",
        password_hash="hashed"
    )
    
    use_case = RegisterUserUseCase(mock_user_repository)
    
    with pytest.raises(ValueError, match="Email already registered"):
        use_case.execute("test@test.com", "Test1234")