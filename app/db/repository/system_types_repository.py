import logging
from typing import Sequence, List

from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.system_type import SystemType
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(SystemType)
class SystemTypesRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def fine_one(self, **kwargs: TArgs) -> SystemType | None:
        try:
            db_system_type = self.session.scalars(
                select(SystemType).filter_by(**kwargs)
            ).first()
            return db_system_type
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_many(self, names: List[str]) -> Sequence[SystemType] | None:
        try:
            condition = [SystemType.name.__eq__(name) for name in names]
            stmt = select(SystemType).where(or_(*condition))
            system_types = self.session.scalars(stmt).all()
            return system_types
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_all(self) -> Sequence[SystemType]:
        db_system_types = self.session.scalars(select(SystemType)).all()
        return db_system_types

    def create(self, new_system_type: SystemType) -> None:
        try:
            self.session.add(new_system_type)
            self.session.commit()
            self.session.refresh(new_system_type)
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()

    def delete(self, system_type: SystemType) -> None:
        try:
            self.session.delete(system_type)
            self.session.commit()
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()
