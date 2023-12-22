# Define your module's routes here

from fastapi import APIRouter

router = APIRouter(prefix="/module1", tags=["module1"])
from . import utils, services, models


@router.get("/")
async def root():
    return {"message": "Hello World"}
