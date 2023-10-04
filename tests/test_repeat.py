import logging
import pytest

from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from fastapi_utilities.repeat import repeat_every


@pytest.mark.asyncio
async def test_repeat_every(capsys: CaptureFixture[str]):
    """
    Simple Test Case for repeat_every
    """

    @repeat_every(seconds=0.1, max_repetitions=3)
    async def print_hello():
        print("Hello")

    await print_hello()
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

    captured_logs = caplog.records

    assert len(captured_logs) > 0

    last_log = captured_logs[-1]  # Get the last log message
    assert last_log.levelname == "ERROR"  # Check log level
    assert "Hello" in last_log.message  # Check log message content


@pytest.mark.asyncio
async def test_repeat_every_with_raise_exceptions(caplog: LogCaptureFixture):
    """
    Test Case for repeat_every with raise_exceptions=True
    """

    @repeat_every(seconds=0.1, raise_exceptions=True, max_repetitions=3)
    async def print_hello():
        raise Exception("Hello")

    with pytest.raises(Exception) as e:
        await print_hello()

    assert str(e.value) == "Hello"
