import pytest
from unittest.mock import Mock
from src.application.use_cases.create_session import CreateSessionUseCase
from src.domain.learning_session import LearningSession, SessionStatus
from datetime import datetime

@pytest.fixture
def mock_session_repository():
    return Mock()

def test_create_session_success(mock_session_repository):
    mock_session_repository.create.return_value = LearningSession(
        id="session123",
        user_id="user123",
        status=SessionStatus.ACTIVE,
        created_at=datetime.utcnow()
    )
    
    use_case = CreateSessionUseCase(mock_session_repository)
    result = use_case.execute("user123")
    
    assert result["session_id"] == "session123"
    assert result["status"] == "active"
    assert "created_at" in result
    mock_session_repository.create.assert_called_once()