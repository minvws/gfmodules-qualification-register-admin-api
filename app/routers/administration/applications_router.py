from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import (
    get_application_roles_service,
    get_vendor_application_service,
    get_application_service,
    get_application_version_service,
    get_application_type_service,
)
from app.db.services.application_type_service import ApplicationTypeService
from app.schemas.application.mapper import (
    map_application_entity_to_dto,
    map_application_version_entity_to_dto,
    map_application_roles_entity_to_dto,
    map_application_system_type_entity_to_dto,
)
from app.schemas.application.schema import (
    ApplicationDTO,
    ApplicationVersionCreateDTO,
    ApplicationVersionDTO,
    ApplicationRoleDTO,
    ApplicationTypeDTO,
)
from app.schemas.vendor.schema import VendorApplicationCreateDTO
from app.db.services.application_roles_service import ApplicationRolesService
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.vendor_application_service import VendorApplicationService

router = APIRouter(prefix="/administration/applications", tags=["Applications"])


@router.get("", response_model=List[ApplicationDTO])
def get_all_registered_applications(
    service: ApplicationService = Depends(get_application_service),
) -> List[ApplicationDTO]:
    applications = service.get_all_applications()
    return [map_application_entity_to_dto(app) for app in applications]


@router.get("/{application_id}", response_model=ApplicationDTO)
def get_application_by_id(
    application_id: UUID, service: ApplicationService = Depends(get_application_service)
) -> ApplicationDTO:
    application = service.get_one_application_by_id(application_id=application_id)
    return map_application_entity_to_dto(application)


@router.delete("/{application_id}", response_model=ApplicationDTO)
def delete_application_by_id(
    application_id: UUID, service: ApplicationService = Depends(get_application_service)
) -> ApplicationDTO:
    deleted_application = service.delete_one_application_by_id(
        application_id=application_id
    )
    return map_application_entity_to_dto(deleted_application)


@router.get("/{application_id}/versions")
def get_applications_versions(
    application_id: UUID,
    service: ApplicationVersionService = Depends(get_application_version_service),
) -> List[ApplicationVersionDTO]:
    versions = service.get_one_application_versions(application_id=application_id)
    return [map_application_version_entity_to_dto(version) for version in versions]


@router.post("/{application_id}/version/")
def add_application_version(
    application_id: UUID,
    data: ApplicationVersionCreateDTO,
    service: ApplicationVersionService = Depends(get_application_version_service),
) -> List[ApplicationVersionDTO]:
    versions = service.add_application_version(
        application_id=application_id, version=data.version
    )
    return [map_application_version_entity_to_dto(version) for version in versions]


@router.delete("/{application_id}/version/{version_id}")
def delete_application_version(
    application_id: UUID,
    version_id: UUID,
    service: ApplicationVersionService = Depends(get_application_version_service),
) -> List[ApplicationVersionDTO]:
    versions = service.delete_application_version(
        application_id=application_id, version_id=version_id
    )
    return [map_application_version_entity_to_dto(version) for version in versions]


@router.get("/vendor/{kvk_number}")
def get_all_vendor_applications(
    kvk_number: str,
    vendor_application_service: VendorApplicationService = Depends(
        get_vendor_application_service
    ),
) -> list[ApplicationDTO]:
    results = vendor_application_service.get_all_vendor_applications(kvk_number)
    return [map_application_entity_to_dto(result) for result in results]


@router.post("/vendor/{vendor_id}")
def register_one_vendor_application(
    vendor_id: UUID,
    data: VendorApplicationCreateDTO,
    service: VendorApplicationService = Depends(get_vendor_application_service),
) -> ApplicationDTO:
    result = service.register_one_app(
        vendor_id=vendor_id,
        application_name=data.name,
        application_version=data.version,
        system_type_names=data.system_types,
        role_names=data.roles,
    )
    return map_application_entity_to_dto(result)


@router.get("/{application_id}/roles")
def get_application_roles(
    application_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> List[ApplicationRoleDTO]:
    roles = service.get_application_roles(application_id)
    return [map_application_roles_entity_to_dto(role) for role in roles]


@router.patch("/{application_id}/role/{role_id}")
def assign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> ApplicationDTO:
    results = service.assign_role_to_application(application_id, role_id)
    return map_application_entity_to_dto(results)


@router.delete("/{application_id}/role/{role_id}")
def unassign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> ApplicationDTO:
    results = service.unassign_role_from_application(application_id, role_id)
    return map_application_entity_to_dto(results)


@router.get("/{application_id}/system_types/")
def get_application_types(
    application_id: UUID,
    service: ApplicationTypeService = Depends(get_application_type_service),
) -> List[ApplicationTypeDTO]:
    application_types = service.get_all_application_types(application_id)
    return [
        map_application_system_type_entity_to_dto(app_type)
        for app_type in application_types
    ]


@router.post("/{application_id}/system_types/{system_type_id}/")
def assign_system_type_to_application(
    application_id: UUID,
    system_type_id: UUID,
    service: ApplicationTypeService = Depends(get_application_type_service),
) -> ApplicationDTO:
    application = service.assign_system_type_to_application(
        application_id, system_type_id
    )
    return map_application_entity_to_dto(application)


@router.delete("/{application_id}/system_types/{system_type_id}/")
def unassing_system_type_from_application(
    application_id: UUID,
    system_type_id: UUID,
    service: ApplicationTypeService = Depends(get_application_type_service),
) -> ApplicationDTO:
    application = service.unassign_system_type_to_application(
        application_id, system_type_id
    )
    return map_application_entity_to_dto(application)
