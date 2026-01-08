"""
Unit tests for Rate Limiter

Tests cover:
- Rate limit checking
- Sliding window
- Reset functionality
- Multiple keys
"""

import pytest
from unittest.mock import Mock, patch
import time
from src.infrastructure.api_gateway.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test rate limiter functionality"""
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_first_request_allowed(self, mock_redis):
        """Test first request is always allowed"""
        mock_client = Mock()
        mock_client.zcard.return_value = 0
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        result = limiter.check_rate_limit("test_key", 10)
        
        assert result["allowed"] is True
        assert result["remaining"] == 9
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_within_limit(self, mock_redis):
        """Test requests within limit are allowed"""
        mock_client = Mock()
        mock_client.zcard.return_value = 5
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        result = limiter.check_rate_limit("test_key", 10)
        
        assert result["allowed"] is True
        assert result["remaining"] == 4
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_limit_exceeded(self, mock_redis):
        """Test rate limit exceeded"""
        mock_client = Mock()
        mock_client.zcard.return_value = 10
        mock_client.zrange.return_value = [(str(time.time()), time.time())]
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        result = limiter.check_rate_limit("test_key", 10)
        
        assert result["allowed"] is False
        assert result["remaining"] == 0
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_reset_limit(self, mock_redis):
        """Test resetting rate limit"""
        mock_client = Mock()
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        limiter.reset_limit("test_key")
        
        mock_client.delete.assert_called_once_with("ratelimit:test_key")
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_different_keys_independent(self, mock_redis):
        """Test different keys have independent limits"""
        mock_client = Mock()
        mock_client.zcard.return_value = 0
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        
        result1 = limiter.check_rate_limit("key1", 10)
        result2 = limiter.check_rate_limit("key2", 10)
        
        assert result1["allowed"] is True
        assert result2["allowed"] is True
    
    @patch('src.infrastructure.api_gateway.rate_limiter.redis.from_url')
    def test_sliding_window_cleanup(self, mock_redis):
        """Test old entries are removed"""
        mock_client = Mock()
        mock_client.zcard.return_value = 5
        mock_redis.return_value = mock_client
        
        limiter = RateLimiter()
        limiter.check_rate_limit("test_key", 10, window=60)
        
        # Should call zremrangebyscore to clean old entries
        mock_client.zremrangebyscore.assert_called_once()


class TestAPIKeyEntity:
    """Test API Key entity"""
    
    def test_free_plan_rate_limit(self):
        """Test free plan has correct rate limit"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key",
            plan=APIKey.PLAN_FREE
        )
        
        assert api_key.get_rate_limit() == 10
    
    def test_pro_plan_rate_limit(self):
        """Test pro plan has correct rate limit"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key",
            plan=APIKey.PLAN_PRO
        )
        
        assert api_key.get_rate_limit() == 60
    
    def test_enterprise_plan_rate_limit(self):
        """Test enterprise plan has correct rate limit"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key",
            plan=APIKey.PLAN_ENTERPRISE
        )
        
        assert api_key.get_rate_limit() == 300
    
    def test_is_valid_active_key(self):
        """Test active key is valid"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key",
            is_active=True
        )
        
        assert api_key.is_valid() is True
    
    def test_is_valid_inactive_key(self):
        """Test inactive key is invalid"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key",
            is_active=False
        )
        
        assert api_key.is_valid() is False
    
    def test_increment_usage(self):
        """Test usage increment"""
        from src.domain.api_key import APIKey
        
        api_key = APIKey(
            key="test_key",
            user_id=1,
            name="Test Key"
        )
        
        initial_count = api_key.usage_count
        api_key.increment_usage()
        
        assert api_key.usage_count == initial_count + 1
        assert api_key.last_used_at is not None
