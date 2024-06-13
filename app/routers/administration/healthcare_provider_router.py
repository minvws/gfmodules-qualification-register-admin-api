from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_healthcare_provider_service
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.schemas.healthcare_provider.mapper import map_healthcare_provider_entity_to_dto
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderCreateDTO,
    HealthcareProviderDTO,
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
