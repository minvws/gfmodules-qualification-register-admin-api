import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.models import Role
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(Role)
class RolesRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> Role | None:
        role = self.session.scalars(select(Role).filter_by(**kwargs)).first()
        return role

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
