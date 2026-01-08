"""
Rate Limiting Service

Implements rate limiting using Redis sliding window
"""

import redis
from typing import Optional
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class RateLimiter:
    """Rate limiter using Redis sliding window"""
    
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    def check_rate_limit(self, key: str, limit: int, window: int = 60) -> dict:
        """
        Check if request is within rate limit
        
        Args:
            key: Unique identifier (e.g., API key)
            limit: Max requests allowed
            window: Time window in seconds (default 60s = 1 minute)
        
        Returns:
            {
                "allowed": bool,
                "remaining": int,
                "reset_at": int (timestamp)
            }
        """
        import time
        
        current_time = int(time.time())
        window_start = current_time - window
        
        # Redis key for this rate limit
        redis_key = f"ratelimit:{key}"
        
        # Remove old entries outside window
        self.client.zremrangebyscore(redis_key, 0, window_start)
        
        # Count requests in current window
        current_count = self.client.zcard(redis_key)
        
        if current_count < limit:
            # Add current request
            self.client.zadd(redis_key, {str(current_time): current_time})
            self.client.expire(redis_key, window)
            
            return {
                "allowed": True,
                "remaining": limit - current_count - 1,
                "reset_at": current_time + window
            }
        else:
            # Rate limit exceeded
            oldest = self.client.zrange(redis_key, 0, 0, withscores=True)
            reset_at = int(oldest[0][1]) + window if oldest else current_time + window
            
            logger.warning(f"Rate limit exceeded for key: {key}")
            
            return {
                "allowed": False,
                "remaining": 0,
                "reset_at": reset_at
            }
    
    def reset_limit(self, key: str):
        """Reset rate limit for key"""
        redis_key = f"ratelimit:{key}"
        self.client.delete(redis_key)
        logger.info(f"Rate limit reset for key: {key}")
