from app.db.entities.application_version_qualification import (
    ProtocolApplicationQualification,
)
from app.db.entities.protocol_version import ProtocolVersion
from app.schemas.protocol_application_qualification.schema import (
    ProtocolApplicationQualificationDto,
    QualifiedApplicationVersionDto,
)


def map_protocol_version_application_entity_to_dto(
    entity: ProtocolApplicationQualification,
) -> QualifiedApplicationVersionDto:
    return QualifiedApplicationVersionDto(
        qualification_id=entity.id,
        application_id=entity.application_version.application_id,
        version_id=entity.application_version_id,
        version=entity.application_version.version,
        qualification_date=entity.qualification_date,
        archived_date=entity.archived_date,
    )


def map_protocol_qualification_entity_to_dto(
    entity: ProtocolVersion,
) -> ProtocolApplicationQualificationDto:
    application_versions = [
        map_protocol_version_application_entity_to_dto(version)
        for version in entity.qualified_application_versions
    ]

    return ProtocolApplicationQualificationDto(
        id=entity.id,
        protocol_id=entity.protocol_id,
        version=entity.version,
        description=entity.description,
        application_versions=application_versions,
    )
