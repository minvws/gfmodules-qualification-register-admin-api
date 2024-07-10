from typing import Sequence, List
from uuid import UUID

from app.db.entities.role import Role
from app.db.repository.role_repository import RoleRepository
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.helpers.validators import validate_sets_equal


class RolesService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.repository_factory = repository_factory

    @session_manager
    def get_one(
        self, role_id: UUID, role_repository: RoleRepository = get_repository()
    ) -> Role:
        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        return role

    @session_manager
    def get_many(
        self,
        role_repository: RoleRepository = get_repository(),
    ) -> Sequence[Role]:
        roles = role_repository.get_many()
        return roles

    @session_manager
    def add_one(
        self,
        name: str,
        description: str,
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
        description: str,
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
