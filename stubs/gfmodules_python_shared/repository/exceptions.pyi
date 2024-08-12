from sqlalchemy.exc import NoResultFound
from typing import Type, TypeVar

T = TypeVar('T')

class EntryNotFound(NoResultFound):
    def __init__(self, model: Type[T]) -> None: ...
