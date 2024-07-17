from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_application_version import (
    HealthcareProviderApplicationVersion,
)
from app.db.entities.healthcare_provider_qualification import (
    HealthcareProviderQualification,
)
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderDto,
    HealthcareProviderApplicationVersionDto,
    QualifiedProtocolVersionsDto,
)


def map_qualified_protoco_versions_entity_to_dto(
    entity: HealthcareProviderQualification,
) -> QualifiedProtocolVersionsDto:
    return QualifiedProtocolVersionsDto(
        id=entity.id,
        protocol_id=entity.protocol_version.protocol_id,
        version_id=entity.protocol_version_id,
        version=entity.protocol_version.version,
        description=entity.protocol_version.description,
        qualification_date=entity.qualification_date,
        archived_date=entity.archived_date,
    )


def map_healthcare_provider_app_version_entity_to_dto(
    entity: HealthcareProviderApplicationVersion,
) -> HealthcareProviderApplicationVersionDto:
    return HealthcareProviderApplicationVersionDto(
        id=entity.application_version.id, version=entity.application_version.version
    )


def map_healthcare_provider_entity_to_dto(
    entity: HealthcareProvider,
) -> HealthcareProviderDto:
    return HealthcareProviderDto(
        id=entity.id,
        ura_code=entity.ura_code,
        agb_code=entity.agb_code,
        trade_name=entity.trade_name,
        statutory_name=entity.statutory_name,
        application_versions=[
            map_healthcare_provider_app_version_entity_to_dto(version)
            for version in entity.application_versions
        ],
        qualified_protocols=[
            map_qualified_protoco_versions_entity_to_dto(protocol)
            for protocol in entity.qualified_protocols
        ],
    )
