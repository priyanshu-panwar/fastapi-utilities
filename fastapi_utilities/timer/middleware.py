"""
Based on https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/timing.py
"""

import time
from typing import Callable
from fastapi import FastAPI, Request
import logging

TIMER_PREFIX = "(fastapi-utilities)"


def add_timer_middleware(
    app: FastAPI,
    show_avg: bool = False,
    reset_after: int = 100000,
) -> None:
    """
    Add a middleware to the FastAPI app that logs the time taken to process a request.
    Optionally, also logs the average response time.
    The average response time is reset after every (reset_after)100,000 requests.

    ::Params::
    ----------
    app: FastAPI
        The FastAPI app to add the middleware to.
    show_avg: bool (default False)
        Whether to show the average response time in the logs.
    reset_after: int (default 100000)
        The number of requests after which to reset the average response time.
    """

    logger = logging.getLogger("uvicorn")

    request_counter = 0
    total_response_time = 0.0

    @app.middleware("http")
    async def timer_middleware(request: Request, call_next):
        nonlocal request_counter, total_response_time

        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f'{TIMER_PREFIX} "{request.method} - {request.url.path}" :: Time Taken :: {process_time:.2f} ms'
        )

        if show_avg:
            request_counter += 1
            total_response_time += process_time
            average_response_time = (
                total_response_time / request_counter if request_counter > 0 else 0
            )
            logger.info(f":: Average Response Time :: {average_response_time:.2f} ms")

            if request_counter % reset_after == 0:
                request_counter = 0
                total_response_time = 0.0

        return response
