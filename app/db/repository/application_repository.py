import logging

from gfmodules_python_shared.repository.repository_base import RepositoryBase
from gfmodules_python_shared.session.db_session import DbSession

from app.db.entities.application import Application

logger = logging.getLogger(__name__)


class ApplicationRepository(RepositoryBase[Application]):
    def __init__(self, db_session: DbSession) -> None:
        super().__init__(session=db_session, cls_model=Application)
