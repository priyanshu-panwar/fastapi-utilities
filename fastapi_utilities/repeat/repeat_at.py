import asyncio
import logging
import typing

from datetime import datetime
from functools import wraps
from asyncio import ensure_future
from starlette.concurrency import run_in_threadpool
from croniter import croniter

_FuncType = typing.TypeVar("_FuncType", bound=typing.Callable)


def get_delta(cron: str) -> float:
    """
    Returns the time delta between now and the next cron execution time.
    """
    now = datetime.now()
    cron = croniter(cron, now)
    return (cron.get_next(datetime) - now).total_seconds()

def repeat_at(
    *,
    cron: str,
    logger: logging.Logger = None,
    raise_exceptions: bool = False,
    max_repetitions: int = None,
) -> typing.Callable[[_FuncType], _FuncType]:
    """
    Decorator to schedule a function's execution based on a cron expression.

    Parameters:
    -----------
    cron: str
        Cron-style string for periodic execution, e.g., '0 0 * * *' for every midnight.
    logger: logging.Logger (default None)
        Logger object to log exceptions.
    raise_exceptions: bool (default False)
        Whether to raise exceptions or log them.
    max_repetitions: int (default None)
        Maximum number of times to repeat the function. If None, repeats indefinitely.
    """

    def decorator(func: _FuncType) -> _FuncType:
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            repetitions = 0
            if not croniter.is_valid(cron):
                raise ValueError(f"Invalid cron expression: '{cron}'")

            while max_repetitions is None or repetitions < max_repetitions:
                try:
                    sleep_time = get_delta(cron)
                    await asyncio.sleep(sleep_time)
                    await func(*args, **kwargs)
                except Exception as e:
                    if logger:
                        logger.exception(e)
                    if raise_exceptions:
                        raise e
                repetitions += 1

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            repetitions = 0
            if not croniter.is_valid(cron):
                raise ValueError(f"Invalid cron expression: '{cron}'")

            async def loop():
                nonlocal repetitions
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        sleep_time = get_delta(cron)
                        await asyncio.sleep(sleep_time)
                        await run_in_threadpool(func, *args, **kwargs)
                    except Exception as e:
                        if logger:
                            logger.exception(e)
                        if raise_exceptions:
                            raise e
                    repetitions += 1

            ensure_future(loop())

        # Return the appropriate wrapper based on the function type
        return async_wrapper if is_coroutine else sync_wrapper

    return decorator
