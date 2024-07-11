from typing import Generator, Any

import pytest

from app.db.db import Database
from app.db.db_session import DbSession
from app.db.session_factory import DbSessionFactory


@pytest.fixture()
def session() -> Generator[DbSession, Any, None]:
    db = Database("sqlite:///:memory:")
    db.generate_tables()
    session_factory = DbSessionFactory(db.engine)
    session = session_factory.create()

    yield session
