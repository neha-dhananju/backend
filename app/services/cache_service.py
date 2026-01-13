import time

class CacheService:
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        item = self.cache.get(key)
        if not item:
            return None

        value, expiry = item
        if expiry < time.time():
            del self.cache[key]
            return None

        return value

    def set(self, key: str, value, ttl: int = 3600):
        self.cache[key] = (value, time.time() + ttl)
