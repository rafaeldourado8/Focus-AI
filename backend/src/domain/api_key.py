"""
API Key Entity

Domain model for API keys used in public API
"""

from datetime import datetime
from typing import Optional


class APIKey:
    """API Key domain entity"""
    
    # Plans
    PLAN_FREE = "free"
    PLAN_PRO = "pro"
    PLAN_ENTERPRISE = "enterprise"
    
    # Rate limits (requests per minute)
    RATE_LIMITS = {
        PLAN_FREE: 10,
        PLAN_PRO: 60,
        PLAN_ENTERPRISE: 300
    }
    
    # Daily limits
    DAILY_LIMITS = {
        PLAN_FREE: 100,
        PLAN_PRO: 10000,
        PLAN_ENTERPRISE: None  # Unlimited
    }
    
    def __init__(
        self,
        key: str,
        user_id: int,
        name: str,
        plan: str = PLAN_FREE,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        last_used_at: Optional[datetime] = None,
        usage_count: int = 0
    ):
        self.key = key
        self.user_id = user_id
        self.name = name
        self.plan = plan
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.expires_at = expires_at
        self.last_used_at = last_used_at
        self.usage_count = usage_count
    
    def get_rate_limit(self) -> int:
        """Get rate limit for this key's plan"""
        return self.RATE_LIMITS.get(self.plan, self.RATE_LIMITS[self.PLAN_FREE])
    
    def get_daily_limit(self) -> Optional[int]:
        """Get daily limit for this key's plan"""
        return self.DAILY_LIMITS.get(self.plan)
    
    def is_valid(self) -> bool:
        """Check if key is valid"""
        if not self.is_active:
            return False
        
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        
        return True
    
    def increment_usage(self):
        """Increment usage counter"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
