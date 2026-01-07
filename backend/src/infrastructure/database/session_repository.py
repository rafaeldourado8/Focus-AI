from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.learning_session import LearningSession, SessionStatus
from src.infrastructure.database.models import LearningSessionModel

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, session: LearningSession) -> LearningSession:
        db_session = LearningSessionModel(
            user_id=session.user_id,
            status=session.status
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return LearningSession(
            id=db_session.id,
            user_id=db_session.user_id,
            status=db_session.status,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at
        )
    
    def get_by_id(self, session_id: str) -> Optional[LearningSession]:
        db_session = self.db.query(LearningSessionModel).filter(
            LearningSessionModel.id == session_id
        ).first()
        if not db_session:
            return None
        return LearningSession(
            id=db_session.id,
            user_id=db_session.user_id,
            status=db_session.status,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at
        )
    
    def update_status(self, session_id: str, status: SessionStatus) -> bool:
        result = self.db.query(LearningSessionModel).filter(
            LearningSessionModel.id == session_id
        ).update({"status": status})
        self.db.commit()
        return result > 0
    
    def get_by_user(self, user_id: str) -> List[LearningSession]:
        db_sessions = self.db.query(LearningSessionModel).filter(
            LearningSessionModel.user_id == user_id
        ).all()
        return [
            LearningSession(
                id=s.id,
                user_id=s.user_id,
                status=s.status,
                created_at=s.created_at,
                updated_at=s.updated_at
            ) for s in db_sessions
        ]