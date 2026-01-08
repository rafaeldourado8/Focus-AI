"""
API Gateway Authentication Middleware

Handles API key validation and rate limiting
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.infrastructure.api_gateway.rate_limiter import RateLimiter
from src.domain.api_key import APIKey
import logging

logger = logging.getLogger(__name__)


class APIGatewayMiddleware:
    """Middleware for API Gateway authentication and rate limiting"""
    
    def __init__(self, api_key_repository):
        self.api_key_repo = api_key_repository
        self.rate_limiter = RateLimiter()
    
    async def authenticate(self, request: Request) -> APIKey:
        """
        Authenticate request using API key
        
        Raises:
            HTTPException: If authentication fails
        """
        # Extract API key from header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing API key"
            )
        
        # Parse Bearer token
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        api_key_value = auth_header.replace("Bearer ", "")
        
        # Validate API key
        api_key = await self.api_key_repo.get_by_key(api_key_value)
        
        if not api_key or not api_key.is_valid():
            logger.warning(f"Invalid API key attempt: {api_key_value[:8]}...")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired API key"
            )
        
        return api_key
    
    def check_rate_limit(self, api_key: APIKey) -> dict:
        """
        Check rate limit for API key
        
        Returns:
            Rate limit info dict
        
        Raises:
            HTTPException: If rate limit exceeded
        """
        limit = api_key.get_rate_limit()
        result = self.rate_limiter.check_rate_limit(api_key.key, limit)
        
        if not result["allowed"]:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(result["reset_at"]),
                    "Retry-After": str(result["reset_at"] - int(__import__("time").time()))
                }
            )
        
        return result
    
    def add_rate_limit_headers(self, response: JSONResponse, rate_info: dict, api_key: APIKey):
        """Add rate limit headers to response"""
        response.headers["X-RateLimit-Limit"] = str(api_key.get_rate_limit())
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_at"])
