from typing import Sequence
from uuid import UUID

from app.db.entities.application import Application
from app.db.entities.application_type import ApplicationType
from app.db.entities.system_type import SystemType
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.repository.system_types_repository import SystemTypesRepository
from app.db.services.application_service import ApplicationService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    SystemTypeNotFoundException,
    SystemTypeExistInApplicationException,
    SystemTypeNotUsedByApplicationException,
)
from app.factory.application_type_factory import ApplicationTypeFactory


class ApplicationTypeService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        application_service: ApplicationService,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.application_service = application_service

    def get_all_application_types(
        self, application_id: UUID
    ) -> Sequence[ApplicationType]:
        application = self.application_service.get_one_application_by_id(application_id)
        return application.system_types

    def assign_system_type_to_application(
        self, application_id: UUID, system_type_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        system_type_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            application = application_repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

            system_type = system_type_repository.find_one(id=system_type_id)
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

    def unassign_system_type_to_application(
        self, application_id: UUID, system_type_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        system_type_repository: SystemTypesRepository = db_session.get_repository(
            SystemType
        )
        session = db_session.session
        with session:
            application = application_repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

            system_type = system_type_repository.find_one(id=system_type_id)
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
