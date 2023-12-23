# Define database connection here

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import constants

engine = create_engine(
    constants.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
