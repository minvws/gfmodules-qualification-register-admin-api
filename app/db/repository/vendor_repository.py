import logging
from typing import Any

from gfmodules_python_shared.repository.base import RepositoryBase
from sqlalchemy import ColumnExpressionArgument

from app.db.entities import Vendor

logger = logging.getLogger(__name__)


class VendorRepository(RepositoryBase[Vendor]):
    @property
    def order_by(self) -> tuple[ColumnExpressionArgument[Any] | str, ...]:
        return (Vendor.created_at.desc(),)
