from typing import Optional
from sqlalchemy.orm import Session
from src.domain.user import User
from src.infrastructure.database.models import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            activation_code=user.activation_code
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)
    
    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_id(self, user_id: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(db_user) if db_user else None
    
    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            password_hash=db_user.password_hash,
            career_stage=db_user.career_stage,
            is_active=db_user.is_active,
            activation_code=db_user.activation_code,
            created_at=db_user.created_at
        )