from app.db.entities.application_version import ApplicationVersion
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_application_version import (
    HealthcareProviderApplicationVersion,
)


class HealthcareProviderApplicationVersionFactory:
    @staticmethod
    def create_instance(
        healthcare_provider: HealthcareProvider, application_version: ApplicationVersion
    ) -> HealthcareProviderApplicationVersion:
        """
        Create a new rich instance of a HealthcareProviderApplicationVersion with parent child objects
        assigned
        """
        new_instance = HealthcareProviderApplicationVersion()
        new_instance.healthcare_provider = healthcare_provider
        new_instance.application_version = application_version

        return new_instance
