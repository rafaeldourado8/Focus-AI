import pytest
from src.domain.learning_session import LearningSession, SessionStatus

def test_session_creation():
    session = LearningSession(user_id="user123")
    assert session.user_id == "user123"
    assert session.status == SessionStatus.ACTIVE
    assert session.id is None

def test_session_with_status():
    session = LearningSession(user_id="user123", status=SessionStatus.PROCESSING)
    assert session.status == SessionStatus.PROCESSING

def test_session_status_enum():
    assert SessionStatus.ACTIVE.value == "active"
    assert SessionStatus.PROCESSING.value == "processing"
    assert SessionStatus.COMPLETED.value == "completed"