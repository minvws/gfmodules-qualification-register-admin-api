from typing import Sequence, List
from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities.system_type import SystemType
from app.db.repository.system_type_repository import SystemTypeRepository
from app.exceptions.app_exceptions import (
    SystemTypeNotFoundException,
    SystemTypeAlreadyExistsException,
)
from app.factory.system_type_factory import SystemTypeFactory
from app.helpers.validators import validate_sets_equal
from app.schemas.meta.schema import Page
from app.schemas.system_type.mapper import map_system_type_entity_to_dto
from app.schemas.system_type.schema import SystemTypeDto


class SystemTypeService:
    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> Page[SystemTypeDto]:
        system_types = system_type_repository.get_many(limit=limit, offset=offset)
        dto = [map_system_type_entity_to_dto(system_type) for system_type in system_types]
        total = system_type_repository.count()

        return Page(items=dto, limit=limit, offset=offset, total=total)

    @session_manager
    def get_one(
        self,
        system_type_id: UUID,
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> SystemType:
        system_type = system_type_repository.get(id=system_type_id)
        if system_type is None:
            raise SystemTypeNotFoundException()

        return system_type

    @session_manager
    def add_one(
        self,
        name: str,
        description: str | None,
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> SystemType:
        system_type = system_type_repository.get(name=name)
        if system_type is not None:
            raise SystemTypeAlreadyExistsException()

        new_system_type = SystemTypeFactory.create_instance(
            name=name, description=description
        )
        system_type_repository.create(new_system_type)

        return new_system_type

    @session_manager
    def delete_one(
        self,
        system_type_id: UUID,
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> SystemType:
        system_type = system_type_repository.get(id=system_type_id)
        if system_type is None:
            raise SystemTypeNotFoundException()

        system_type_repository.delete(system_type)

        return system_type

    @session_manager
    def get_many_by_names(
        self,
        system_type_names: List[str],
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> Sequence[SystemType]:
        system_types = system_type_repository.get_by_property(
            attribute="name", values=system_type_names
        )
        if system_types is None:
            raise SystemTypeNotFoundException()

        valid_system_types = validate_sets_equal(
            system_type_names, [system_type.name for system_type in system_types]
        )
        if not valid_system_types:
            raise SystemTypeNotFoundException()

        return system_types
