# Define all the router here.

from fastapi import APIRouter
from .module1.views import router as module1_router

router = APIRouter()
router.include_router(module1_router)
