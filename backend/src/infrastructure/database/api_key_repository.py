"""
API Key Repository

Handles database operations for API keys
"""

from sqlalchemy.orm import Session
from src.infrastructure.database.api_key_model import APIKeyModel
from src.domain.api_key import APIKey
from typing import Optional, List
import secrets
import logging

logger = logging.getLogger(__name__)


class APIKeyRepository:
    """Repository for API key operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, name: str, plan: str = "free") -> APIKey:
        """Create new API key"""
        # Generate secure random key
        key = f"ck_{'live' if plan != 'free' else 'test'}_{secrets.token_urlsafe(32)}"
        
        db_key = APIKeyModel(
            key=key,
            user_id=user_id,
            name=name,
            plan=plan
        )
        
        self.db.add(db_key)
        self.db.commit()
        self.db.refresh(db_key)
        
        logger.info(f"API key created: {name} (user_id={user_id})")
        
        return self._to_entity(db_key)
    
    def get_by_key(self, key: str) -> Optional[APIKey]:
        """Get API key by key value"""
        db_key = self.db.query(APIKeyModel).filter(APIKeyModel.key == key).first()
        return self._to_entity(db_key) if db_key else None
    
    def get_by_user(self, user_id: int) -> List[APIKey]:
        """Get all API keys for user"""
        db_keys = self.db.query(APIKeyModel).filter(APIKeyModel.user_id == user_id).all()
        return [self._to_entity(k) for k in db_keys]
    
    def update(self, key: str, **kwargs) -> Optional[APIKey]:
        """Update API key"""
        db_key = self.db.query(APIKeyModel).filter(APIKeyModel.key == key).first()
        
        if not db_key:
            return None
        
        for field, value in kwargs.items():
            if hasattr(db_key, field):
                setattr(db_key, field, value)
        
        self.db.commit()
        self.db.refresh(db_key)
        
        logger.info(f"API key updated: {key[:8]}...")
        
        return self._to_entity(db_key)
    
    def deactivate(self, key: str) -> bool:
        """Deactivate API key"""
        db_key = self.db.query(APIKeyModel).filter(APIKeyModel.key == key).first()
        
        if not db_key:
            return False
        
        db_key.is_active = False
        self.db.commit()
        
        logger.info(f"API key deactivated: {key[:8]}...")
        
        return True
    
    def rotate(self, old_key: str) -> Optional[APIKey]:
        """Rotate API key (create new, deactivate old)"""
        db_key = self.db.query(APIKeyModel).filter(APIKeyModel.key == old_key).first()
        
        if not db_key:
            return None
        
        # Create new key with same settings
        new_key = self.create(
            user_id=db_key.user_id,
            name=f"{db_key.name} (rotated)",
            plan=db_key.plan
        )
        
        # Deactivate old key
        self.deactivate(old_key)
        
        logger.info(f"API key rotated: {old_key[:8]}... -> {new_key.key[:8]}...")
        
        return new_key
    
    def increment_usage(self, key: str):
        """Increment usage counter"""
        from datetime import datetime
        
        db_key = self.db.query(APIKeyModel).filter(APIKeyModel.key == key).first()
        
        if db_key:
            db_key.usage_count += 1
            db_key.last_used_at = datetime.utcnow()
            self.db.commit()
    
    def _to_entity(self, db_key: APIKeyModel) -> APIKey:
        """Convert database model to domain entity"""
        return APIKey(
            key=db_key.key,
            user_id=db_key.user_id,
            name=db_key.name,
            plan=db_key.plan,
            is_active=db_key.is_active,
            created_at=db_key.created_at,
            expires_at=db_key.expires_at,
            last_used_at=db_key.last_used_at,
            usage_count=db_key.usage_count
        )
