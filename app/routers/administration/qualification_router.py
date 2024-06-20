from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_protocol_application_qualification_service
from app.db.services.protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from app.schemas.protocol_application_qualification.mapper import (
    map_protocol_qualification_entity_to_dto,
)
from app.schemas.protocol_application_qualification.schema import (
    ApplicationQualificationCreateDTO,
    ProtocolApplicationQualificationDTO,
)

router = APIRouter(prefix="/administration/qualifications", tags=["Qualification"])


@router.post("/{protocol_version_id}/application_versions/{version_id}")
def qualify_application_version_for_a_protocol(
    protocol_version_id: UUID,
    application_version_id: UUID,
    data: ApplicationQualificationCreateDTO,
    service: ProtocolApplicationQualificationService = Depends(
        get_protocol_application_qualification_service
    ),
) -> ProtocolApplicationQualificationDTO:
    protocol_version = service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version_id,
        application_version_id=application_version_id,
        qualification_date=data.qualification_date,
    )

    return map_protocol_qualification_entity_to_dto(protocol_version)


@router.delete("/{protocol_version_id}/application_versions/{application_version_id}")
def archive_application_version_qualification(
    protocol_version_id: UUID,
    application_version_id: UUID,
    service: ProtocolApplicationQualificationService = Depends(
        get_protocol_application_qualification_service
    ),
) -> ProtocolApplicationQualificationDTO:
    protocol_version = service.archive_protocol_application_qualification(
        protocol_version_id=protocol_version_id,
        application_version_id=application_version_id,
    )
    return map_protocol_qualification_entity_to_dto(protocol_version)
