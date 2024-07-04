from typing import Sequence
from uuid import UUID

from app.db.entities.application import Application
from app.db.entities.application_type import ApplicationType
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.repository.system_types_repository import SystemTypesRepository
from app.db.repository_factory import RepositoryFactory
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
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.application_service = application_service
        self.repository_factory = repository_factory

    def get_all(self, application_id: UUID) -> Sequence[ApplicationType]:
        application = self.application_service.get_one(application_id)
        return application.system_types

    def assign_system_type_to_application(
        self, application_id: UUID, system_type_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
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

    def unassign_system_type_to_application(
        self, application_id: UUID, system_type_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        system_type_repository = self.repository_factory.create(
            SystemTypesRepository, db_session
        )
        with db_session:
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
