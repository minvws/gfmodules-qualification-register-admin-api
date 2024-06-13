from typing import Type

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.decorator import repository_registry
from app.db.entities.base import Base
from app.db.repository.repository_base import RepositoryBase


class RepositoryFactory:
    def __init__(self, engine: Engine) -> None:
        self.session = Session(engine)

    def get_session(self) -> Session:
        return self.session

    def get_repository(self, model_class: Type[Base]) -> Type[RepositoryBase]:
        """
        Returns an instantiated repository for the given model class

        :param model_class:
        :return:
        """
        repo_class = repository_registry.get(model_class)
        if repo_class:
            return repo_class(self.session)  # type: ignore
        raise ValueError(f"No repository registered for model {model_class}")
