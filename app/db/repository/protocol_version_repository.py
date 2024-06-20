import logging

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.protocol_version import ProtocolVersion
from app.db.repository.repository_base import TArgs, RepositoryBase

logger = logging.getLogger(__name__)


@repository(ProtocolVersion)
class ProtocolVersionRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> ProtocolVersion | None:
        try:
            db_protocol_version = self.session.scalars(
                select(ProtocolVersion).filter_by(**kwargs)
            ).first()
            return db_protocol_version
        except DatabaseError as e:
            logger.error(e)
            return None

    def update(self, protocol_version: ProtocolVersion) -> None:
        try:
            self.session.commit()
            self.session.refresh(protocol_version)
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()
