from datetime import date, datetime
from uuid import UUID

from app.db.entities.application_version import ApplicationVersion
from app.db.entities.protocol_version import ProtocolVersion
from app.db.repository.application_version_repository import (
    ApplicationVersionRepository,
)
from app.db.repository.protocol_version_repository import ProtocolVersionRepository
from app.db.session_factory import DbSessionFactory
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
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def qualify_protocol_version_to_application_version(
        self,
        protocol_version_id: UUID,
        application_version_id: UUID,
        qualification_date: date,
    ) -> ProtocolVersion:
        db_session = self.db_session_factory.create()
        application_version_repository: ApplicationVersionRepository = (
            db_session.get_repository(ApplicationVersion)
        )
        protocol_version_repository: ProtocolVersionRepository = (
            db_session.get_repository(ProtocolVersion)
        )
        session = db_session.session
        with session:
            protocol_version = protocol_version_repository.find_one(
                id=protocol_version_id
            )
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

            application_version = application_version_repository.find_one(
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

    def archive_protocol_application_qualification(
        self, application_version_id: UUID, protocol_version_id: UUID
    ) -> ProtocolVersion:
        db_session = self.db_session_factory.create()
        protocol_version_repository: ProtocolVersionRepository = (
            db_session.get_repository(ProtocolVersion)
        )
        application_version_repository: ApplicationVersionRepository = (
            db_session.get_repository(ApplicationVersion)
        )
        session = db_session.session
        with session:
            protocol_version = protocol_version_repository.find_one(
                id=protocol_version_id
            )
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

            application_version = application_version_repository.find_one(
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
