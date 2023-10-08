from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class FastAPISessionMaker:
    """
    This will allow us to create a cached session maker that can be used as context manager.
    """

    def __init__(self, db_url: str):
        """
        `db_url` should be any sqlalchemy-compatible database URI.
        """
        self.db_url = db_url
        self._cached_engine: Engine = None
        self._cached_session_maker: Session = None

    def _get_db(self):
        """
        This will return a cached db connection Session.
        """
        if self._cached_engine is None:
            self._cached_engine = create_engine(self.db_url)
        if self._cached_session_maker is None:
            self._cached_session_maker = sessionmaker(
                autocommit=False, autoflush=False, bind=self._cached_engine
            )
        db = self._cached_session_maker()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @contextmanager
    def context_session(self):
        """
        A context manager that works for `get_db` dependency injection.

        Usage:
            session_maker = FastAPISessionMaker(database_uri)
            with session_maker.context_session() as session:
                session.query(...)
        """
        yield from self._get_db()

    def reset_session(self):
        """
        This will reset the sessionmaker and engine.
        """
        self._cached_session_maker = None
        self._cached_engine = None
