import logging


from app.db.db_session import DbSession
from app.db.entities.role import Role
from app.db.repository.repository_base import RepositoryBase

logger = logging.getLogger(__name__)


class RoleRepository(RepositoryBase[Role]):
    model = Role

    def __init__(self, db_session: DbSession) -> None:
        super().__init__(db_session)
