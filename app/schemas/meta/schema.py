from typing import List, TypeVar, Generic

from app.schemas.default import BaseModelConfig

T = TypeVar("T")


class Page(BaseModelConfig, Generic[T]):
    """
    Schema for pagination of entities in the application.
    """

    items: List[T]
    limit: int
    offset: int
    total: int
