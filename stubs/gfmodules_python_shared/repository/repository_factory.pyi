from gfmodules_python_shared.repository.repository_base import GenericRepository as GenericRepository
from gfmodules_python_shared.session.db_session import DbSession as DbSession
from sqlalchemy.orm import DeclarativeBase as DeclarativeBase
from typing import Type

class RepositoryFactory:
    @staticmethod
    def create(repo_class: Type[GenericRepository[DeclarativeBase]], session: DbSession) -> GenericRepository[DeclarativeBase]: ...
