from uuid import UUID

from app.db.entities.models import Application, Role, ApplicationRole
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    RoleNotFoundException,
    RoleExistInApplicationException,
    RoleNotInApplicationException,
)
from app.factory.application_roles_factory import ApplicationRolesFactory
from app.services.application_service import ApplicationService
from app.services.roles_service import RolesService


class ApplicationRolesService:
    def __init__(
        self, roles_service: RolesService, application_service: ApplicationService
    ) -> None:
        self.roles_service = roles_service
        self.application_service = application_service

    def assign_role_to_application(
        self, application_id: UUID, role_id: UUID
    ) -> Application:
        application_repository = self.application_service.get_applications_repository()
        role_repository = self.roles_service.get_roles_repository()

        application = application_repository.find_one(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        role = role_repository.find_one(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        role_in_application = self._validate_if_role_exists_in_application(
            application, role
        )
        if role_in_application:
            raise RoleExistInApplicationException()

        new_role = application_repository.session.merge(role)
        application_role = ApplicationRolesFactory.create_instance()
        application_role.role = new_role
        application.roles.append(application_role)
        application_repository.update(application)

        return application

    def remove_role_from_application(
        self, application_id: UUID, role_id: UUID
    ) -> Application:
        application_repository = self.application_service.get_applications_repository()
        role_repository = self.roles_service.get_roles_repository()

        application = application_repository.find_one(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        role = role_repository.find_one(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        role_exist_in_application = self._validate_if_role_exists_in_application(
            application, role
        )
        if not role_exist_in_application:
            raise RoleNotInApplicationException()

        target_role = self._get_role_from_app(application, role)
        application.roles.remove(target_role)
        application_repository.update(application)

        return application

    @staticmethod
    def _validate_if_role_exists_in_application(
        application: Application, role: Role
    ) -> bool:
        return str(role.id) in [str(role.role_id) for role in application.roles]

    @staticmethod
    def _get_role_from_app(application: Application, role: Role) -> ApplicationRole:
        for app_role in application.roles:
            print(role.id)
            if str(role.id) == str(app_role.role_id):
                return app_role

        raise RoleNotFoundException()
