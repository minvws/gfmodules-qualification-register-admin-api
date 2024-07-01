import logging


from app.db.db_session import DbSession
from app.db.entities.application_version import ApplicationVersion
from app.db.repository.repository_base import RepositoryBase


logger = logging.getLogger(__name__)


class ApplicationVersionRepository(RepositoryBase[ApplicationVersion]):
    model = ApplicationVersion

    def __init__(self, db_session: DbSession) -> None:
        super().__init__(db_session)
