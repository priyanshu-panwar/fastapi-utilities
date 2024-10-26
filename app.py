from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_utilities.repeat import repeat_every, repeat_at

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    await test()
    test2()
    yield
    # --- shutdown ---

app = FastAPI(lifespan=lifespan)

# Repeat Every Example
@repeat_every(seconds=2)
async def test():
    print("test")

# Repeat At Example
@repeat_at(cron="* * * * *")
def test2():
    print("test2")