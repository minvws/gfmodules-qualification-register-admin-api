from uuid import UUID
from datetime import date, datetime

from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.protocol_version import ProtocolVersion
from app.db.repository.healthcare_provider_repository import (
    HealthcareProviderRepository,
)
from app.db.repository.protocol_version_repository import ProtocolVersionRepository
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    HealthcareProviderNotFoundException,
    ProtocolVersionNotFoundException,
    HealthcareProviderAlreadyQualifiedException,
    HealthcareProviderQualificationAlreadyArchivedException,
    HealthcareProviderNotQualifiedForProtocolException,
)
from app.factory.healthcare_provider_qualification_factory import (
    HealthcareProviderQualificationFactory,
)


class HealthcareProviderQualificationService:
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def qualify_healthcare_provider(
        self,
        healthcare_provider_id: UUID,
        protocol_version_id: UUID,
        qualification_date: date,
    ) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        protocol_version_repository: ProtocolVersionRepository = (
            db_session.get_repository(ProtocolVersion)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=healthcare_provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

            protocol_version = protocol_version_repository.find_one(
                id=protocol_version_id
            )
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

            for qualified_protocols in healthcare_provider.qualified_protocols:
                if (
                    qualified_protocols.protocol_version_id == protocol_version_id
                    and qualified_protocols.healthcare_provider_id
                    == healthcare_provider.id
                ):
                    print(qualified_protocols.archived_date)
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

    def archive_healthcare_provider_qualification(
        self, healthcare_provider_id: UUID, protocol_version_id: UUID
    ) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        protocol_version_repository: ProtocolVersionRepository = (
            db_session.get_repository(ProtocolVersion)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=healthcare_provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

            protocol_version = protocol_version_repository.find_one(
                id=protocol_version_id
            )
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

            for qualified_protocols in healthcare_provider.qualified_protocols:
                if (
                    qualified_protocols.protocol_version_id == protocol_version_id
                    and qualified_protocols.healthcare_provider_id
                    == healthcare_provider_id
                ):
                    if qualified_protocols.archived_date is not None:
                        raise HealthcareProviderQualificationAlreadyArchivedException()

                    qualified_protocols.archived_date = datetime.now()
                    healthcare_provider_repository.update(healthcare_provider)
                    return healthcare_provider

        raise HealthcareProviderNotQualifiedForProtocolException()