from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import (
    get_protocol_application_qualification_service,
    get_healthcare_provider_qualification_service,
)
from app.db.services.healthcare_provider_qualification_service import (
    HealthcareProviderQualificationService,
)
from app.db.services.protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from app.openapi.responses import api_version_header_responses
from app.schemas.healthcare_provider.mapper import map_healthcare_provider_entity_to_dto
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderDto,
    HealthcareProviderQualificationCreateDto,
)
from app.schemas.protocol_application_qualification.mapper import (
    map_protocol_qualification_entity_to_dto,
)
from app.schemas.protocol_application_qualification.schema import (
    ApplicationQualificationCreateDto,
    ProtocolApplicationQualificationDto,
)

router = APIRouter(prefix="/qualifications", tags=["Qualification"])


@router.post("/{protocol_version_id}/application-versions/{version_id}", responses={**api_version_header_responses([200])})
def qualify_application_version_for_a_protocol(
    protocol_version_id: UUID,
    application_version_id: UUID,
    data: ApplicationQualificationCreateDto,
    service: ProtocolApplicationQualificationService = Depends(
        get_protocol_application_qualification_service
    ),
) -> ProtocolApplicationQualificationDto:
    protocol_version = service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version_id,
        application_version_id=application_version_id,
        qualification_date=data.qualification_date,
    )

    return map_protocol_qualification_entity_to_dto(protocol_version)


@router.delete("/{protocol_version_id}/application-versions/{application_version_id}")
def archive_application_version_qualification(
    protocol_version_id: UUID,
    application_version_id: UUID,
    service: ProtocolApplicationQualificationService = Depends(
        get_protocol_application_qualification_service
    ),
) -> ProtocolApplicationQualificationDto:
    protocol_version = service.archive_protocol_application_qualification(
        protocol_version_id=protocol_version_id,
        application_version_id=application_version_id,
    )
    return map_protocol_qualification_entity_to_dto(protocol_version)


@router.post("/{healthcare_provider_id}/protocol-versions/{protocol_version_id}")
def qualify_healthcare_provider(
    healthcare_provider_id: UUID,
    protocol_version_id: UUID,
    data: HealthcareProviderQualificationCreateDto,
    service: HealthcareProviderQualificationService = Depends(
        get_healthcare_provider_qualification_service
    ),
) -> HealthcareProviderDto:
    healthcare_provider = service.qualify_healthcare_provider(
        healthcare_provider_id=healthcare_provider_id,
        protocol_version_id=protocol_version_id,
        qualification_date=data.qualification_date,
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)


@router.delete("/{healthcare_provider_id}/protocol-versions/{protocol_version_id}")
def archive_healthcare_provider_qualification(
    healthcare_provider_id: UUID,
    protocol_version_id: UUID,
    service: HealthcareProviderQualificationService = Depends(
        get_healthcare_provider_qualification_service
    ),
) -> HealthcareProviderDto:
    healthcare_provider = service.archive_healthcare_provider_qualification(
        healthcare_provider_id=healthcare_provider_id,
        protocol_version_id=protocol_version_id,
    )
    return map_healthcare_provider_entity_to_dto(healthcare_provider)
