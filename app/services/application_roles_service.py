from typing import List
from uuid import UUID

from app.db.entities.application import Application
from app.db.entities.application_role import ApplicationRole
from app.db.entities.role import Role
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.repository.roles_repository import RolesRepository
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    RoleNotFoundException,
    RoleExistInApplicationException,
    ApplicationRoleDeleteException,
)
from app.factory.application_roles_factory import ApplicationRolesFactory
from app.helpers.validators import validate_list_for_removal
from app.services.application_service import ApplicationService
from app.services.roles_service import RolesService


class ApplicationRolesService:
    def __init__(
        self,
        roles_service: RolesService,
        application_service: ApplicationService,
        db_session_factory: DbSessionFactory,
    ) -> None:
        self.roles_service = roles_service
        self.application_service = application_service
        self.db_session_factory = db_session_factory

    def assign_role_to_application(
        self, application_id: UUID, role_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        role_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            application = application_repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

            role = role_repository.find_one(id=role_id)
            if role is None:
                raise RoleNotFoundException()

            for app_role in application.roles:
                if app_role.role_id == role_id:
                    raise RoleExistInApplicationException()

            new_application_role = ApplicationRolesFactory.create_instance()
            new_application_role.role = role
            new_application_role.application = application

            application.roles.append(new_application_role)
            role.applications.append(new_application_role)

            session.add(application)
            session.commit()
            session.refresh(application)

            return application

    def unassign_role_from_application(
        self, application_id: UUID, role_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        role_repository: RolesRepository = db_session.get_repository(Role)
        session = db_session.session
        with session:
            application = application_repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

            app_role_valid_for_delete = validate_list_for_removal(application.roles)
            if not app_role_valid_for_delete:
                raise ApplicationRoleDeleteException()

            role = role_repository.find_one(id=role_id)
            if role is None:
                raise RoleNotFoundException()

            for app_role in application.roles:
                if (
                    app_role.role_id == role.id
                    and app_role.application_id == application_id
                ):
                    application.roles.remove(app_role)
                    role.applications.remove(app_role)
                    session.commit()
                    session.refresh(application)
                    break

            return application

    def get_application_roles(self, application_id: UUID) -> List[ApplicationRole]:
        application = self.application_service.get_one_application_by_id(application_id)
        return application.roles
