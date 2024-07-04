import logging


from app.db.db_session import DbSession
from app.db.entities.system_type import SystemType
from app.db.repository.repository_base import RepositoryBase

logger = logging.getLogger(__name__)


class SystemTypesRepository(RepositoryBase[SystemType]):
    model = SystemType

    def __init__(self, db_session: DbSession) -> None:
        super().__init__(db_session)
