from typing import Sequence, List
from uuid import UUID

from app.db.entities.system_type import SystemType
from app.db.repository.system_types_repository import SystemTypesRepository
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    SystemTypeNotFoundException,
    SystemTypeAlreadyExistsException,
)
from app.factory.system_type_factory import SystemTypeFactory
from app.helpers.validators import validated_sets_equal


class SystemTypeService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.repository_factory = repository_factory

    def get_all(self) -> Sequence[SystemType]:
        db_session = self.db_session_factory.create()
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
            system_types = system_type_repository.get_all()

        return system_types

    def get_one(self, system_type_id: UUID) -> SystemType:
        db_session = self.db_session_factory.create()
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
            system_type = system_type_repository.get(id=system_type_id)
            if system_type is None:
                raise SystemTypeNotFoundException()

        return system_type

    def add_one(self, name: str, description: str) -> SystemType:
        db_session = self.db_session_factory.create()
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
            system_type = system_type_repository.get(name=name)
            if system_type is not None:
                raise SystemTypeAlreadyExistsException()

            new_system_type = SystemTypeFactory.create_instance(
                name=name, description=description
            )
            system_type_repository.create(new_system_type)

        return new_system_type

    def delete_one(self, system_type_id: UUID) -> SystemType:
        db_session = self.db_session_factory.create()
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
            system_type = system_type_repository.get(id=system_type_id)
            if system_type is None:
                raise SystemTypeNotFoundException()

            system_type_repository.delete(system_type)

        return system_type

    def get_many_by_names(self, system_type_names: List[str]) -> Sequence[SystemType]:
        db_session = self.db_session_factory.create()
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
            system_types = system_type_repository.get_by_property(
                attribute="name",
                values=system_type_names
            )
            if system_types is None:
                raise SystemTypeNotFoundException()

            valid_system_types = validated_sets_equal(
                system_type_names, [system_type.name for system_type in system_types]
            )
            if not valid_system_types:
                raise SystemTypeNotFoundException()

        return system_types
