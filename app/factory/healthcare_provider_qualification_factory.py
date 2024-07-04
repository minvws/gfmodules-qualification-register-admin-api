from datetime import date

from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_qualification import (
    HealthcareProviderQualification,
)
from app.db.entities.protocol_version import ProtocolVersion


class HealthcareProviderQualificationFactory:
    """
    Factory class to create an instance of the HealthcareProviderQualification association between
    parent HealthcareProvider and child ProtocolVersion
    """

    @staticmethod
    def create_instance(
        healthcare_provider: HealthcareProvider,
        protocol_version: ProtocolVersion,
        qualification_date: date,
    ) -> HealthcareProviderQualification:
        new_instance = HealthcareProviderQualification(
            qualification_date=qualification_date
        )
        new_instance.protocol_version = protocol_version
        new_instance.healthcare_provider = healthcare_provider
        return new_instance
