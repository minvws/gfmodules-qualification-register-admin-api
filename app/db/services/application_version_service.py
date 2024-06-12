from typing import Sequence
from uuid import UUID


from app.db.entities.application import Application
from app.db.entities.application_version import ApplicationVersion
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    ApplicationVersionDeleteException,
    ApplicationNotFoundException,
    ApplicationVersionNotFoundException,
)
from app.factory.application_version_factory import ApplicationVersionFactory
from app.helpers.validators import validate_list_for_removal
from app.db.services.application_service import ApplicationService


class ApplicationVersionService:
    def __init__(
        self,
        application_service: ApplicationService,
        db_session_factory: DbSessionFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.application_service = application_service

    def get_one_application_versions(
        self, application_id: UUID
    ) -> Sequence[ApplicationVersion]:
        application = self.application_service.get_one_application_by_id(application_id)
        return application.versions

    def add_application_version(
        self, application_id: UUID, version: str
    ) -> Sequence[ApplicationVersion]:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        session = db_session.session
        with session:
            application = session.merge(
                self.application_service.get_one_application_by_id(application_id)
            )
            new_version = ApplicationVersionFactory.create_instance(version=version)
            new_version.application = application
            application.versions.append(new_version)
            application_repository.update(application)

        return application.versions

    def delete_application_version(
        self, application_id: UUID, version_id: UUID
    ) -> Sequence[ApplicationVersion]:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        application_version_repository: ApplicationVersionRepository = (
            db_session.get_repository(ApplicationVersion)
        )
        session = db_session.session
        with session:
            application = application_repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

            app_has_versions = validate_list_for_removal(application.versions)
            if not app_has_versions:
                raise ApplicationVersionDeleteException()

            application_version = application_version_repository.find_one(id=version_id)
            if application_version is None:
                raise ApplicationVersionNotFoundException()

            application.versions.remove(application_version)
            application_repository.update(application)

        return application.versions
