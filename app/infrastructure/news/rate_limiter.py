import time
from threading import Lock

class RateLimiter:
    def __init__(self, min_interval=0.4):
        self.min_interval = min_interval
        self.lock = Lock()
        self.last_time = 0

    def wait(self):
        with self.lock:
            now = time.time()
            diff = now - self.last_time

            if diff < self.min_interval:
                time.sleep(self.min_interval - diff)

            self.last_time = time.time()