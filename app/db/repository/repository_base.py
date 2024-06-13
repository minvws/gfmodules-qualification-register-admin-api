from typing import TypeVar, Union, Dict
from uuid import UUID

from sqlalchemy.orm import Session


class RepositoryBase:
    def __init__(self, session: Session) -> None:
        self.session = session


TRepositoryBase = TypeVar("TRepositoryBase", bound=RepositoryBase, covariant=True)

TArgs = TypeVar("TArgs", bound=Union[str, UUID, Dict[str, str]])
