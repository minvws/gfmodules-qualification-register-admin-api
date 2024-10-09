from app.db.entities import Application, HealthcareProvider
from app.db.services import (
    HealthcareProviderApplicationVersionService,
    HealthcareProviderService,
)
from tests.utests.db.services.utils import are_the_same_entity


def test_assign_application_version_to_healthcare_provider(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
    application: Application,
    healthcare_provider_application_version_service: HealthcareProviderApplicationVersionService,
) -> None:
    expected_healthcare_provider = healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
        provider_id=healthcare_provider.id,
        application_version_id=application.versions[0].id,
    )

    actual_healthcare_provider = healthcare_provider_service.get_one(
        healthcare_provider.id
    )

    # assert if objects are equal
    assert expected_healthcare_provider.id == actual_healthcare_provider.id

    # assert versions are equal
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            actual_healthcare_provider.application_versions,
            expected_healthcare_provider.application_versions,
        )
    )


def test_unassign_application_version_to_healthcare_provider(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
    application: Application,
    healthcare_provider_application_version_service: HealthcareProviderApplicationVersionService,
) -> None:
    healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
        provider_id=healthcare_provider.id,
        application_version_id=application.versions[0].id,
    )
    assert healthcare_provider_service.get_one(
        healthcare_provider.id
    ).application_versions
    healthcare_provider_application_version_service.unassing_application_version_to_healthcare_provider(
        healthcare_provider_id=healthcare_provider.id,
        application_version_id=application.versions[0].id,
    )
    assert not healthcare_provider_service.get_one(
        healthcare_provider.id
    ).application_versions
