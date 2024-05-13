from typing import Sequence
from uuid import UUID

from app.db.db import Database
from app.db.db_session import DbSession
from app.db.entities.models import Role
from app.db.repository.roles_repository import RolesRepository
from app.exceptions.app_exceptions import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
    RoleDBServiceUnavailableException,
    RoleDeleteException,
)


class RolesService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_one_role(self, role_id: UUID) -> Role:
        repository = self.get_roles_repository()
        role = repository.find_one(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        return role

    def gel_all_roles(self) -> Sequence[Role]:
        repository = self.get_roles_repository()
        roles = repository.find_all()
        if roles is None:
            raise RoleDBServiceUnavailableException()

        return roles

    def create_role(self, name: str, description: str) -> Role:
        repository = self.get_roles_repository()

        role = Role(name=name, description=description)
        updated_role = repository.create(role)
        if updated_role is None:
            raise RoleAlreadyExistsException()

        return updated_role

    def update_role_description(self, role_id: UUID, description: str) -> Role:
        repository = self.get_roles_repository()
        role = repository.find_one(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        role.description = description
        repository.update(role)

        return role

    def delete_role(self, role_id: UUID) -> Role:
        repository = self.get_roles_repository()
        role = repository.find_one(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        deleted_role = repository.delete(role)
        if deleted_role is None:
            raise RoleDeleteException()

        return deleted_role

    def get_roles_repository(self) -> RolesRepository:
        repository_session = DbSession[RolesRepository](engine=self.database.engine)
        return repository_session.get_repository(Role)
