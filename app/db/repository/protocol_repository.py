import logging


from app.db.db_session import DbSession
from app.db.entities.protocol import Protocol
from app.db.repository.repository_base import RepositoryBase

logger = logging.getLogger(__name__)


class ProtocolRepository(RepositoryBase[Protocol]):
    model = Protocol

    def __init__(self, db_session: DbSession) -> None:
        super().__init__(db_session)
