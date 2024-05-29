import logging
from sqlite3 import DatabaseError
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.decorator import repository
from app.db.entities.application import Application

from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(Application)
class ApplicationsRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> Application | None:
        try:
            db_application = self.session.scalars(
                select(Application)
                .options(
                    selectinload(Application.versions),
                    selectinload(Application.roles),
                    selectinload(Application.system_types),
                )
                .filter_by(**kwargs)
            ).first()
            return db_application
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_many(self, **kwargs: TArgs) -> Sequence[Application]:
        db_applications = self.session.scalars(
            select(Application)
            .options(
                selectinload(Application.roles), selectinload(Application.versions)
            )
            .filter_by(**kwargs)
        ).all()
        return db_applications

    def create(self, new_application: Application) -> None:
        try:
            self.session.add(new_application)
            self.session.commit()
            self.session.refresh(new_application)

        except DatabaseError as error:
            self.session.rollback()
            logger.error(error)

    def update(self, application: Application) -> None:
        try:
            self.session.commit()
            self.session.refresh(application)
        except DatabaseError as error:
            logger.error(error)
            self.session.rollback()

    def delete(self, application: Application) -> None:
        try:
            self.session.delete(application)
            self.session.commit()
        except DatabaseError as error:
            logger.error(error)
            self.session.rollback()
