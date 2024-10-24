from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import NoResultFound

from app.container import (
    get_application_roles_service,
    get_application_service,
    get_application_version_service,
    get_application_type_service,
)
from app.db.services.application_type_service import ApplicationTypeService
from app.exceptions.http_base_exceptions import NotFoundException
from app.schemas.application.mapper import (
    map_application_entity_to_dto,
    map_application_version_entity_to_dto,
)
from app.schemas.application.schema import (
    ApplicationDto,
    ApplicationVersionCreateDto,
    ApplicationVersionDto,
)
from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams
from app.schemas.vendor.schema import VendorApplicationCreateDto
from app.db.services.application_roles_service import ApplicationRolesService
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("")
def get_applications(
    query: Annotated[PaginationQueryParams, Depends()],
    service: ApplicationService = Depends(get_application_service),
) -> Page[ApplicationDto]:
    return service.get_paginated(limit=query.limit, offset=query.offset)


@router.get("/{application_id}")
def get_application_by_id(
    application_id: UUID, service: ApplicationService = Depends(get_application_service)
) -> ApplicationDto:
    application = service.get_one(application_id=application_id)
    return map_application_entity_to_dto(application)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application_by_id(
    application_id: UUID, service: ApplicationService = Depends(get_application_service)
) -> None:
    service.remove_one(application_id=application_id)


@router.post("/{application_id}/versions")
def add_application_version(
    application_id: UUID,
    data: ApplicationVersionCreateDto,
    service: ApplicationVersionService = Depends(get_application_version_service),
) -> List[ApplicationVersionDto]:
    versions = service.add_one(application_id=application_id, version=data.version)
    return [map_application_version_entity_to_dto(version) for version in versions]


@router.delete("/{application_id}/versions/{version_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application_version(
    application_id: UUID,
    version_id: UUID,
    service: ApplicationVersionService = Depends(get_application_version_service),
) -> None:
    service.remove_one(application_id=application_id, version_id=version_id)


@router.get("/vendors/{vendor_id}")
def get_all_vendor_applications(
    vendor_id: UUID,
    application_service: ApplicationService = Depends(get_application_service),
) -> list[ApplicationDto]:
    results = application_service.get_by_vendor_id(vendor_id)
    return [map_application_entity_to_dto(result) for result in results]


@router.post("/vendors/{vendor_id}")
def register_one_vendor_application(
    vendor_id: UUID,
    data: VendorApplicationCreateDto,
    service: ApplicationService = Depends(get_application_service),
) -> ApplicationDto:
    try:
        result = service.add_one(
            vendor_id=vendor_id,
            application_name=data.name,
            version=data.version,
            system_type_names=data.system_types,
            role_names=data.roles,
        )
        return map_application_entity_to_dto(result)
    except NoResultFound as e:
        raise NotFoundException(str(e))


@router.patch("/{application_id}/roles/{role_id}")
def assign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> ApplicationDto:
    results = service.assign_role_to_application(application_id, role_id)
    return map_application_entity_to_dto(results)


@router.delete("/{application_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> None:
    service.unassign_role_from_application(application_id, role_id)


@router.post("/{application_id}/system-types/{system_type_id}")
def assign_system_type_to_application(
    application_id: UUID,
    system_type_id: UUID,
    service: ApplicationTypeService = Depends(get_application_type_service),
) -> ApplicationDto:
    application = service.assign_system_type_to_application(
        application_id, system_type_id
    )
    return map_application_entity_to_dto(application)


@router.delete("/{application_id}/system-types/{system_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassing_system_type_from_application(
    application_id: UUID,
    system_type_id: UUID,
    service: ApplicationTypeService = Depends(get_application_type_service),
) -> None:
    service.unassign_system_type_to_application(
        application_id, system_type_id
    )
