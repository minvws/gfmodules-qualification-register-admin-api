import logging

from gfmodules_python_shared.repository.repository_base import RepositoryBase
from gfmodules_python_shared.session.db_session import DbSession

from app.db.entities.application_version import ApplicationVersion


logger = logging.getLogger(__name__)


class ApplicationVersionRepository(RepositoryBase[ApplicationVersion]):
    def __init__(self, db_session: DbSession) -> None:
        super().__init__(session=db_session, cls_model=ApplicationVersion)
