import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    def __init__(self, requests: int = 60, per_seconds: int = 60):
        self.requests = requests
        self.per_seconds = per_seconds
        self.store = defaultdict(list)  # ip -> list[timestamps]
        self.lock = Lock()

    def allow(self, key: str):
        now = time.time()
        with self.lock:
            q = self.store[key]
            # remove old
            while q and q[0] <= now - self.per_seconds:
                q.pop(0)
            if len(q) >= self.requests:
                return False, 0
            q.append(now)
            remaining = self.requests - len(q)
            return True, remaining
