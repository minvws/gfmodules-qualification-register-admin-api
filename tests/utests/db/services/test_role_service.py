import pytest

from app.db.entities import Role
from app.db.services import RoleService
from app.exceptions.app_exceptions import RoleNotFoundException
from app.schemas.meta.schema import Page
from app.schemas.roles.mapper import map_role_model_to_dto

from .utils import are_the_same_entity


def test_create_role(role_service: RoleService) -> None:
    expected_role = role_service.add_one(
        name="example role", description="some description"
    )
    actual_role = role_service.get_one(role_id=expected_role.id)

    assert are_the_same_entity(actual_role, expected_role)


def test_update_role_description(role: Role, role_service: RoleService) -> None:
    expected_role = role_service.update_role_description(
        role_id=role.id, description="new description"
    )
    actual_role = role_service.get_one(role_id=role.id)
    assert role.id == expected_role.id == actual_role.id
    assert role.description != actual_role.description
    assert expected_role.description == actual_role.description


def test_delete_role(role: Role, role_service: RoleService) -> None:
    actual_role = role_service.remove_one(role_id=role.id)

    assert are_the_same_entity(actual_role, role)

    with pytest.raises(RoleNotFoundException, match="404: Role not found"):
        role_service.get_one(role.id)


def test_get_many_roles(role: Role, role_service: RoleService) -> None:
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            role_service.get_many_by_names([role.name]),
            [role],
        )
    )


def test_get_paginated_roles(role: Role, role_service: RoleService) -> None:
    assert role_service.get_paginated(limit=10, offset=0) == Page(
        items=[map_role_model_to_dto(role)],
        limit=10,
        offset=0,
        total=1,
    )
