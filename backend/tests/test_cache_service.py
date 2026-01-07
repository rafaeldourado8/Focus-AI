import pytest
from unittest.mock import Mock, patch
from src.infrastructure.cache.redis_service import CacheService

@pytest.fixture
def mock_redis():
    with patch('src.infrastructure.cache.redis_service.redis.from_url') as mock:
        yield mock.return_value

def test_acquire_lock_success(mock_redis):
    mock_redis.set.return_value = True
    cache = CacheService()
    result = cache.acquire_lock("session123", ttl=180)
    assert result is True
    mock_redis.set.assert_called_once_with("lock:session123", "1", nx=True, ex=180)

def test_acquire_lock_fail(mock_redis):
    mock_redis.set.return_value = False
    cache = CacheService()
    result = cache.acquire_lock("session123")
    assert result is False

def test_release_lock(mock_redis):
    mock_redis.delete.return_value = 1
    cache = CacheService()
    result = cache.release_lock("session123")
    assert result is True
    mock_redis.delete.assert_called_once_with("lock:session123")

def test_is_locked_true(mock_redis):
    mock_redis.exists.return_value = 1
    cache = CacheService()
    result = cache.is_locked("session123")
    assert result is True

def test_is_locked_false(mock_redis):
    mock_redis.exists.return_value = 0
    cache = CacheService()
    result = cache.is_locked("session123")
    assert result is False

def test_set_with_ttl(mock_redis):
    cache = CacheService()
    cache.set("key1", "value1", ttl=60)
    mock_redis.setex.assert_called_once_with("key1", 60, "value1")

def test_set_without_ttl(mock_redis):
    cache = CacheService()
    cache.set("key1", "value1")
    mock_redis.set.assert_called_once_with("key1", "value1")

def test_get(mock_redis):
    mock_redis.get.return_value = "value1"
    cache = CacheService()
    result = cache.get("key1")
    assert result == "value1"

def test_delete(mock_redis):
    mock_redis.delete.return_value = 1
    cache = CacheService()
    result = cache.delete("key1")
    assert result is True