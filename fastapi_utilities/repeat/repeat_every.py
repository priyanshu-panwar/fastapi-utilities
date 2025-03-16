import asyncio
import logging
import typing

from functools import wraps
from asyncio import ensure_future
from starlette.concurrency import run_in_threadpool


_FuncType = typing.TypeVar("_FuncType", bound=typing.Callable)


def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    logger: logging.Logger = None,
    raise_exceptions: bool = False,
    max_repetitions: int = None,
) -> typing.Callable[[_FuncType], _FuncType]:
    """
    This function returns a decorator that schedules a function to execute periodically after every `seconds` seconds.

    :: Params ::
    ------------
    seconds: float
        The number of seconds to wait before executing the function again.
    wait_first: bool (default False)
        Whether to wait `seconds` seconds before executing the function for the first time.
    logger: logging.Logger (default None)
        The logger to use for logging exceptions.
    raise_exceptions: bool (default False)
        Whether to raise exceptions instead of logging them.
    max_repetitions: int (default None)
        The maximum number of times to repeat the function. If None, the function will repeat indefinitely.
    """

    def decorator(func: _FuncType) -> _FuncType:
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            repetitions = 0

            async def loop(*args, **kwargs):
                nonlocal repetitions
                if wait_first:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if is_coroutine:
                            await func(*args, **kwargs)
                        else:
                            await run_in_threadpool(func, *args, **kwargs)
                    except Exception as e:
                        if logger is not None:
                            logger.exception(e)
                        if raise_exceptions:
                            raise e
                    repetitions += 1
                    await asyncio.sleep(seconds)

            ensure_future(loop(*args, **kwargs))

        return wrapper

    return decorator
