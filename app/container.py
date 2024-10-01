import inject
from sqlalchemy.orm import Session, sessionmaker

from app.db.db import Database
from app.config import get_config
from app.db.services import (
    ApplicationService,
    ApplicationTypeService,
    HealthcareProviderApplicationVersionService,
    HealthcareProviderQualificationService,
    HealthcareProviderService,
    ProtocolApplicationQualificationService,
    ProtocolService,
    ProtocolVersionService,
    ApplicationRolesService,
    ApplicationVersionService,
    RoleService,
    SystemTypeService,
    VendorService,
)


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(dsn=config.database.dsn)
    binder.bind(Database, db)
    binder.bind(sessionmaker[Session], sessionmaker(db.engine))

    vendors_service = VendorService()
    binder.bind(VendorService, vendors_service)

    roles_service = RoleService()
    binder.bind(RoleService, roles_service)

    system_type_service = SystemTypeService()
    binder.bind(SystemTypeService, system_type_service)

    application_service = ApplicationService()
    binder.bind(ApplicationService, application_service)

    application_version_service = ApplicationVersionService(
        application_service=application_service,
    )
    binder.bind(ApplicationVersionService, application_version_service)

    application_roles_service = ApplicationRolesService(
        application_service=application_service
    )
    binder.bind(ApplicationRolesService, application_roles_service)

    application_type_service = ApplicationTypeService()
    binder.bind(ApplicationTypeService, application_type_service)

    healthcare_provider_service = HealthcareProviderService()
    binder.bind(HealthcareProviderService, healthcare_provider_service)

    healthcare_provider_application_version_service = (
        HealthcareProviderApplicationVersionService(
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
        ProtocolApplicationQualificationService()
    )
    binder.bind(
        ProtocolApplicationQualificationService,
        protocol_application_qualification_service,
    )

    healthcare_provider_qualification_service = HealthcareProviderQualificationService()
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


def get_roles_service() -> RoleService:
    return inject.instance(RoleService)


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
