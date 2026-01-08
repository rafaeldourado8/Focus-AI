import redis
from typing import Optional, List
import json
import hashlib
from src.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class CacheService:
    """Redis cache service with distributed locks and intelligent TTL"""
    
    # TTL constants (seconds)
    TTL_LOCK = 180           # 3 minutes
    TTL_ANSWER = 604800      # 7 days (technical answers)
    TTL_CONTEXT = 3600       # 1 hour
    TTL_SESSION = 86400      # 24 hours
    
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    # Distributed Lock
    def acquire_lock(self, key: str, ttl: int = None) -> bool:
        """Acquire distributed lock"""
        ttl = ttl or self.TTL_LOCK
        acquired = self.client.set(f"lock:{key}", "1", nx=True, ex=ttl)
        if acquired:
            logger.info(f"Lock acquired: {key}")
        return acquired
    
    def release_lock(self, key: str) -> bool:
        """Release distributed lock"""
        released = self.client.delete(f"lock:{key}") > 0
        if released:
            logger.info(f"Lock released: {key}")
        return released
    
    def is_locked(self, key: str) -> bool:
        """Check if key is locked"""
        return self.client.exists(f"lock:{key}") > 0
    
    # Generic Cache
    def set(self, key: str, value: str, ttl: Optional[int] = None):
        """Set cache value"""
        if ttl:
            self.client.setex(key, ttl, value)
        else:
            self.client.set(key, value)
    
    def get(self, key: str) -> Optional[str]:
        """Get cache value"""
        return self.client.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete cache key"""
        return self.client.delete(key) > 0
    
    # Answer Cache
    def cache_answer(self, question: str, answer: dict, ttl: int = None):
        """Cache LLM answer with hash key"""
        ttl = ttl or self.TTL_ANSWER
        question_hash = self._hash_question(question)
        self.client.setex(f"answer:{question_hash}", ttl, json.dumps(answer))
        logger.info(f"Answer cached: {question_hash[:8]}... (TTL: {ttl}s)")
    
    def get_cached_answer(self, question: str) -> Optional[dict]:
        """Get cached answer by question hash"""
        question_hash = self._hash_question(question)
        cached = self.client.get(f"answer:{question_hash}")
        if cached:
            logger.info(f"Cache hit: {question_hash[:8]}...")
            return json.loads(cached)
        return None
    
    # Context Cache
    def cache_context(self, session_id: str, messages: List[dict], ttl: int = None):
        """Cache conversation context"""
        ttl = ttl or self.TTL_CONTEXT
        self.client.setex(f"context:{session_id}", ttl, json.dumps(messages))
        logger.info(f"Context cached: {session_id} ({len(messages)} messages)")
    
    def get_cached_context(self, session_id: str) -> Optional[List[dict]]:
        """Get cached conversation context"""
        cached = self.client.get(f"context:{session_id}")
        if cached:
            logger.info(f"Context hit: {session_id}")
            return json.loads(cached)
        return None
    
    def invalidate_context(self, session_id: str) -> bool:
        """Invalidate session context"""
        return self.delete(f"context:{session_id}")
    
    # Cache Invalidation
    def invalidate_by_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        keys = self.client.keys(pattern)
        if keys:
            deleted = self.client.delete(*keys)
            logger.info(f"Invalidated {deleted} keys matching: {pattern}")
            return deleted
        return 0
    
    def invalidate_by_version(self, version: str):
        """Invalidate cache by model version"""
        return self.invalidate_by_pattern(f"answer:*:v{version}")
    
    # Helpers
    def _hash_question(self, question: str) -> str:
        """Generate hash for question (cache key)"""
        return hashlib.sha256(question.lower().strip().encode()).hexdigest()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        info = self.client.info("stats")
        return {
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": self._calculate_hit_rate(info)
        }
    
    def _calculate_hit_rate(self, info: dict) -> float:
        """Calculate cache hit rate"""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        return round((hits / total * 100) if total > 0 else 0, 2)