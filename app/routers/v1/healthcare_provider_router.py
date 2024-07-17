from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import (
    get_healthcare_provider_service,
    get_healthcare_provider_application_version_service,
)
from app.db.services.healthcare_provider_application_version_service import (
    HealthcareProviderApplicationVersionService,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.schemas.healthcare_provider.mapper import (
    map_healthcare_provider_entity_to_dto,
)
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderCreateDto,
    HealthcareProviderDto,
)
from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams

router = APIRouter(prefix="/healthcare-provider", tags=["Healthcare  Provider"])


@router.get("")
def get_healthcare_providers(
    query: Annotated[PaginationQueryParams, Depends()],
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> Page[HealthcareProviderDto]:
    return service.get_paginated(limit=query.limit, offset=query.offset)


@router.get("/{healthcare_provider_id}")
def get_healthcare_provider_by_id(
    healthcare_provider_id: UUID,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDto:
    healthcare_provider = service.get_one(healthcare_provider_id)
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.post("")
def register_one_healthcare_provider(
    data: HealthcareProviderCreateDto,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDto:
    new_healthcare_provider = service.add_one(**data.model_dump())
    return map_healthcare_provider_entity_to_dto(new_healthcare_provider)


@router.delete("/{healthcare_provider_id}")
def deregister_one_healthcare_provider(
    healthcare_provider_id: UUID,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDto:
    healthcare_provider = service.remove_one(healthcare_provider_id)
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.post("/{healthcare_provider_id}/application-versions/{version_id}")
def register_application_version_to_healthcare_provider(
    healthcare_provider_id: UUID,
    version_id: UUID,
    service: HealthcareProviderApplicationVersionService = Depends(
        get_healthcare_provider_application_version_service
    ),
) -> HealthcareProviderDto:
    healthcare_provider = service.assign_application_version_to_healthcare_provider(
        healthcare_provider_id, version_id
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.delete("/{healthcare_provider_id}/application-versions/{version_id}")
def deregister_application_version_to_healthcare_provider(
    healthcare_provider_id: UUID,
    version_id: UUID,
    service: HealthcareProviderApplicationVersionService = Depends(
        get_healthcare_provider_application_version_service
    ),
) -> HealthcareProviderDto:
    healthcare_provider = service.unassing_application_version_to_healthcare_provider(
        healthcare_provider_id, version_id
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)
