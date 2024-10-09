from typing import cast

import pytest
from inject import configure

from app.db.entities import Application, Role, SystemType, Vendor
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.protocol import Protocol
from app.db.entities.protocol_version import ProtocolVersion
from app.db.services import (
    ApplicationRolesService,
    ApplicationService,
    ApplicationTypeService,
    ApplicationVersionService,
    HealthcareProviderApplicationVersionService,
    HealthcareProviderQualificationService,
    HealthcareProviderService,
    RoleService,
    SystemTypeService,
    VendorService,
)
from app.db.services.protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from tests.utests.db.services.utils import Services, container_config


@pytest.fixture(autouse=True)
def container() -> None:
    configure(container_config, clear=True)


@pytest.fixture
def vendor_service() -> VendorService:
    return cast(VendorService, Services.VENDOR.get_instance())


@pytest.fixture
def role_service() -> RoleService:
    return cast(RoleService, Services.ROLE.get_instance())


@pytest.fixture
def system_type_service() -> SystemTypeService:
    return cast(SystemTypeService, Services.SYSTEM_TYPE.get_instance())


@pytest.fixture
def application_service() -> ApplicationService:
    return cast(ApplicationService, Services.APPLICATION.get_instance())


@pytest.fixture
def application_type_service() -> ApplicationTypeService:
    return cast(ApplicationTypeService, Services.APPLICATION_TYPE.get_instance())


@pytest.fixture
def application_version_service() -> ApplicationVersionService:
    return cast(ApplicationVersionService, Services.APPLICATION_VERSION.get_instance())


@pytest.fixture
def application_role_service() -> ApplicationRolesService:
    return cast(ApplicationRolesService, Services.APPLICATION_ROLES.get_instance())


@pytest.fixture
def healthcare_provider_service() -> HealthcareProviderService:
    return cast(HealthcareProviderService, Services.HEALTHCARE_PROVIDER.get_instance())


@pytest.fixture
def healthcare_provider_qualification_service() -> (
    HealthcareProviderQualificationService
):
    return cast(
        HealthcareProviderQualificationService,
        Services.HEALTHCARE_PROVIDER_QUALIFICATION.get_instance(),
    )


@pytest.fixture
def healthcare_provider_application_version_service() -> (
    HealthcareProviderApplicationVersionService
):
    return cast(
        HealthcareProviderApplicationVersionService,
        Services.HEALTHCARE_PROVIDER_APPLICATION_VERSION.get_instance(),
    )


@pytest.fixture
def protocol_service() -> ProtocolService:
    return cast(ProtocolService, Services.PROTOCOL.get_instance())


@pytest.fixture
def protocol_version_service() -> ProtocolVersionService:
    return cast(ProtocolVersionService, Services.PROTOCOL_VERSION.get_instance())


@pytest.fixture
def protocol_application_qualification_service() -> (
    ProtocolApplicationQualificationService
):
    return cast(
        ProtocolApplicationQualificationService,
        Services.PROTOCOL_APPLICATION_QUALIFICATION.get_instance(),
    )


@pytest.fixture
def role(role_service: RoleService) -> Role:
    return role_service.add_one(name="example role", description="some description")


@pytest.fixture
def vendor(vendor_service: VendorService) -> Vendor:
    return vendor_service.add_one(
        kvk_number="12456",
        trade_name="example vendor",
        statutory_name="example vendor bv",
    )


@pytest.fixture
def system_type(system_type_service: SystemTypeService) -> SystemType:
    return system_type_service.add_one(
        name="example system type", description="some description"
    )


@pytest.fixture
def application(
    vendor: Vendor,
    role: Role,
    system_type: SystemType,
    application_service: ApplicationService,
) -> Application:
    return application_service.add_one(
        vendor_id=vendor.id,
        application_name="example application",
        version="v1.0.0",
        system_type_names=[system_type.name],
        role_names=[role.name],
    )


@pytest.fixture
def protocol(protocol_service: ProtocolService) -> Protocol:
    return protocol_service.add_one(
        protocol_type="Directive", name="example", description="example"
    )


@pytest.fixture
def protocol_version(
    protocol: Protocol, protocol_version_service: ProtocolVersionService
) -> ProtocolVersion:
    return protocol_version_service.add_one(
        protocol_id=protocol.id, version="example", description="example"
    )


@pytest.fixture
def healthcare_provider(
    protocol_version: ProtocolVersion,
    healthcare_provider_service: HealthcareProviderService,
) -> HealthcareProvider:
    return healthcare_provider_service.add_one(
        ura_code="example",
        agb_code="example",
        trade_name="example",
        statutory_name="example",
        protocol_version_id=protocol_version.id,
    )
