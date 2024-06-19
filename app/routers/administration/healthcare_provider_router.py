from typing import List
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
    map_healthcare_provider_app_version_entity_to_dto,
)
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderCreateDTO,
    HealthcareProviderDTO,
    HealthcareProviderApplicationVersionDTO,
)

router = APIRouter(
    prefix="/administration/healthcare-provider", tags=["Healthcare  Provider"]
)


@router.get("/")
def get_all_healthcare_providers(
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> List[HealthcareProviderDTO]:
    healthcare_providers = service.get_all_healthcare_providers()
    return [
        map_healthcare_provider_entity_to_dto(provider)
        for provider in healthcare_providers
    ]


@router.get("/{healthcare_provider_id}")
def get_healthcare_provider_by_id(
    healthcare_provider_id: UUID,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDTO:
    healthcare_provider = service.get_one_by_id(healthcare_provider_id)
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.post("/")
def register_one_healthcare_provider(
    data: HealthcareProviderCreateDTO,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDTO:
    new_healthcare_provider = service.add_one_provider(**data.model_dump())
    return map_healthcare_provider_entity_to_dto(new_healthcare_provider)


@router.delete("/{healthcare_provider_id}")
def deregister_one_healthcare_provider(
    healthcare_provider_id: UUID,
    service: HealthcareProviderService = Depends(get_healthcare_provider_service),
) -> HealthcareProviderDTO:
    healthcare_provider = service.delete_one_healthcare_provider(healthcare_provider_id)
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.get("/{healthcare_provider_id}/application_versions/")
def get_healthcare_provider_application_versions(
    healthcare_provider_id: UUID,
    service: HealthcareProviderApplicationVersionService = Depends(
        get_healthcare_provider_application_version_service
    ),
) -> List[HealthcareProviderApplicationVersionDTO]:
    application_versions = service.get_healthcare_provider_application_versions(
        healthcare_provider_id
    )
    return [
        map_healthcare_provider_app_version_entity_to_dto(version)
        for version in application_versions
    ]


@router.post("/{healthcare_provider_id}/application_versions/{version_id}")
def register_application_version_to_healthcare_provider(
    healthcare_provider_id: UUID,
    version_id: UUID,
    service: HealthcareProviderApplicationVersionService = Depends(
        get_healthcare_provider_application_version_service
    ),
) -> HealthcareProviderDTO:
    healthcare_provider = service.assign_application_version_to_healthcare_provider(
        healthcare_provider_id, version_id
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.delete("/{healthcare_provider_id}/application_versions/{version_id}")
def deregister_application_version_to_healthcare_provider(
    healthcare_provider_id: UUID,
    version_id: UUID,
    service: HealthcareProviderApplicationVersionService = Depends(
        get_healthcare_provider_application_version_service
    ),
) -> HealthcareProviderDTO:
    healthcare_provider = service.unassing_application_version_to_healthcare_provider(
        healthcare_provider_id, version_id
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)
