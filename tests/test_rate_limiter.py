import asyncio
import time
import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.testclient import TestClient
from fastapi_utilities import rate_limiter  # Import your decorator

# Initialize FastAPI app
app = FastAPI()


@app.get("/limited")
@rate_limiter(max_requests=2, time_window=3)
async def limited_endpoint(request: Request):
    return {"message": "Success"}


# Client for testing
client = TestClient(app)


def test_rate_limiter_allows_requests_within_limit():
    """Test if the rate limiter allows requests within the defined limit."""
    response1 = client.get("/limited")
    response2 = client.get("/limited")
    assert response1.status_code == 200
    assert response2.status_code == 200


@pytest.mark.asyncio
async def test_rate_limiter_blocks_excess_requests():
    """Test if the rate limiter blocks requests exceeding the limit."""
    await asyncio.sleep(3)
    response1 = client.get("/limited")
    response2 = client.get("/limited")
    response3 = client.get("/limited")  # This should be blocked
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 429  # Too Many Requests


@pytest.mark.asyncio
async def test_rate_limiter_resets_after_time_window():
    """Ensure the rate limiter resets the request count after the time window expires."""
    client.get("/limited")
    client.get("/limited")
    await asyncio.sleep(3)  # Wait for time window to expire
    response = client.get("/limited")
    assert response.status_code == 200  # Should allow again after reset


def test_rate_limiter_edge_case_single_request():
    """Ensure a single request is always allowed."""
    response = client.get("/limited")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rate_limiter_recovers_after_block():
    """Ensure that requests are allowed again after a user is blocked and time resets."""
    client.get("/limited")
    client.get("/limited")
    client.get("/limited")  # Blocked
    await asyncio.sleep(3)  # Wait for time window
    response = client.get("/limited")  # Should be allowed again
    assert response.status_code == 200
