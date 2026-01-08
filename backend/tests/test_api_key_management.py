"""
Unit tests for API Key Management

Tests cover:
- Repository CRUD operations
- Key generation
- Rotation
- Usage tracking
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.infrastructure.database.api_key_repository import APIKeyRepository
from src.infrastructure.database.api_key_model import APIKeyModel
from src.domain.api_key import APIKey


class TestAPIKeyRepository:
    """Test API key repository"""
    
    def test_create_api_key(self):
        """Test creating API key"""
        mock_db = Mock()
        repo = APIKeyRepository(mock_db)
        
        api_key = repo.create(user_id=1, name="Test Key", plan="free")
        
        assert api_key.key.startswith("ck_test_")
        assert api_key.user_id == 1
        assert api_key.name == "Test Key"
        assert api_key.plan == "free"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_create_pro_key_prefix(self):
        """Test pro key has live prefix"""
        mock_db = Mock()
        repo = APIKeyRepository(mock_db)
        
        api_key = repo.create(user_id=1, name="Pro Key", plan="pro")
        
        assert api_key.key.startswith("ck_live_")
    
    def test_get_by_key(self):
        """Test getting key by value"""
        mock_db = Mock()
        mock_db_key = APIKeyModel(
            key="test_key",
            user_id=1,
            name="Test",
            plan="free",
            is_active=True,
            usage_count=0
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_db_key
        
        repo = APIKeyRepository(mock_db)
        api_key = repo.get_by_key("test_key")
        
        assert api_key is not None
        assert api_key.key == "test_key"
    
    def test_get_by_user(self):
        """Test getting all keys for user"""
        mock_db = Mock()
        mock_keys = [
            APIKeyModel(key="key1", user_id=1, name="Key 1", plan="free", is_active=True, usage_count=0),
            APIKeyModel(key="key2", user_id=1, name="Key 2", plan="pro", is_active=True, usage_count=0)
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_keys
        
        repo = APIKeyRepository(mock_db)
        keys = repo.get_by_user(1)
        
        assert len(keys) == 2
    
    def test_deactivate_key(self):
        """Test deactivating key"""
        mock_db = Mock()
        mock_db_key = APIKeyModel(
            key="test_key",
            user_id=1,
            name="Test",
            plan="free",
            is_active=True,
            usage_count=0
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_db_key
        
        repo = APIKeyRepository(mock_db)
        result = repo.deactivate("test_key")
        
        assert result is True
        assert mock_db_key.is_active is False
        mock_db.commit.assert_called_once()
    
    def test_rotate_key(self):
        """Test key rotation"""
        mock_db = Mock()
        mock_db_key = APIKeyModel(
            key="old_key",
            user_id=1,
            name="Test",
            plan="pro",
            is_active=True,
            usage_count=10
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_db_key
        
        repo = APIKeyRepository(mock_db)
        new_key = repo.rotate("old_key")
        
        assert new_key is not None
        assert new_key.key != "old_key"
        assert new_key.plan == "pro"
    
    def test_increment_usage(self):
        """Test incrementing usage"""
        mock_db = Mock()
        mock_db_key = APIKeyModel(
            key="test_key",
            user_id=1,
            name="Test",
            plan="free",
            is_active=True,
            usage_count=5
        )
        mock_db.query.return_value.filter.return_value.first.return_value = mock_db_key
        
        repo = APIKeyRepository(mock_db)
        repo.increment_usage("test_key")
        
        assert mock_db_key.usage_count == 6
        assert mock_db_key.last_used_at is not None
        mock_db.commit.assert_called_once()


class TestKeyGeneration:
    """Test key generation"""
    
    def test_key_is_secure(self):
        """Test generated keys are secure"""
        mock_db = Mock()
        repo = APIKeyRepository(mock_db)
        
        key1 = repo.create(user_id=1, name="Key 1", plan="free")
        key2 = repo.create(user_id=1, name="Key 2", plan="free")
        
        # Keys should be different
        assert key1.key != key2.key
        
        # Keys should be long enough
        assert len(key1.key) > 40
    
    def test_key_format(self):
        """Test key format is correct"""
        mock_db = Mock()
        repo = APIKeyRepository(mock_db)
        
        free_key = repo.create(user_id=1, name="Free", plan="free")
        pro_key = repo.create(user_id=1, name="Pro", plan="pro")
        
        assert free_key.key.startswith("ck_test_")
        assert pro_key.key.startswith("ck_live_")
