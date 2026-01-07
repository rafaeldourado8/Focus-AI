from src.domain.learning_session import LearningSession
from src.infrastructure.database.session_repository import SessionRepository

class CreateSessionUseCase:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository
    
    def execute(self, user_id: str) -> dict:
        session = LearningSession(user_id=user_id)
        created_session = self.session_repository.create(session)
        
        return {
            "session_id": created_session.id,
            "status": created_session.status.value,
            "created_at": created_session.created_at.isoformat()
        }