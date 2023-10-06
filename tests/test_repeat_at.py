import logging
import asyncio
import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from fastapi_utilities import repeat_at


@pytest.mark.asyncio
async def test_repeat_at(capsys: CaptureFixture[str]):
    """
    Simple Test Case for repeat_at
    """

    @repeat_at(cron="* * * * *", max_repetitions=3)
    async def print_hello():
        print("Hello")

    print_hello()
    await asyncio.sleep(1)
    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""


@pytest.mark.asyncio
async def test_repeat_at_def(capsys: CaptureFixture[str]):
    """
    Simple Test Case for repeat_at
    """

    @repeat_at(cron="* * * * *", max_repetitions=3)
    def print_hello():
        print("Hello")

    print_hello()
    await asyncio.sleep(1)
    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""


@pytest.mark.asyncio
async def test_repeat_at_with_logger(caplog: LogCaptureFixture):
    """
    Test Case for repeat_at with logger
    """

    @repeat_at(cron="* * * * *", logger=logging.getLogger("test"), max_repetitions=3)
    async def print_hello():
        raise Exception("Hello")

    print_hello()
    await asyncio.sleep(60)

    captured_logs = caplog.records

    assert len(captured_logs) > 0


from asyncio import AbstractEventLoop
from typing import Any, Dict


def ignore_exception(_loop: AbstractEventLoop, _context: Dict[str, Any]) -> None:
    pass


@pytest.fixture(autouse=True)
def setup_event_loop(event_loop: AbstractEventLoop) -> None:
    event_loop.set_exception_handler(ignore_exception)


@pytest.mark.asyncio
async def test_repeat_at_exception(capsys: CaptureFixture[str]) -> None:
    """
    Test Case for repeat_at with an invalid cron expression
    """

    logger = logging.getLogger(__name__)

    @repeat_at(
        cron="* * * * *", max_repetitions=None, raise_exceptions=True, logger=logger
    )
    def raise_exc():
        raise ValueError("repeat")

    try:
        raise_exc()
        await asyncio.sleep(60)
    except ValueError:
        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""


@pytest.mark.asyncio
async def test_repeat_at_invalid_cron(capsys: CaptureFixture[str]) -> None:
    """
    Test Case for repeat_at with an invalid cron expression
    """

    logger = logging.getLogger(__name__)

    @repeat_at(
        cron="invalid", max_repetitions=None, raise_exceptions=True, logger=logger
    )
    def raise_exc():
        raise ValueError("repeat")

    try:
        await raise_exc()
        await asyncio.sleep(60)
    except ValueError:
        out, err = capsys.readouterr()
        assert out == ""
        assert err == ""
