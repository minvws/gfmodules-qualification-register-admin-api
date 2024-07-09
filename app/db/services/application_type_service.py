from typing import Sequence
from uuid import UUID

from app.db.entities.application import Application
from app.db.entities.application_type import ApplicationType
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.repository.system_types_repository import SystemTypesRepository
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
    def get_all(
        self,
        application_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
    ) -> Sequence[ApplicationType]:
        application = application_repository.get_or_fail(id=application_id)
        return application.system_types

    @session_manager
    def assign_system_type_to_application(
        self,
        application_id: UUID,
        system_type_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
        system_type_repository: SystemTypesRepository = get_repository(),
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
        application_repository: ApplicationsRepository = get_repository(),
        system_type_repository: SystemTypesRepository = get_repository(),
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
