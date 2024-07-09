from datetime import date, datetime
from uuid import UUID

from app.db.entities.protocol_version import ProtocolVersion
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.repository.protocol_version_repository import ProtocolVersionRepository
from app.db.session_manager import get_repository, session_manager
from app.exceptions.app_exceptions import (
    ProtocolVersionNotFoundException,
    ApplicationVersionNotFoundException,
    AppVersionAlreadyQualifiedException,
    AppVersionAlreadyArchivedException,
    AppVersionNotQualifiedForProtocolException,
)
from app.factory.protocol_application_qualification_factory import (
    ProtocolApplicationQualificationFactory,
)


class ProtocolApplicationQualificationService:
    @session_manager
    def qualify_protocol_version_to_application_version(
        self,
        protocol_version_id: UUID,
        application_version_id: UUID,
        qualification_date: date,
        application_version_repository: ApplicationVersionRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> ProtocolVersion:
        protocol_version = protocol_version_repository.get(id=protocol_version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        application_version = application_version_repository.get(
            id=application_version_id
        )
        if application_version is None:
            raise ApplicationVersionNotFoundException()

        for qualified_apps in protocol_version.qualified_application_versions:
            if (
                qualified_apps.application_version_id == application_version.id
                and qualified_apps.protocol_version_id == protocol_version.id
            ):
                if qualified_apps.archived_date is not None:
                    raise AppVersionAlreadyArchivedException()

                raise AppVersionAlreadyQualifiedException()

        new_qualification = ProtocolApplicationQualificationFactory.create_instance(
            protocol_version=protocol_version,
            application_version=application_version,
            qualification_date=qualification_date,
        )

        protocol_version.qualified_application_versions.append(new_qualification)
        protocol_version_repository.update(protocol_version)

        return protocol_version

    @session_manager
    def archive_protocol_application_qualification(
        self,
        application_version_id: UUID,
        protocol_version_id: UUID,
        application_version_repository: ApplicationVersionRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> ProtocolVersion:
        protocol_version = protocol_version_repository.get(id=protocol_version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        application_version = application_version_repository.get(
            id=application_version_id
        )
        if application_version is None:
            raise ApplicationVersionNotFoundException()

        for qualified_app in protocol_version.qualified_application_versions:
            if (
                qualified_app.application_version_id == application_version.id
                and qualified_app.protocol_version_id == protocol_version.id
            ):
                if qualified_app.archived_date is not None:
                    raise AppVersionAlreadyArchivedException()

                qualified_app.archived_date = datetime.now()
                protocol_version_repository.update(protocol_version)
                return protocol_version

        raise AppVersionNotQualifiedForProtocolException()
