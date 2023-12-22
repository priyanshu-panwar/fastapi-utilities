# Define your module's crud operations here

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from src import utils


async def get_all(db: Session = Depends(utils.get_db)) -> List[models.MyModel]:
    pass
