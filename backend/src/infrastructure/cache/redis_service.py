import redis
from typing import Optional
import json
from src.config import get_settings

settings = get_settings()

class CacheService:
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    def acquire_lock(self, key: str, ttl: int = 180) -> bool:
        return self.client.set(f"lock:{key}", "1", nx=True, ex=ttl)
    
    def release_lock(self, key: str) -> bool:
        return self.client.delete(f"lock:{key}") > 0
    
    def is_locked(self, key: str) -> bool:
        return self.client.exists(f"lock:{key}") > 0
    
    def set(self, key: str, value: str, ttl: Optional[int] = None):
        if ttl:
            self.client.setex(key, ttl, value)
        else:
            self.client.set(key, value)
    
    def get(self, key: str) -> Optional[str]:
        return self.client.get(key)
    
    def delete(self, key: str) -> bool:
        return self.client.delete(key) > 0
    
    def cache_answer(self, question_hash: str, answer: dict, ttl: int = 3600):
        self.client.setex(f"answer:{question_hash}", ttl, json.dumps(answer))
    
    def get_cached_answer(self, question_hash: str) -> Optional[dict]:
        cached = self.client.get(f"answer:{question_hash}")
        return json.loads(cached) if cached else None