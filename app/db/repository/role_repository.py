import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import Role

logger = logging.getLogger(__name__)


class RoleRepository(RepositoryBase[Role]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (Role.created_at.desc(),)
