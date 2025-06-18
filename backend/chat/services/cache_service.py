import redis
from config import settings
import json
from functools import wraps



class CacheService:
    def __init__(self):
        self.client = redis.from_url(settings.redis_url)

    def get(self, key: str):
        val = self.client.get(key)
        return json.loads(val) if val else None

    def set(self, key: str, value, ttl: int = 3600):
        self.client.set(key, json.dumps(value), ex=ttl)

    def cached(self, ttl: int = 3600):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cached = self.get(cache_key)
                if cached:
                    return cached
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator

cache = CacheService()