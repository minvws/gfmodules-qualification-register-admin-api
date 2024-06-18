from app.db.entities.healthcare_provider import HealthcareProvider
from app.schemas.healthcare_provider.schema import HealthcareProviderDTO


def map_healthcare_provider_entity_to_dto(
    entity: HealthcareProvider,
) -> HealthcareProviderDTO:
    return HealthcareProviderDTO(
        id=entity.id,
        ura_code=entity.ura_code,
        agb_code=entity.agb_code,
        trade_name=entity.trade_name,
        statutory_name=entity.statutory_name,
    )
