# Sample main file

from fastapi import FastAPI
from .api import router

app = FastAPI("My App")
app.include_router(router)
