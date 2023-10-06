import logging
import pytest
import asyncio

from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from fastapi_utilities import repeat_every


@pytest.mark.asyncio
async def test_repeat_every(capsys: CaptureFixture[str]):
    """
    Simple Test Case for repeat_every
    """

    @repeat_every(seconds=0.1, max_repetitions=3)
    async def print_hello():
        print("Hello")

    await print_hello()
    await asyncio.sleep(0.5)
    out, err = capsys.readouterr()
    assert out == "Hello\nHello\nHello\n"
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_every_sync(capsys: CaptureFixture[str]):
    """
    Simple Test Case for repeat_every
    """

    @repeat_every(seconds=0.1, max_repetitions=3)
    def print_hello():
        print("Hello")

    await print_hello()
    await asyncio.sleep(0.5)
    out, err = capsys.readouterr()
    assert out == "Hello\nHello\nHello\n"
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_every_with_wait_first(capsys: CaptureFixture[str]):
    """
    Test Case for repeat_every with wait_first=True
    """

    @repeat_every(seconds=0.1, wait_first=True, max_repetitions=3)
    async def print_hello():
        print("Hello")

    await print_hello()
    await asyncio.sleep(0.5)
    out, err = capsys.readouterr()
    assert out == "Hello\nHello\nHello\n"
    assert err == ""


@pytest.mark.asyncio
async def test_repeat_every_with_logger(caplog: LogCaptureFixture):
    """
    Test Case for repeat_every with logger
    """

    @repeat_every(seconds=0.1, logger=logging.getLogger("test"), max_repetitions=3)
    async def print_hello():
        raise Exception("Hello")

    await print_hello()
    await asyncio.sleep(0.5)

    captured_logs = caplog.records

    assert len(captured_logs) > 0

    last_log = captured_logs[-1]  # Get the last log message
    assert last_log.levelname == "ERROR"  # Check log level
    assert "Hello" in last_log.message  # Check log message content


from asyncio import AbstractEventLoop
from typing import Any, Dict


def ignore_exception(_loop: AbstractEventLoop, _context: Dict[str, Any]) -> None:
    pass


@pytest.fixture(autouse=True)
def setup_event_loop(event_loop: AbstractEventLoop) -> None:
    event_loop.set_exception_handler(ignore_exception)


@pytest.mark.asyncio
async def test_repeat_raise_error(capsys: CaptureFixture[str]) -> None:
    logger = logging.getLogger(__name__)

    @repeat_every(
        seconds=0.07, max_repetitions=None, raise_exceptions=True, logger=logger
    )
    def raise_exc():
        raise ValueError("repeat")

    await raise_exc()
    await asyncio.sleep(0.1)
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
