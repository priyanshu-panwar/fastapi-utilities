import logging
import pytest
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from _pytest.capture import CaptureFixture
from fastapi_utilities import add_timer_middleware

app = FastAPI()
add_timer_middleware(app, show_avg=True, reset_after=1)


@app.get("/")
def root():
    pass


client = TestClient(app)


def test_timer_middleware(capsys: CaptureFixture[str]) -> None:
    client.get("/")
    out, err = capsys.readouterr()
    assert err == ""
