from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.repository.healthcare_provider_repository import (
    HealthcareProviderRepository,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
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
        healthcare_provider_service: HealthcareProviderService,
    ) -> None:
        self.healthcare_provider_service = healthcare_provider_service

    @session_manager
    def assign_application_version_to_healthcare_provider(
        self,
        provider_id: UUID,
        application_version_id: UUID,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
        application_version_repository: ApplicationVersionRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(id=provider_id)
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        application_version = application_version_repository.get(
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

    @session_manager
    def unassing_application_version_to_healthcare_provider(
        self,
        healthcare_provider_id: UUID,
        application_version_id: UUID,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
        application_version_repository: ApplicationVersionRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(
            id=healthcare_provider_id
        )
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        application_version = application_version_repository.get(
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
