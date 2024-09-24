import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import Application

logger = logging.getLogger(__name__)


class ApplicationRepository(RepositoryBase[Application]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (Application.created_at.desc(),)
