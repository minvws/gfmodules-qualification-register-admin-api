from typing import Sequence
from uuid import UUID

from app.db.entities.application_version import ApplicationVersion
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_application_version import (
    HealthcareProviderApplicationVersion,
)
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.repository.healthcare_provider_repository import (
    HealthcareProviderRepository,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    HealthcareProviderNotFoundException,
    ApplicationVersionNotFoundException,
    AppVersionExistsInHealthcareProviderException,
    AppVersionNotUsedByHealthcareProviderException,
)
from app.factory.healthcare_provider_application_version_factory import (
    HealthcareProviderApplicationVersionFactory,
)


class HealthcareProviderApplicationVersionService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        healthcare_provider_service: HealthcareProviderService,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.healthcare_provider_service = healthcare_provider_service

    def get_healthcare_provider_application_versions(
        self, provider_id: UUID
    ) -> Sequence[HealthcareProviderApplicationVersion]:
        healthcare_provider = self.healthcare_provider_service.get_one_by_id(
            provider_id
        )
        return healthcare_provider.application_versions

    def assign_application_version_to_healthcare_provider(
        self, provider_id: UUID, application_version_id: UUID
    ) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        application_version_repository: ApplicationVersionRepository = (
            db_session.get_repository(ApplicationVersion)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

            application_version = application_version_repository.find_one(
                id=application_version_id
            )
            if application_version is None:
                raise ApplicationVersionNotFoundException()

            for app_version in healthcare_provider.application_versions:
                if app_version.application_version_id == application_version.id:
                    raise AppVersionExistsInHealthcareProviderException()

            new_healthcare_provider_app_version = (
                HealthcareProviderApplicationVersionFactory.create_instance(
                    healthcare_provider=healthcare_provider,
                    application_version=application_version,
                )
            )

            healthcare_provider.application_versions.append(
                new_healthcare_provider_app_version
            )

            healthcare_provider_repository.update(healthcare_provider)

        return healthcare_provider

    def unassing_application_version_to_healthcare_provider(
        self, healthcare_provider_id: UUID, application_version_id: UUID
    ) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        application_version_repository: ApplicationVersionRepository = (
            db_session.get_repository(ApplicationVersion)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=healthcare_provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

            application_version = application_version_repository.find_one(
                id=application_version_id
            )
            if application_version is None:
                raise ApplicationVersionNotFoundException()

            for app_version in healthcare_provider.application_versions:
                if (
                    app_version.healthcare_provider_id == healthcare_provider.id
                    and app_version.application_version_id == application_version.id
                ):
                    healthcare_provider.application_versions.remove(app_version)
                    healthcare_provider_repository.update(healthcare_provider)
                    return healthcare_provider

            raise AppVersionNotUsedByHealthcareProviderException()
