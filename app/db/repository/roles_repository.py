import logging
from typing import Sequence, List

from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.role import Role
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(Role)
class RolesRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> Role | None:
        try:
            role = self.session.scalars(select(Role).filter_by(**kwargs)).first()
            return role
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_many(self, names: List[str]) -> Sequence[Role] | None:
        try:
            condition = [Role.name.__eq__(name) for name in names]
            stmt = select(Role).where(or_(*condition))
            roles = self.session.scalars(stmt).all()
            return roles
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_all(self) -> Sequence[Role] | None:
        try:
            roles = self.session.scalars(select(Role)).all()
            return roles
        except DatabaseError as e:
            logger.error(e)
            return None

    def create(self, new_role: Role) -> Role | None:
        try:
            self.session.add(new_role)
            self.session.commit()
            self.session.refresh(new_role)
            return new_role
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()
            return None

    def update(self, role: Role) -> None:
        try:
            self.session.commit()
            self.session.refresh(role)
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()

    def delete(self, role: Role) -> Role | None:
        try:
            self.session.delete(role)
            self.session.commit()
            return role
        except DatabaseError as e:
            logger.error(e)
            self.session.rollback()
            return None
