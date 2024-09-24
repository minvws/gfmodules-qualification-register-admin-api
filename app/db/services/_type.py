from typing import TypeAlias, Union
from .application_roles_service import ApplicationRolesService
from .application_service import ApplicationService
from .application_type_service import ApplicationTypeService
from .application_version_service import ApplicationVersionService
from .healthcare_provider_application_version_service import (
    HealthcareProviderApplicationVersionService,
)
from .healthcare_provider_qualification_service import (
    HealthcareProviderQualificationService,
)
from .healthcare_provider_service import HealthcareProviderService
from .protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from .protocol_service import ProtocolService
from .protocol_version_service import ProtocolVersionService
from .roles_service import RoleService
from .system_type_service import SystemTypeService
from .vendors_service import VendorService


Service: TypeAlias = Union[
    ApplicationService,
    ApplicationTypeService,
    ApplicationRolesService,
    ApplicationVersionService,
    HealthcareProviderService,
    HealthcareProviderQualificationService,
    HealthcareProviderApplicationVersionService,
    ProtocolService,
    ProtocolVersionService,
    ProtocolApplicationQualificationService,
    RoleService,
    SystemTypeService,
    VendorService,
]
