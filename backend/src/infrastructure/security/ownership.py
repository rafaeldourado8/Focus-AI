"""
Ownership Validation Decorator

Prevents IDOR (Insecure Direct Object Reference) attacks
"""

from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def validate_session_ownership(func):
    """Validate that session belongs to user"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session_id = kwargs.get('session_id')
        user_id = kwargs.get('user_id')
        db: Session = kwargs.get('db')
        
        if not all([session_id, user_id, db]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters"
            )
        
        from src.infrastructure.database.session_repository import SessionRepository
        session_repo = SessionRepository(db)
        session = session_repo.get_by_id(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return await func(*args, **kwargs)
    return wrapper


def validate_api_key_ownership(func):
    """Validate that API key belongs to user"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = kwargs.get('key')
        current_user = kwargs.get('current_user')
        db: Session = kwargs.get('db')
        
        if not all([key, current_user, db]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters"
            )
        
        from src.infrastructure.database.api_key_repository import APIKeyRepository
        repo = APIKeyRepository(db)
        api_key = repo.get_by_key(key)
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        if api_key.user_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return await func(*args, **kwargs)
    return wrapper
