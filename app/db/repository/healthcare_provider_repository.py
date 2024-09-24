import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument, exists

from app.db.entities import HealthcareProvider

logger = logging.getLogger(__name__)


class HealthcareProviderRepository(RepositoryBase[HealthcareProvider]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (HealthcareProvider.created_at.desc(),)

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
