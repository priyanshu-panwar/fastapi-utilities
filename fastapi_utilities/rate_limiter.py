import time
from typing import Callable, Dict
from fastapi import Request, HTTPException
from functools import wraps

class RateLimiter:
    def __init__(self, rate: int, per: int):
        self.rate = rate
        self.per = per
        self.allowance: Dict[str, float] = {}
        self.last_check: Dict[str, float] = {}

    def is_allowed(self, key: str) -> bool:
        current = time.time()
        if key not in self.allowance:
            self.allowance[key] = self.rate
            self.last_check[key] = current

        time_passed = current - self.last_check[key]
        self.last_check[key] = current
        self.allowance[key] += time_passed * (self.rate / self.per)

        if self.allowance[key] > self.rate:
            self.allowance[key] = self.rate

        if self.allowance[key] < 1.0:
            return False
        else:
            self.allowance[key] -= 1.0
            return True

def rate_limit(rate: int, per: int) -> Callable:
    limiter = RateLimiter(rate, per)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            if not limiter.is_allowed(client_ip):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
