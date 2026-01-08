"""
Tests for Ownership Validation
"""

import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock
from src.infrastructure.security.ownership import validate_session_ownership, validate_api_key_ownership


@pytest.mark.asyncio
async def test_validate_session_ownership_success(mock_db):
    """Test successful session ownership validation"""
    
    @validate_session_ownership
    async def dummy_func(session_id, user_id, db):
        return "success"
    
    # Mock session repository
    from src.infrastructure.database.session_repository import SessionRepository
    SessionRepository.get_by_id = Mock(return_value=Mock(user_id="user123"))
    
    result = await dummy_func(session_id="session123", user_id="user123", db=mock_db)
    assert result == "success"


@pytest.mark.asyncio
async def test_validate_session_ownership_unauthorized(mock_db):
    """Test unauthorized access to session"""
    
    @validate_session_ownership
    async def dummy_func(session_id, user_id, db):
        return "success"
    
    from src.infrastructure.database.session_repository import SessionRepository
    SessionRepository.get_by_id = Mock(return_value=Mock(user_id="other_user"))
    
    with pytest.raises(HTTPException) as exc:
        await dummy_func(session_id="session123", user_id="user123", db=mock_db)
    
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_validate_session_ownership_not_found(mock_db):
    """Test session not found"""
    
    @validate_session_ownership
    async def dummy_func(session_id, user_id, db):
        return "success"
    
    from src.infrastructure.database.session_repository import SessionRepository
    SessionRepository.get_by_id = Mock(return_value=None)
    
    with pytest.raises(HTTPException) as exc:
        await dummy_func(session_id="invalid", user_id="user123", db=mock_db)
    
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_validate_api_key_ownership_success(mock_db):
    """Test successful API key ownership validation"""
    
    @validate_api_key_ownership
    async def dummy_func(key, current_user, db):
        return "success"
    
    from src.infrastructure.database.api_key_repository import APIKeyRepository
    APIKeyRepository.get_by_key = Mock(return_value=Mock(user_id="user123"))
    
    result = await dummy_func(
        key="key123",
        current_user={"user_id": "user123"},
        db=mock_db
    )
    assert result == "success"


@pytest.mark.asyncio
async def test_validate_api_key_ownership_unauthorized(mock_db):
    """Test unauthorized access to API key"""
    
    @validate_api_key_ownership
    async def dummy_func(key, current_user, db):
        return "success"
    
    from src.infrastructure.database.api_key_repository import APIKeyRepository
    APIKeyRepository.get_by_key = Mock(return_value=Mock(user_id="other_user"))
    
    with pytest.raises(HTTPException) as exc:
        await dummy_func(
            key="key123",
            current_user={"user_id": "user123"},
            db=mock_db
        )
    
    assert exc.value.status_code == 403


@pytest.fixture
def mock_db():
    return Mock()
