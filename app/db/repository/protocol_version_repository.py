import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import ProtocolVersion

logger = logging.getLogger(__name__)


class ProtocolVersionRepository(RepositoryBase[ProtocolVersion]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (ProtocolVersion.created_at.desc(),)
