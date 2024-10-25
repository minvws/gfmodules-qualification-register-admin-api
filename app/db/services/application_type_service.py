from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities import Application
from app.db.repository import ApplicationRepository, SystemTypeRepository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    SystemTypeNotFoundException,
    SystemTypeExistInApplicationException,
    SystemTypeNotUsedByApplicationException,
)
from app.factory import ApplicationTypeFactory


class ApplicationTypeService:
    @session_manager
    def assign_system_type_to_application(
        self,
        application_id: UUID,
        system_type_id: UUID,
        *,
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

        return application

    @session_manager
    def unassign_system_type_to_application(
        self,
        application_id: UUID,
        system_type_id: UUID,
        *,
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
                return application

        raise SystemTypeNotUsedByApplicationException()
