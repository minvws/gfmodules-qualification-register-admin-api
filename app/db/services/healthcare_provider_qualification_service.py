from uuid import UUID
from datetime import date, datetime

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities import HealthcareProvider
from app.db.repository import HealthcareProviderRepository, ProtocolVersionRepository
from app.exceptions.app_exceptions import (
    HealthcareProviderNotFoundException,
    ProtocolVersionNotFoundException,
    HealthcareProviderAlreadyQualifiedException,
    HealthcareProviderQualificationAlreadyArchivedException,
    HealthcareProviderNotQualifiedForProtocolException,
)
from app.factory import HealthcareProviderQualificationFactory


class HealthcareProviderQualificationService:
    @session_manager
    def qualify_healthcare_provider(
        self,
        healthcare_provider_id: UUID,
        protocol_version_id: UUID,
        qualification_date: date,
        *,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(
            id=healthcare_provider_id
        )
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        protocol_version = protocol_version_repository.get(id=protocol_version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        for qualified_protocols in healthcare_provider.qualified_protocols:
            if (
                qualified_protocols.protocol_version_id == protocol_version_id
                and qualified_protocols.healthcare_provider_id == healthcare_provider.id
            ):
                if qualified_protocols.archived_date is not None:
                    raise HealthcareProviderQualificationAlreadyArchivedException()

                raise HealthcareProviderAlreadyQualifiedException()

        new_healthcare_provider_qualification = (
            HealthcareProviderQualificationFactory.create_instance(
                healthcare_provider=healthcare_provider,
                protocol_version=protocol_version,
                qualification_date=qualification_date,
            )
        )
        healthcare_provider.qualified_protocols.append(
            new_healthcare_provider_qualification
        )

        healthcare_provider_repository.update(healthcare_provider)

        return healthcare_provider

    @session_manager
    def archive_healthcare_provider_qualification(
        self,
        healthcare_provider_id: UUID,
        protocol_version_id: UUID,
        *,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(
            id=healthcare_provider_id
        )
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        protocol_version = protocol_version_repository.get(id=protocol_version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        for qualified_protocols in healthcare_provider.qualified_protocols:
            if (
                qualified_protocols.protocol_version_id == protocol_version_id
                and qualified_protocols.healthcare_provider_id == healthcare_provider_id
            ):
                if qualified_protocols.archived_date is not None:
                    raise HealthcareProviderQualificationAlreadyArchivedException()

                qualified_protocols.archived_date = datetime.now()
                healthcare_provider_repository.update(healthcare_provider)
                return healthcare_provider

        raise HealthcareProviderNotQualifiedForProtocolException()
