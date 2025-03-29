import time
from fastapi import Request, HTTPException
from functools import wraps
from typing import Dict, Callable, Tuple

# Store the latest request timestamp and request count per client IP
request_logs: Dict[str, Tuple[float, int]] = {}


def rate_limiter(max_requests: int, time_window: int):
    """
    Decorator to apply rate limiting.
    :param max_requests: Maximum requests allowed per time window.
    :param time_window: Time window in seconds.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host  # Get client IP
            current_time = time.time()

            if client_ip not in request_logs:
                request_logs[client_ip] = (current_time, 1)
            else:
                first_request_time, request_count = request_logs[client_ip]
                if current_time - first_request_time < time_window:
                    if request_count >= max_requests:
                        raise HTTPException(
                            status_code=429, detail="Too many requests, slow down!"
                        )
                    request_logs[client_ip] = (first_request_time, request_count + 1)
                else:
                    # Reset the counter after the time window expires
                    request_logs[client_ip] = (current_time, 1)

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
