from typing import List, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """
    Schema for pagination of entities in the application.
    """

    items: List[T]
    limit: int
    offset: int
    total: int
