import inject
from gfmodules_python_shared.repository.repository_factory import RepositoryFactory
from gfmodules_python_shared.session.session_factory import DbSessionFactory

from app.db.db import Database


def config_binder(binder: inject.Binder, database: Database) -> None:
    db_session_factory = DbSessionFactory(engine=database.engine)
    repository_factory = RepositoryFactory()
    binder.bind(DbSessionFactory, db_session_factory).bind(
        RepositoryFactory, repository_factory
    )
