from uuid import UUID

import pytest

from app.db.entities import HealthcareProvider, ProtocolVersion
from app.db.services import (
    HealthcareProviderService,
)
from app.exceptions.app_exceptions import (
    AGBCodeAlreadyExists,
    HealthcareProviderNotFoundException,
    URACodeAlreadyExists,
)
from app.schemas.healthcare_provider.mapper import map_healthcare_provider_entity_to_dto
from app.schemas.meta.schema import Page
from tests.utests.db.services.utils import are_the_same_entity


def test_add_one_healthcare_provider(
    healthcare_provider_service: HealthcareProviderService,
    protocol_version: ProtocolVersion,
) -> None:
    expected_healthcare_provider = healthcare_provider_service.add_one(
        ura_code="123456",
        agb_code="example agb code",
        trade_name="example trade name",
        statutory_name="example statutory name",
        protocol_version_id=protocol_version.id,
    )

    actual_healthcare_provider = healthcare_provider_service.get_one(
        provider_id=expected_healthcare_provider.id
    )

    assert expected_healthcare_provider.ura_code == actual_healthcare_provider.ura_code
    assert expected_healthcare_provider.agb_code == actual_healthcare_provider.agb_code
    assert (
        expected_healthcare_provider.statutory_name
        == actual_healthcare_provider.statutory_name
    )


def test_duplicate_ura_code_should_raise_exception(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
    protocol_version: ProtocolVersion,
) -> None:
    with pytest.raises(URACodeAlreadyExists, match="409: URA code already exists"):
        healthcare_provider_service.add_one(
            ura_code=healthcare_provider.ura_code,
            agb_code="some other agb code",
            trade_name="some other trade name",
            statutory_name="some other statutory name",
            protocol_version_id=protocol_version.id,
        )


def test_duplicate_agb_code_should_raise_exception(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
    protocol_version: ProtocolVersion,
) -> None:
    with pytest.raises(AGBCodeAlreadyExists, match="409: AGB code already exists"):
        healthcare_provider_service.add_one(
            ura_code="other example",
            agb_code=healthcare_provider.agb_code,
            trade_name="some other trade name",
            statutory_name="some other statutory name",
            protocol_version_id=protocol_version.id,
        )


def test_delete_one_healthcare_provider(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
) -> None:
    assert are_the_same_entity(
        healthcare_provider_service.remove_one(provider_id=healthcare_provider.id),
        healthcare_provider,
    )


def test_delete_non_existing_healthcare_provider(
    healthcare_provider_service: HealthcareProviderService,
) -> None:
    with pytest.raises(
        HealthcareProviderNotFoundException, match="404: Healthcare provider not found"
    ):
        healthcare_provider_service.get_one(
            provider_id=UUID("0fafbf14-7b06-4cd3-b278-cadad14ee6e1")
        )


def test_get_paginated_healthcare_providers(
    healthcare_provider: HealthcareProvider,
    healthcare_provider_service: HealthcareProviderService,
) -> None:
    assert healthcare_provider_service.get_paginated(limit=10, offset=0) == Page(
        limit=10,
        offset=0,
        items=[map_healthcare_provider_entity_to_dto(healthcare_provider)],
        total=1,
    )
