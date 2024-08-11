import time

class Cache:
    def _init_(self):
        self.cache = {}
        self.expiration = {}

    def set(self, key, value, expirationInSeconds):
        self.cache[key] = value
        self.expiration[key] = time.time() + expirationInSeconds

    def get(self, key):
        if key not in self.cache:
            return None
        if time.time() > self.expiration[key]:
            del self.cache[key]
            del self.expiration[key]
            return None
        return self.cache[key]
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
            del self.expiration[key]

    def clear(self):
        self.cache = {}
        self.expiration = {}