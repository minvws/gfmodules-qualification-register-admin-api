from typing import Sequence
from uuid import UUID

from app.db.entities.application_version import ApplicationVersion
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.session_manager import get_repository, session_manager
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
    ) -> None:
        self.application_service = application_service

    def get_many(self, application_id: UUID) -> Sequence[ApplicationVersion]:
        application = self.application_service.get_one(application_id)
        return application.versions

    @session_manager
    def add_one(
        self,
        application_id: UUID,
        version: str,
        application_respository: ApplicationsRepository = get_repository(),
    ) -> Sequence[ApplicationVersion]:

        application = application_respository.get_or_fail(id=application_id)

        new_version = ApplicationVersionFactory.create_instance(version=version)
        new_version.application = application
        application.versions.append(new_version)
        application_respository.update(application)

        return application.versions

    @session_manager
    def remove_one(
        self,
        application_id: UUID,
        version_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
        application_version_repository: ApplicationVersionRepository = get_repository(),
    ) -> Sequence[ApplicationVersion]:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        app_has_versions = validate_list_for_removal(application.versions)
        if not app_has_versions:
            raise ApplicationVersionDeleteException()

        application_version = application_version_repository.get(id=version_id)
        if application_version is None:
            raise ApplicationVersionNotFoundException()

        application.versions.remove(application_version)
        application_repository.update(application)

        return application.versions
