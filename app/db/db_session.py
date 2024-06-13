import logging
from typing import Type

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.decorator import repository_registry
from app.db.entities.base import Base
from app.db.repository.repository_base import TRepositoryBase

logger = logging.getLogger(__name__)


class DbSession(object):
    def __init__(self, engine: Engine) -> None:
        self._session = Session(engine, expire_on_commit=False)

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, new_session: Session) -> None:
        self._session = new_session

    def get_repository(self, model_class: Type[Base]) -> TRepositoryBase:  # type: ignore
        """
        Returns an instantiated repository for the given model class

        :param model_class:
        :return:
        """
        repo_class = repository_registry.get(model_class)
        if repo_class:
            return repo_class(self.session)  # type: ignore
        raise ValueError(f"No repository registered for model {model_class}")
