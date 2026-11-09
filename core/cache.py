import redis
import os
import json
from typing import Any, Optional

class SmartCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl_seconds = ttl_seconds
        self.hits = 0
        self.misses = 0
        redis_url = os.getenv("REDIS_URL", "redis://veritas_redis_cache:6379")
        try:
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
            print("SmartCache connected to Redis successfully.")
        except Exception as e:
            print(f"SmartCache Redis connection warning: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        if not self.client:
            return None
        try:
            cached = self.client.get(f"veritas:cache:{key}")
            if cached:
                self.hits += 1
                data = json.loads(cached)
                if isinstance(data, dict):
                    data["from_cache"] = True
                return data
            else:
                self.misses += 1
        except Exception as e:
            print(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any) -> None:
        if not self.client:
            return
        try:
            val_copy = value.copy() if isinstance(value, dict) else value
            if isinstance(val_copy, dict):
                val_copy["from_cache"] = False
            self.client.setex(f"veritas:cache:{key}", self.ttl_seconds, json.dumps(val_copy))
        except Exception as e:
            print(f"Cache set error: {e}")

    def clear(self) -> None:
        if not self.client:
            return
        try:
            keys = self.client.keys("veritas:cache:*")
            if keys:
                self.client.delete(*keys)
            self.hits = 0
            self.misses = 0
        except Exception as e:
            print(f"Cache clear error: {e}")

    def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_ratio = (self.hits / total * 100) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total,
            "hit_ratio_percent": round(hit_ratio, 2)
        }

cache = SmartCache()
