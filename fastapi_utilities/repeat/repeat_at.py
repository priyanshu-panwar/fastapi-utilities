import asyncio
import logging

from datetime import datetime
from functools import wraps
from asyncio import ensure_future
from starlette.concurrency import run_in_threadpool
from croniter import croniter


def get_delta(cron):
    """
    This function returns the time delta between now and the next cron execution time.
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
):
    """
    This function returns a decorator that makes a function execute periodically as per the cron expression provided.

    :: Params ::
    ------------
    cron: str
        Cron-style string for periodic execution, eg. '0 0 * * *' every midnight
    logger: logging.Logger (default None)
        Logger object to log exceptions
    raise_exceptions: bool (default False)
        Whether to raise exceptions or log them
    max_repetitions: int (default None)
        Maximum number of times to repeat the function. If None, repeat indefinitely.

    """

    def decorator(func):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            repititions = 0
            if not croniter.is_valid(cron):
                raise ValueError(f"Invalid cron expression: '{cron}'")

            async def loop(*args, **kwargs):
                nonlocal repititions
                while max_repetitions is None or repititions < max_repetitions:
                    try:
                        sleepTime = get_delta(cron)
                        await asyncio.sleep(sleepTime)
                        if is_coroutine:
                            await func(*args, **kwargs)
                        else:
                            await run_in_threadpool(func, *args, **kwargs)
                    except Exception as e:
                        if logger is not None:
                            logger.exception(e)
                        if raise_exceptions:
                            raise e
                    repititions += 1

            ensure_future(loop(*args, **kwargs))

        return wrapper

    return decorator
