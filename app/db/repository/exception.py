
from sqlalchemy.exc import NoResultFound

from app.db.entities.base import TBase


class EntryNotFound(NoResultFound):
    def __init__(self, model: TBase) -> None:
        super().__init__(f"No result found in {model.__name__}")
