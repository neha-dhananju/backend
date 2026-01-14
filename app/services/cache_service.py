import json
import redis
from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )

    def get(self, key: str):
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value, ttl: int = 3600):
        self.redis.setex(key, ttl, json.dumps(value))

    def delete(self, key: str):
        self.redis.delete(key)
