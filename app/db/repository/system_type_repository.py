import logging

from gfmodules_python_shared.repository.repository_base import RepositoryBase
from gfmodules_python_shared.session.db_session import DbSession

from app.db.entities.system_type import SystemType

logger = logging.getLogger(__name__)


class SystemTypeRepository(RepositoryBase[SystemType]):
    def __init__(self, db_session: DbSession) -> None:
        super().__init__(session=db_session, cls_model=SystemType)
