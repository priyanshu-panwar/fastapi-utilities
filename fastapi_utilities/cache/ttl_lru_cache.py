from functools import lru_cache, wraps
from typing import Callable
import time


def ttl_lru_cache(ttl: int, max_size: int = 128) -> Callable:
    """
    This function is a decorator that wraps the lru_cache decorator.
    """

    def decorator(func) -> Callable:
        @lru_cache(maxsize=max_size)
        def _new(*args, __time_salt, **kwargs):
            return func(*args, **kwargs)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if ttl:
                return _new(*args, __time_salt=int(time.time() / ttl), **kwargs)
            return func(*args, **kwargs)

        wrapper.cache_clear = _new.cache_clear
        return wrapper

    return decorator
