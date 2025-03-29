from fastapi import FastAPI, Request

from fastapi_utilities import rate_limiter

app = FastAPI()


@app.get("/")
@rate_limiter(max_requests=1, time_window=10)
async def root(request: Request):
    return {"message": "Hello World"}


@app.get("/hello")
@rate_limiter(max_requests=2, time_window=10)
async def hello(request: Request):
    return {"message": "Hello from the hello endpoint!"}
