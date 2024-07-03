import logging

from sqlalchemy import exists

from app.db.db_session import DbSession
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.repository.repository_base import RepositoryBase

logger = logging.getLogger(__name__)


class HealthcareProviderRepository(RepositoryBase[HealthcareProvider]):
    model = HealthcareProvider

    def __init__(self, db_session: DbSession) -> None:
        super().__init__(db_session)

    def ura_code_exists(self, ura_code: str) -> bool:
        stmt = exists(1).where(HealthcareProvider.ura_code == ura_code).select()
        result = self.session.execute_scalar(stmt)
        if isinstance(result, bool):
            return result

        raise TypeError("Incorrect return from sql statement")

    def agb_code_exists(self, agb_code: str) -> bool:
        stmt = exists(1).where(HealthcareProvider.agb_code == agb_code).select()
        result = self.session.execute_scalar(stmt)
        if isinstance(result, bool):
            return result

        raise TypeError("Incorrect return from sql statement")
