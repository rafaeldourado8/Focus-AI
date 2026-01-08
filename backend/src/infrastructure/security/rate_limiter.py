"""
Rate Limiting Middleware

Prevents abuse by limiting requests per IP and User
"""

from fastapi import Request, HTTPException, status
from src.infrastructure.cache.redis_service import CacheService
import time


class RateLimiter:
    def __init__(self, requests: int = 60, window: int = 60):
        self.requests = requests
        self.window = window
        self.cache = CacheService()
    
    async def __call__(self, request: Request):
        # Get identifier (IP or User ID)
        ip = request.client.host
        user_id = request.state.user_id if hasattr(request.state, 'user_id') else None
        identifier = user_id or ip
        
        key = f"rate_limit:{identifier}"
        
        # Get current count
        current = self.cache.redis.get(key)
        
        if current is None:
            # First request in window
            self.cache.redis.setex(key, self.window, 1)
            return
        
        current = int(current)
        
        if current >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {self.window} seconds"
            )
        
        # Increment counter
        self.cache.redis.incr(key)


# Global rate limiter instances
global_rate_limiter = RateLimiter(requests=100, window=60)  # 100 req/min
strict_rate_limiter = RateLimiter(requests=10, window=60)   # 10 req/min
