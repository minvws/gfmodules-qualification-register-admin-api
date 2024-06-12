from typing import Sequence, List
from uuid import UUID

from app.db.entities.role import Role
from app.db.repository.roles_repository import RolesRepository
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.helpers.validators import validated_sets_equal


class RolesService:
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def get_one_role(self, role_id: UUID) -> Role:
        db_session = self.db_session_factory.create()
        roles_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            role = roles_repository.find_one(id=role_id)
            if role is None:
                raise RoleNotFoundException()

        return role

    def gel_all_roles(self) -> Sequence[Role]:
        db_session = self.db_session_factory.create()
        roles_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            roles = roles_repository.find_all()
            if roles is None:
                raise RoleNotFoundException()

        return roles

    def create_role(self, name: str, description: str) -> Role:
        db_session = self.db_session_factory.create()
        roles_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            role = roles_repository.find_one(name=name)
            if role is not None:
                raise RoleAlreadyExistsException()

            new_role = Role(name=name, description=description)
            roles_repository.create(new_role)

        return new_role

    def update_role_description(self, role_id: UUID, description: str) -> Role:
        db_session = self.db_session_factory.create()
        roles_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            role = roles_repository.find_one(id=role_id)
            if role is None:
                raise RoleNotFoundException()

            role.description = description
            roles_repository.update(role)

        return role

    def delete_role(self, role_id: UUID) -> Role:
        db_session = self.db_session_factory.create()
        roles_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            role = roles_repository.find_one(id=role_id)
            if role is None:
                raise RoleNotFoundException()

            roles_repository.delete(role)

        return role

    def get_many_roles(self, role_names: List[str]) -> Sequence[Role]:
        db_session = self.db_session_factory.create()
        repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session

        with session:
            roles = repository.find_many(role_names)
            if roles is None:
                raise RoleNotFoundException()

            valid_roles = validated_sets_equal(
                role_names, [role.name for role in roles]
            )
            if not valid_roles:
                raise RoleNotFoundException()

        return roles
