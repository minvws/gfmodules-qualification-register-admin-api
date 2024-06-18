import logging
from typing import Sequence

from sqlalchemy import select, exists
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.db.decorator import repository
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.repository.repository_base import RepositoryBase, TArgs

logger = logging.getLogger(__name__)


@repository(HealthcareProvider)
class HealthcareProviderRepository(RepositoryBase):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def find_one(self, **kwargs: TArgs) -> HealthcareProvider | None:
        try:
            db_healthcare_provider = self.session.scalars(
                select(HealthcareProvider).filter_by(**kwargs)
            ).first()
            return db_healthcare_provider
        except DatabaseError as e:
            logger.error(e)
            return None

    def find_all(
        self,
    ) -> Sequence[HealthcareProvider]:
        db_healthcare_providers = self.session.scalars(select(HealthcareProvider)).all()
        return db_healthcare_providers

    def create(self, new_healthcare_provider: HealthcareProvider) -> None:
        try:
            self.session.add(new_healthcare_provider)
            self.session.commit()
            self.session.refresh(new_healthcare_provider)
        except DatabaseError as e:
            self.session.rollback()
            logger.error(e)

    def update(self, healthcare_provider: HealthcareProvider) -> None:
        try:
            self.session.commit()
            self.session.refresh(healthcare_provider)
        except DatabaseError as e:
            self.session.rollback()
            logger.error(e)

    def delete(self, healthcare_provider: HealthcareProvider) -> None:
        try:
            self.session.delete(healthcare_provider)
            self.session.commit()
        except DatabaseError as e:
            self.session.rollback()
            logger.error(e)

    def ura_code_exists(self, ura_code: str) -> bool:
        stmt = exists(1).where(HealthcareProvider.ura_code == ura_code).select()
        result = self.session.execute(stmt).scalar()
        if isinstance(result, bool):
            return result

        raise TypeError("Incorrect return from sql statement")

    def agb_code_exists(self, agb_code: str) -> bool:
        stmt = exists(1).where(HealthcareProvider.agb_code == agb_code).select()
        result = self.session.execute(stmt).scalar()
        if isinstance(result, bool):
            return result

        raise TypeError("Incorrect return from sql statement")
