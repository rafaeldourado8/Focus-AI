"""
Unit tests for Redis Cache Service

Tests cover:
- Distributed locks
- Answer caching
- Context caching
- Cache invalidation
- Statistics
"""

import pytest
from unittest.mock import Mock, patch
from src.infrastructure.cache.redis_service import CacheService


class TestDistributedLock:
    """Test distributed lock functionality"""
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_acquire_lock_success(self, mock_redis):
        mock_client = Mock()
        mock_client.set.return_value = True
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.acquire_lock("test_key")
        
        assert result is True
        mock_client.set.assert_called_once()
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_acquire_lock_already_locked(self, mock_redis):
        mock_client = Mock()
        mock_client.set.return_value = False
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.acquire_lock("test_key")
        
        assert result is False
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_release_lock(self, mock_redis):
        mock_client = Mock()
        mock_client.delete.return_value = 1
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.release_lock("test_key")
        
        assert result is True
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_is_locked(self, mock_redis):
        mock_client = Mock()
        mock_client.exists.return_value = 1
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.is_locked("test_key")
        
        assert result is True


class TestAnswerCache:
    """Test answer caching functionality"""
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_cache_answer(self, mock_redis):
        mock_client = Mock()
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        question = "How to use async/await?"
        answer = {"content": "Use async def...", "model": "cerberus-pro"}
        
        cache.cache_answer(question, answer)
        
        mock_client.setex.assert_called_once()
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_get_cached_answer_hit(self, mock_redis):
        mock_client = Mock()
        mock_client.get.return_value = '{"content": "cached", "model": "cerberus-lite"}'
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.get_cached_answer("test question")
        
        assert result is not None
        assert result["content"] == "cached"
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_get_cached_answer_miss(self, mock_redis):
        mock_client = Mock()
        mock_client.get.return_value = None
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.get_cached_answer("test question")
        
        assert result is None
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_hash_question_consistency(self, mock_redis):
        mock_redis.return_value = Mock()
        
        cache = CacheService()
        hash1 = cache._hash_question("Test Question")
        hash2 = cache._hash_question("test question")
        hash3 = cache._hash_question("  Test Question  ")
        
        assert hash1 == hash2 == hash3


class TestContextCache:
    """Test context caching functionality"""
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_cache_context(self, mock_redis):
        mock_client = Mock()
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"}
        ]
        
        cache.cache_context("session_123", messages)
        
        mock_client.setex.assert_called_once()
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_get_cached_context(self, mock_redis):
        mock_client = Mock()
        mock_client.get.return_value = '[{"role": "user", "content": "test"}]'
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.get_cached_context("session_123")
        
        assert result is not None
        assert len(result) == 1
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_invalidate_context(self, mock_redis):
        mock_client = Mock()
        mock_client.delete.return_value = 1
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        result = cache.invalidate_context("session_123")
        
        assert result is True


class TestCacheInvalidation:
    """Test cache invalidation"""
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_invalidate_by_pattern(self, mock_redis):
        mock_client = Mock()
        mock_client.keys.return_value = ["key1", "key2", "key3"]
        mock_client.delete.return_value = 3
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        deleted = cache.invalidate_by_pattern("answer:*")
        
        assert deleted == 3
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_invalidate_by_version(self, mock_redis):
        mock_client = Mock()
        mock_client.keys.return_value = []
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        deleted = cache.invalidate_by_version("1.0")
        
        assert deleted == 0


class TestCacheStats:
    """Test cache statistics"""
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_get_stats(self, mock_redis):
        mock_client = Mock()
        mock_client.info.return_value = {
            "keyspace_hits": 80,
            "keyspace_misses": 20
        }
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        stats = cache.get_stats()
        
        assert stats["hits"] == 80
        assert stats["misses"] == 20
        assert stats["hit_rate"] == 80.0
    
    @patch('src.infrastructure.cache.redis_service.redis.from_url')
    def test_hit_rate_zero_total(self, mock_redis):
        mock_client = Mock()
        mock_client.info.return_value = {
            "keyspace_hits": 0,
            "keyspace_misses": 0
        }
        mock_redis.return_value = mock_client
        
        cache = CacheService()
        stats = cache.get_stats()
        
        assert stats["hit_rate"] == 0.0


class TestTTLConstants:
    """Test TTL constants"""
    
    def test_ttl_constants_defined(self):
        assert CacheService.TTL_LOCK == 180
        assert CacheService.TTL_ANSWER == 604800
        assert CacheService.TTL_CONTEXT == 3600
        assert CacheService.TTL_SESSION == 86400
