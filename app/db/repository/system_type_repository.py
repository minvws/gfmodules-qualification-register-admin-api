import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import SystemType

logger = logging.getLogger(__name__)


class SystemTypeRepository(RepositoryBase[SystemType]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (SystemType.created_at.desc(),)
