from typing import Sequence, List
from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities.role import Role
from app.db.repository.role_repository import RoleRepository
from app.exceptions.app_exceptions import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.helpers.validators import validate_sets_equal
from app.schemas.meta.schema import Page
from app.schemas.roles.mapper import map_role_model_to_dto
from app.schemas.roles.schema import RoleDto


class RoleService:

    @session_manager
    def get_one(
        self, role_id: UUID, role_repository: RoleRepository = get_repository()
    ) -> Role:
        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        return role

    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        role_repository: RoleRepository = get_repository(),
    ) -> Page[RoleDto]:
        roles = role_repository.get_many(limit=limit, offset=offset)
        dto = [map_role_model_to_dto(role) for role in roles]
        total = role_repository.count()

        return Page(items=dto, limit=limit, offset=offset, total=total)

    @session_manager
    def add_one(
        self,
        name: str,
        description: str | None,
        role_repository: RoleRepository = get_repository(),
    ) -> Role:
        role = role_repository.get(name=name)
        if role is not None:
            raise RoleAlreadyExistsException()

        new_role = Role(name=name, description=description)
        role_repository.create(new_role)

        return new_role

    @session_manager
    def update_role_description(
        self,
        role_id: UUID,
        description: str | None,
        role_repository: RoleRepository = get_repository(),
    ) -> Role:
        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        role.description = description
        role_repository.update(role)

        return role

    @session_manager
    def remove_one(
        self, role_id: UUID, role_repository: RoleRepository = get_repository()
    ) -> Role:
        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        role_repository.delete(role)

        return role

    @session_manager
    def get_many_by_names(
        self, role_names: List[str], role_repository: RoleRepository = get_repository()
    ) -> Sequence[Role]:
        roles = role_repository.get_by_property("name", role_names)
        if roles is None:
            raise RoleNotFoundException()

        valid_roles = validate_sets_equal(role_names, [role.name for role in roles])
        if not valid_roles:
            raise RoleNotFoundException()

        return roles
