from datetime import date

import pytest

from app.db.entities import HealthcareProvider, Protocol, ProtocolVersion
from app.db.services import (
    HealthcareProviderQualificationService,
    HealthcareProviderService,
    ProtocolVersionService,
)
from app.exceptions.app_exceptions import (
    HealthcareProviderAlreadyQualifiedException,
    HealthcareProviderNotQualifiedForProtocolException,
    HealthcareProviderQualificationAlreadyArchivedException,
)
from tests.utests.db.services.utils import are_the_same_entity


def test_qualify_healthcare_provider(
    protocol_version_service: ProtocolVersionService,
    healthcare_provider_qualification_service: HealthcareProviderQualificationService,
    healthcare_provider_service: HealthcareProviderService,
    protocol: Protocol,
    healthcare_provider: HealthcareProvider,
) -> None:
    protocol_version = protocol_version_service.add_one(
        protocol_id=protocol.id,
        version="example",
        description="example",
    )

    expected_healthcare_provider = (
        healthcare_provider_qualification_service.qualify_healthcare_provider(
            healthcare_provider_id=healthcare_provider.id,
            protocol_version_id=protocol_version.id,
            qualification_date=date.today(),
        )
    )
    actual_healthcare_provider = healthcare_provider_service.get_one(
        healthcare_provider.id
    )

    assert expected_healthcare_provider.id == actual_healthcare_provider.id
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            actual_healthcare_provider.qualified_protocols,
            expected_healthcare_provider.qualified_protocols,
        )
    )


def test_duplicate_healthcare_provider_qualification_should_raise_exception(
    healthcare_provider_qualification_service: HealthcareProviderQualificationService,
    protocol_version: ProtocolVersion,
    healthcare_provider: HealthcareProvider,
) -> None:
    with pytest.raises(
        HealthcareProviderAlreadyQualifiedException,
        match="409: Healthcare provider already qualified for the protocol version",
    ):
        healthcare_provider_qualification_service.qualify_healthcare_provider(
            healthcare_provider_id=healthcare_provider.id,
            protocol_version_id=protocol_version.id,
            qualification_date=date.today(),
        )


def test_archive_healthcare_provider_qualification(
    healthcare_provider_qualification_service: HealthcareProviderQualificationService,
    healthcare_provider_service: HealthcareProviderService,
    protocol_version: ProtocolVersion,
    healthcare_provider: HealthcareProvider,
) -> None:
    expected_healthcare_provider = healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
        healthcare_provider_id=healthcare_provider.id,
        protocol_version_id=protocol_version.id,
    )
    actual_healthcare_provider = healthcare_provider_service.get_one(
        provider_id=healthcare_provider.id
    )
    assert expected_healthcare_provider.id == actual_healthcare_provider.id
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            actual_healthcare_provider.qualified_protocols,
            expected_healthcare_provider.qualified_protocols,
        )
    )


def test_archive_an_archived_healthcare_provider_qualification_should_raise_exception(
    healthcare_provider_qualification_service: HealthcareProviderQualificationService,
    protocol_version: ProtocolVersion,
    healthcare_provider: HealthcareProvider,
) -> None:
    healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
        healthcare_provider_id=healthcare_provider.id,
        protocol_version_id=protocol_version.id,
    )

    with pytest.raises(
        HealthcareProviderQualificationAlreadyArchivedException,
        match="409: Qualification is already archived for healthcare provider",
    ):
        healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
            healthcare_provider_id=healthcare_provider.id,
            protocol_version_id=protocol_version.id,
        )


def test_archive_a_non_qualified_healthcare_provider_should_raise_exception(
    protocol_version_service: ProtocolVersionService,
    protocol: Protocol,
    healthcare_provider_qualification_service: HealthcareProviderQualificationService,
    protocol_version: ProtocolVersion,
    healthcare_provider: HealthcareProvider,
) -> None:
    protocol_version = protocol_version_service.add_one(
        protocol_id=protocol.id,
        version="example",
        description="example",
    )

    with pytest.raises(
        HealthcareProviderNotQualifiedForProtocolException,
        match="404: Healthcare provider is not qualified for the protocol",
    ):
        healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
            healthcare_provider_id=healthcare_provider.id,
            protocol_version_id=protocol_version.id,
        )
