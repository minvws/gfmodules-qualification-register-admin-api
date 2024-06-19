from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_application_version import (
    HealthcareProviderApplicationVersion,
)
from app.schemas.healthcare_provider.schema import (
    HealthcareProviderDTO,
    HealthcareProviderApplicationVersionDTO,
)


def map_healthcare_provider_app_version_entity_to_dto(
    entity: HealthcareProviderApplicationVersion,
) -> HealthcareProviderApplicationVersionDTO:
    return HealthcareProviderApplicationVersionDTO(
        id=entity.application_version.id, version=entity.application_version.version
    )


def map_healthcare_provider_entity_to_dto(
    entity: HealthcareProvider,
) -> HealthcareProviderDTO:
    return HealthcareProviderDTO(
        id=entity.id,
        ura_code=entity.ura_code,
        agb_code=entity.agb_code,
        trade_name=entity.trade_name,
        statutory_name=entity.statutory_name,
        application_versions=[
            map_healthcare_provider_app_version_entity_to_dto(version)
            for version in entity.application_versions
        ],
    )
