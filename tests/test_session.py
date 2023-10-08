import pytest
from pathlib import Path
import random
from _pytest.capture import CaptureFixture

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_utilities import FastAPISessionMaker

# setup
db_path = Path("./db.sqlite3")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = f"sqlite:///{db_path}"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import Column, Integer


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)


app = FastAPI()
Base.metadata.create_all(bind=engine)

# done


def test_session():
    sm = FastAPISessionMaker(DB_URL)
    with sm.context_session() as session:
        x = User(id=random.randint(0, 10000))
        session.add(x)


def test_reset_session():
    sm = FastAPISessionMaker(DB_URL)
    sm.reset_session()


def test_session_raise_error(capsys: CaptureFixture[str]) -> None:
    sm = FastAPISessionMaker(DB_URL)
    try:
        with sm.context_session() as session:
            x = User(id=1)
            session.add(x)
            x = User(id=1)
            session.add(x)
    except Exception:
        out, err = capsys.readouterr()
        assert out == ""
