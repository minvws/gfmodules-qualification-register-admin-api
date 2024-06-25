from uuid import UUID

from app.db.entities.application import Application
from app.db.repository.application_repository import ApplicationRepository
from app.db.repository.system_type_repository import SystemTypeRepository
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    SystemTypeNotFoundException,
    SystemTypeExistInApplicationException,
    SystemTypeNotUsedByApplicationException,
)
from app.factory.application_type_factory import ApplicationTypeFactory


class ApplicationTypeService:
    @session_manager
    def assign_system_type_to_application(
        self,
        application_id: UUID,
        system_type_id: UUID,
        application_repository: ApplicationRepository = get_repository(),
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        system_type = system_type_repository.get(id=system_type_id)
        if system_type is None:
            raise SystemTypeNotFoundException()

        for app_type in application.system_types:
            if (
                app_type.application_id == application_id
                and app_type.system_type_id == system_type_id
            ):
                raise SystemTypeExistInApplicationException()

        new_application_type = ApplicationTypeFactory.create_instance(
            application=application, system_type=system_type
        )
        application.system_types.append(new_application_type)

        application_repository.update(application)

        return application

    @session_manager
    def unassign_system_type_to_application(
        self,
        application_id: UUID,
        system_type_id: UUID,
        application_repository: ApplicationRepository = get_repository(),
        system_type_repository: SystemTypeRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        system_type = system_type_repository.get(id=system_type_id)
        if system_type is None:
            raise SystemTypeNotFoundException()

        for app_type in application.system_types:
            if (
                app_type.application_id == application_id
                and app_type.system_type_id == system_type.id
            ):
                application.system_types.remove(app_type)
                application_repository.update(application)
                return application

        raise SystemTypeNotUsedByApplicationException()
