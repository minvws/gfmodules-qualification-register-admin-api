from datetime import date
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.protocol_version import ProtocolVersion
from app.factory.healthcare_provider_qualification_factory import (
    HealthcareProviderQualificationFactory,
)


class HealthcareProviderFactory:
    @staticmethod
    def create_instance(
        ura_code: str,
        agb_code: str,
        trade_name: str,
        statutory_name: str,
        protocol_version: ProtocolVersion,
    ) -> HealthcareProvider:
        new_healthcare_provider = HealthcareProvider(
            ura_code=ura_code,
            agb_code=agb_code,
            trade_name=trade_name,
            statutory_name=statutory_name,
        )
        qualified_protocol_version = (
            HealthcareProviderQualificationFactory.create_instance(
                healthcare_provider=new_healthcare_provider,
                protocol_version=protocol_version,
                qualification_date=date.today(),
            )
        )
        new_healthcare_provider.qualified_protocols.append(qualified_protocol_version)
        return new_healthcare_provider
