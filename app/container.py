import inject
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

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
    application_service = ApplicationService()
    healthcare_provider_service = HealthcareProviderService()
    protocol_service = ProtocolService()
    engine = create_engine(
        config.database.dsn, echo=False, pool_recycle=25, pool_size=10
    )

    (
        binder.bind(Engine, engine)
        .bind(sessionmaker[Session], sessionmaker(engine))
        .bind(VendorService, VendorService())
        .bind(RoleService, RoleService())
        .bind(SystemTypeService, SystemTypeService())
        .bind(ApplicationService, application_service)
        .bind(ApplicationTypeService, ApplicationTypeService())
        .bind(ProtocolService, protocol_service)
        .bind(HealthcareProviderService, healthcare_provider_service)
        .bind(
            ApplicationVersionService,
            ApplicationVersionService(application_service=application_service),
        )
        .bind(
            ApplicationRolesService,
            ApplicationRolesService(application_service=application_service),
        )
        .bind(
            HealthcareProviderApplicationVersionService,
            HealthcareProviderApplicationVersionService(
                healthcare_provider_service=healthcare_provider_service
            ),
        )
        .bind(
            ProtocolVersionService,
            ProtocolVersionService(protocol_service=protocol_service),
        )
        .bind(
            ProtocolApplicationQualificationService,
            ProtocolApplicationQualificationService(),
        )
        .bind(
            HealthcareProviderQualificationService,
            HealthcareProviderQualificationService(),
        )
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


def get_engine() -> Engine:
    return inject.instance(Engine)


if not inject.is_configured():
    inject.configure(container_config)