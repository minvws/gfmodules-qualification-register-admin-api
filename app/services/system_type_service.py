from typing import Sequence, List
from uuid import UUID

from app.db.entities.system_type import SystemType
from app.db.repository.system_types_repository import SystemTypesRepository
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import SystemTypeNotFoundException
from app.factory.system_type_factory import SystemTypeFactory
from app.helpers.validators import validated_sets_equal


class SystemTypeService:
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def get_all_system_types(self) -> Sequence[SystemType]:
        db_session = self.db_session_factory.create()
        system_types_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            system_types = system_types_repository.find_all()

        return system_types

    def get_one_by_id(self, system_type_id: UUID) -> SystemType:
        db_session = self.db_session_factory.create()
        system_types_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            system_type = system_types_repository.fine_one(id=system_type_id)
            if system_type is None:
                raise SystemTypeNotFoundException()

        return system_type

    def add_one_system_type(self, name: str, description: str) -> SystemType:
        db_session = self.db_session_factory.create()
        session = db_session.session
        with session:
            new_system_type = SystemTypeFactory.create_instance(
                name=name, description=description
            )
            session.add(new_system_type)
            session.commit()
            session.refresh(new_system_type)

        return new_system_type

    def delete_one_system_type(self, system_type_id: UUID) -> SystemType:
        db_session = self.db_session_factory.create()
        system_types_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            system_type = system_types_repository.fine_one(id=system_type_id)
            if system_type is None:
                raise SystemTypeNotFoundException()

            session.delete(system_type)
            session.commit()

        return system_type

    def get_many_system_types(
        self, system_type_names: List[str]
    ) -> Sequence[SystemType]:
        db_session = self.db_session_factory.create()
        system_types_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            system_types = system_types_repository.find_many(names=system_type_names)
            if system_types is None:
                raise SystemTypeNotFoundException()

            valid_system_types = validated_sets_equal(
                system_type_names, [system_type.name for system_type in system_types]
            )
            if not valid_system_types:
                raise SystemTypeNotFoundException()

        return system_types
