import unittest

import inject

from app.db.db import Database
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.exceptions.app_exceptions import (
    URACodeAlreadyExists,
    AGBCodeAlreadyExists,
    HealthcareProviderNotFoundException,
)
from app.schemas.healthcare_provider.mapper import map_healthcare_provider_entity_to_dto
from app.schemas.meta.schema import Page
from tests.utils.config_binder import config_binder


class TestHealthcareProviderService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        inject.configure(
            lambda binder: config_binder(binder, self.database),
            clear=True,
        )
        # setup service
        self.protocol_service = ProtocolService()
        self.protocol_version_service = ProtocolVersionService(
            protocol_service=self.protocol_service
        )
        self.healthcare_provider_service = HealthcareProviderService()

        # setup data
        self.mock_protocol = self.protocol_service.add_one(
            protocol_type="Directive",
            name="example",
            description="example",
        )
        self.mock_protocol_version = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="example",
            description="example",
        )

    def test_add_one_healthcare_provider(self) -> None:
        expected_healthcare_provider = self.healthcare_provider_service.add_one(
            ura_code="123456",
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )

        actual_healthcare_provider = self.healthcare_provider_service.get_one(
            provider_id=expected_healthcare_provider.id
        )

        self.assertEqual(
            expected_healthcare_provider.ura_code, actual_healthcare_provider.ura_code
        )
        self.assertEqual(
            expected_healthcare_provider.agb_code, actual_healthcare_provider.agb_code
        )
        self.assertEqual(
            expected_healthcare_provider.statutory_name,
            actual_healthcare_provider.statutory_name,
        )

    def test_duplicate_ura_code_should_raise_exception(self) -> None:
        ura_code = "123456"
        self.healthcare_provider_service.add_one(
            ura_code=ura_code,
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )

        with self.assertRaises(URACodeAlreadyExists) as context:
            self.healthcare_provider_service.add_one(
                ura_code=ura_code,
                agb_code="some other agb code",
                trade_name="some other trade name",
                statutory_name="some other statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )
            self.assertTrue("ura code does not exits" in str(context.exception))

    def test_duplicate_agb_code_should_raise_exception(self) -> None:
        agb_code = "example agb code"
        self.healthcare_provider_service.add_one(
            ura_code="123456",
            agb_code=agb_code,
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )

        with self.assertRaises(AGBCodeAlreadyExists) as context:
            self.healthcare_provider_service.add_one(
                ura_code="456789",
                agb_code=agb_code,
                trade_name="some other trade name",
                statutory_name="some other statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )

            self.assertTrue("agb code does not exits" in str(context.exception))

    def test_delete_one_healthcare_provider(self) -> None:
        expected_healthcare_provider = self.healthcare_provider_service.add_one(
            ura_code="example ura code",
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )
        self.healthcare_provider_service.remove_one(
            provider_id=expected_healthcare_provider.id
        )

        with self.assertRaises(HealthcareProviderNotFoundException) as context:
            self.healthcare_provider_service.get_one(
                provider_id=expected_healthcare_provider.id
            )

            self.assertTrue("healthcare provider not found" in str(context.exception))

    def test_get_paginated_healthcare_providers(self) -> None:
        new_healthcare_provider = self.healthcare_provider_service.add_one(
            ura_code="example ura code",
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )
        expected_healthcare_providers = Page(
            limit=10,
            offset=0,
            items=[map_healthcare_provider_entity_to_dto(new_healthcare_provider)],
            total=1,
        )
        actual_healthcare_providers = self.healthcare_provider_service.get_paginated(
            limit=10, offset=0
        )

        self.assertEqual(expected_healthcare_providers, actual_healthcare_providers)