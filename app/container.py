import inject


from app.db.db import Database
from app.config import get_config
from app.db.repository_factory import RepositoryFactory
from app.db.services.application_type_service import ApplicationTypeService
from app.db.services.healthcare_provider_application_version_service import (
    HealthcareProviderApplicationVersionService,
)
from app.db.services.healthcare_provider_qualification_service import (
    HealthcareProviderQualificationService,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.db.session_factory import DbSessionFactory
from app.db.services.application_roles_service import ApplicationRolesService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService

from app.db.services.application_service import ApplicationService


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(dsn=config.database.dsn)
    binder.bind(Database, db)

    session_factory = DbSessionFactory(db.engine)
    binder.bind(DbSessionFactory, session_factory)

    repository_factory = RepositoryFactory()
    binder.bind(RepositoryFactory, repository_factory)

    vendors_service = VendorService()
    binder.bind(VendorService, vendors_service)

    roles_service = RolesService(
        db_session_factory=session_factory, repository_factory=repository_factory
    )
    binder.bind(RolesService, roles_service)

    system_type_service = SystemTypeService()
    binder.bind(SystemTypeService, system_type_service)

    application_service = ApplicationService()
    binder.bind(ApplicationService, application_service)

    application_version_service = ApplicationVersionService(
        db_session_factory=session_factory,
        application_service=application_service,
        repository_factory=repository_factory,
    )
    binder.bind(ApplicationVersionService, application_version_service)

    application_roles_service = ApplicationRolesService(
        roles_service,
        application_service,
        db_session_factory=session_factory,
        repository_factory=repository_factory,
    )
    binder.bind(ApplicationRolesService, application_roles_service)

    application_type_service = ApplicationTypeService()
    binder.bind(ApplicationTypeService, application_type_service)

    healthcare_provider_service = HealthcareProviderService()
    binder.bind(HealthcareProviderService, healthcare_provider_service)

    healthcare_provider_application_version_service = (
        HealthcareProviderApplicationVersionService(
            db_session_factory=session_factory,
            repository_factory=repository_factory,
            healthcare_provider_service=healthcare_provider_service,
        )
    )
    binder.bind(
        HealthcareProviderApplicationVersionService,
        healthcare_provider_application_version_service,
    )

    protocol_service = ProtocolService()
    binder.bind(ProtocolService, protocol_service)

    protocol_version_service = ProtocolVersionService(
        protocol_service=protocol_service,
    )
    binder.bind(ProtocolVersionService, protocol_version_service)

    protocol_application_qualification_service = (
        ProtocolApplicationQualificationService(
            db_session_factory=session_factory, repository_factory=repository_factory
        )
    )
    binder.bind(
        ProtocolApplicationQualificationService,
        protocol_application_qualification_service,
    )

    healthcare_provider_qualification_service = HealthcareProviderQualificationService(
        db_session_factory=session_factory, repository_factory=repository_factory
    )
    binder.bind(
        HealthcareProviderQualificationService,
        healthcare_provider_qualification_service,
    )


def get_vendors_service() -> VendorService:
    return inject.instance(VendorService)


def get_system_type_service() -> SystemTypeService:
    return inject.instance(SystemTypeService)


def get_application_service() -> ApplicationService:
    return inject.instance(ApplicationService)


def get_roles_service() -> RolesService:
    return inject.instance(RolesService)


def get_application_roles_service() -> ApplicationRolesService:
    return inject.instance(ApplicationRolesService)


def get_application_type_service() -> ApplicationTypeService:
    return inject.instance(ApplicationTypeService)


def get_application_version_service() -> ApplicationVersionService:
    return inject.instance(ApplicationVersionService)


def get_healthcare_provider_service() -> HealthcareProviderService:
    return inject.instance(HealthcareProviderService)


def get_healthcare_provider_application_version_service() -> (
    HealthcareProviderApplicationVersionService
):
    return inject.instance(HealthcareProviderApplicationVersionService)


def get_protocol_application_qualification_service() -> (
    ProtocolApplicationQualificationService
):
    return inject.instance(ProtocolApplicationQualificationService)


def get_protocol_service() -> ProtocolService:
    return inject.instance(ProtocolService)


def get_protocol_version_service() -> ProtocolVersionService:
    return inject.instance(ProtocolVersionService)


def get_healthcare_provider_qualification_service() -> (
    HealthcareProviderQualificationService
):
    return inject.instance(HealthcareProviderQualificationService)


def get_database() -> Database:
    return inject.instance(Database)


if not inject.is_configured():
    inject.configure(container_config)
