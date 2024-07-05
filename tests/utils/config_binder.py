import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory


def config_binder(binder: inject.Binder, database: Database) -> None:
    db_session_factory = DbSessionFactory(engine=database.engine)
    repository_factory = RepositoryFactory()
    binder.bind(DbSessionFactory, db_session_factory).bind(
        RepositoryFactory, repository_factory
    )
