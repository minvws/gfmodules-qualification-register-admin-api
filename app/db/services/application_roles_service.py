from uuid import UUID

from app.db.entities.application import Application
from app.db.repository.application_repository import ApplicationRepository
from app.db.repository.role_repository import RoleRepository
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    RoleNotFoundException,
    RoleExistInApplicationException,
    ApplicationRoleDeleteException,
)
from app.factory.application_roles_factory import ApplicationRolesFactory
from app.helpers.validators import validate_list_for_removal
from app.db.services.application_service import ApplicationService


class ApplicationRolesService:
    def __init__(
        self,
        application_service: ApplicationService,
    ) -> None:
        self.application_service = application_service

    @session_manager
    def assign_role_to_application(
        self,
        application_id: UUID,
        role_id: UUID,
        application_repository: ApplicationRepository = get_repository(),
        role_repository: RoleRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        for app_role in application.roles:
            if app_role.role_id == role_id:
                raise RoleExistInApplicationException()

        new_application_role = ApplicationRolesFactory.create_instance(
            application=application, role=role
        )
        application.roles.append(new_application_role)

        application_repository.update(application)

        return application

    @session_manager
    def unassign_role_from_application(
        self,
        application_id: UUID,
        role_id: UUID,
        application_repository: ApplicationRepository = get_repository(),
        role_repository: RoleRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        app_has_roles = validate_list_for_removal(application.roles)
        if not app_has_roles:
            raise ApplicationRoleDeleteException()

        role = role_repository.get(id=role_id)
        if role is None:
            raise RoleNotFoundException()

        for app_role in application.roles:
            if (
                app_role.role_id == role.id
                and app_role.application_id == application_id
            ):
                application.roles.remove(app_role)
                application_repository.update(application)
                break

        return application
