import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.protocol import Protocol
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(Protocol)
class ProtocolRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> Protocol | None:
        try:
            db_protocol = self.session.scalars(
                select(Protocol).filter_by(**kwargs)
            ).first()
            return db_protocol
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_many(self, **kwargs: TArgs) -> Sequence[Protocol]:
        db_protocols = self.session.scalars(select(Protocol).filter_by(**kwargs)).all()
        return db_protocols

    def create(self, protocol: Protocol) -> None:
        try:
            self.session.add(protocol)
            self.session.commit()
            self.session.refresh(protocol)
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()

    def delete(self, protocol: Protocol) -> None:
        try:
            self.session.delete(protocol)
            self.session.commit()
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()
