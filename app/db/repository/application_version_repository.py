import logging

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.application_version import ApplicationVersion
from app.db.repository.repository_base import RepositoryBase, TArgs


logger = logging.getLogger(__name__)


@repository(ApplicationVersion)
class ApplicationVersionRepository(RepositoryBase):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> ApplicationVersion | None:
        try:
            db_application = self.session.scalars(
                select(ApplicationVersion).filter_by(**kwargs)
            ).first()
            return db_application
        except DatabaseError as e:
            logger.error(e)
            return None
