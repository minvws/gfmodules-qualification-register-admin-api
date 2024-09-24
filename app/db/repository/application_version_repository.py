import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import ApplicationVersion


logger = logging.getLogger(__name__)


class ApplicationVersionRepository(RepositoryBase[ApplicationVersion]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (ApplicationVersion.created_at.desc(),)
