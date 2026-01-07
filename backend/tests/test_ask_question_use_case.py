import pytest
from unittest.mock import Mock
from src.application.use_cases.ask_question import AskQuestionUseCase
from src.domain.learning_session import LearningSession, SessionStatus
from src.domain.qa import Question, Answer
from datetime import datetime

@pytest.fixture
def mock_repositories():
    return {
        "session_repo": Mock(),
        "question_repo": Mock(),
        "answer_repo": Mock(),
        "cache_service": Mock(),
        "llm_service": Mock()
    }

def test_ask_question_success(mock_repositories):
    mock_repositories["session_repo"].get_by_id.return_value = LearningSession(
        id="session123",
        user_id="user123",
        status=SessionStatus.ACTIVE
    )
    mock_repositories["cache_service"].is_locked.return_value = False
    mock_repositories["cache_service"].acquire_lock.return_value = True
    
    mock_repositories["question_repo"].create.return_value = Question(
        id="q123",
        session_id="session123",
        content="What is DDD?"
    )
    
    mock_repositories["llm_service"].generate_socratic_answer.return_value = {
        "content": "DDD is Domain-Driven Design",
        "explanation": "Detailed explanation",
        "edge_cases": "Edge cases"
    }
    
    mock_repositories["answer_repo"].create.return_value = Answer(
        id="a123",
        question_id="q123",
        content="DDD is Domain-Driven Design",
        explanation="Detailed explanation",
        edge_cases="Edge cases"
    )
    
    use_case = AskQuestionUseCase(**mock_repositories)
    result = use_case.execute("session123", "user123", "What is DDD?")
    
    assert result["question_id"] == "q123"
    assert result["answer_id"] == "a123"
    assert result["content"] == "DDD is Domain-Driven Design"
    mock_repositories["cache_service"].release_lock.assert_called_once()

def test_ask_question_session_not_found(mock_repositories):
    mock_repositories["session_repo"].get_by_id.return_value = None
    
    use_case = AskQuestionUseCase(**mock_repositories)
    
    with pytest.raises(ValueError, match="Session not found"):
        use_case.execute("session123", "user123", "What is DDD?")

def test_ask_question_unauthorized(mock_repositories):
    mock_repositories["session_repo"].get_by_id.return_value = LearningSession(
        id="session123",
        user_id="other_user",
        status=SessionStatus.ACTIVE
    )
    
    use_case = AskQuestionUseCase(**mock_repositories)
    
    with pytest.raises(ValueError, match="Unauthorized"):
        use_case.execute("session123", "user123", "What is DDD?")

def test_ask_question_session_locked(mock_repositories):
    mock_repositories["session_repo"].get_by_id.return_value = LearningSession(
        id="session123",
        user_id="user123",
        status=SessionStatus.ACTIVE
    )
    mock_repositories["cache_service"].is_locked.return_value = True
    
    use_case = AskQuestionUseCase(**mock_repositories)
    
    with pytest.raises(ValueError, match="processing another question"):
        use_case.execute("session123", "user123", "What is DDD?")