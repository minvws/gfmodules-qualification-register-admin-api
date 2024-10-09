from uuid import UUID

import pytest

from app.db.entities import SystemType
from app.db.services import SystemTypeService
from app.exceptions.app_exceptions import SystemTypeNotFoundException
from app.schemas.meta.schema import Page
from app.schemas.system_type.mapper import map_system_type_entity_to_dto

from .utils import are_the_same_entity


def test_add_one_single_type(system_type_service: SystemTypeService) -> None:
    expected_system_type = system_type_service.add_one(
        name="example", description="some description"
    )
    actual_system_type = system_type_service.get_one(expected_system_type.id)

    assert are_the_same_entity(actual_system_type, expected_system_type)


def test_delete_one_system_type(
    system_type: SystemType, system_type_service: SystemTypeService
) -> None:
    assert are_the_same_entity(
        system_type_service.delete_one(system_type.id), system_type
    )
    with pytest.raises(SystemTypeNotFoundException, match="404: System type not found"):
        system_type_service.get_one(system_type.id)


def test_delete_non_existing_protocol(system_type_service: SystemTypeService) -> None:
    with pytest.raises(SystemTypeNotFoundException, match="404: System type not found"):
        system_type_service.get_one(UUID("9b4014dc-71aa-4075-bdc4-6634691d31fc"))


def test_get_many_system_types(
    system_type: SystemType, system_type_service: SystemTypeService
) -> None:
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            system_type_service.get_many_by_names([system_type.name]),
            [system_type],
        )
    )


def test_get_paginated_system_types(
    system_type: SystemType, system_type_service: SystemTypeService
) -> None:
    assert system_type_service.get_paginated(limit=10, offset=0) == Page(
        items=[map_system_type_entity_to_dto(system_type)],
        limit=10,
        offset=0,
        total=1,
    )
