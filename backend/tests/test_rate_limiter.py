"""
Tests for Rate Limiter
"""

import pytest
from fastapi import HTTPException, Request
from unittest.mock import Mock, patch
from src.infrastructure.security.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_allows_first_request():
    """Test that first request is allowed"""
    limiter = RateLimiter(requests=10, window=60)
    
    with patch.object(limiter.cache.redis, 'get', return_value=None):
        with patch.object(limiter.cache.redis, 'setex') as mock_setex:
            request = Mock(spec=Request)
            request.client.host = "127.0.0.1"
            request.state = Mock()
            
            await limiter(request)
            mock_setex.assert_called_once()


@pytest.mark.asyncio
async def test_rate_limiter_allows_within_limit():
    """Test that requests within limit are allowed"""
    limiter = RateLimiter(requests=10, window=60)
    
    with patch.object(limiter.cache.redis, 'get', return_value=b'5'):
        with patch.object(limiter.cache.redis, 'incr') as mock_incr:
            request = Mock(spec=Request)
            request.client.host = "127.0.0.1"
            request.state = Mock()
            
            await limiter(request)
            mock_incr.assert_called_once()


@pytest.mark.asyncio
async def test_rate_limiter_blocks_over_limit():
    """Test that requests over limit are blocked"""
    limiter = RateLimiter(requests=10, window=60)
    
    with patch.object(limiter.cache.redis, 'get', return_value=b'10'):
        request = Mock(spec=Request)
        request.client.host = "127.0.0.1"
        request.state = Mock()
        
        with pytest.raises(HTTPException) as exc:
            await limiter(request)
        
        assert exc.value.status_code == 429
        assert "Rate limit exceeded" in exc.value.detail


@pytest.mark.asyncio
async def test_rate_limiter_uses_user_id_over_ip():
    """Test that user ID is preferred over IP"""
    limiter = RateLimiter(requests=10, window=60)
    
    with patch.object(limiter.cache.redis, 'get', return_value=None):
        with patch.object(limiter.cache.redis, 'setex') as mock_setex:
            request = Mock(spec=Request)
            request.client.host = "127.0.0.1"
            request.state = Mock(user_id="user123")
            
            await limiter(request)
            
            # Check that key uses user_id
            call_args = mock_setex.call_args[0]
            assert "user123" in call_args[0]
