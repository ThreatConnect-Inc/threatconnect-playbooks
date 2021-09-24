# -*- coding: utf-8 -*-
"""Throttle class to implement rate limiting"""
from threading import Lock
import time


class Throttle:
    """Throttle Class"""

    def __init__(self, rate=150, period=60, burst=0):
        """Create a throttle for a specific rate/sec"""

        self.lock = Lock()
        self.rate = rate
        self.period = period
        self.burst = max(min(burst, rate), 0)
        self.count = 0
        self.ts = None
        self.end = None

    def __call__(self):
        """Return when the throttle limit is acceptable"""

        with self.lock:
            now = time.time()
            if self.ts is None:
                self.ts = now
                self.end = now + self.period

            if now > self.end:
                self.count = 0
                # Because we do a tail sleep, the rollover will let an extra request through,
                # unless we "count" that request here
                if self.ts > (now - self.period * 2):
                    self.count += 1
                self.ts = now
                self.end = now + self.period

            self.count += 1

            if self.count <= max(self.burst, 0):
                return

            deadline = self.period / self.rate * max(self.count - 1, 0)

            if self.ts != now:
                time.sleep(max(self.ts + deadline - now, 0))


if __name__ == '__main__':
    throttle = Throttle(20, period=60, burst=10)
    for i in range(40):
        throttle()
        t = time.time()
        f = int((t - int(t)) * 1000)
        print(f'{i}: {time.strftime("%H:%M:%S",time.localtime(time.time()))}.{f}')
