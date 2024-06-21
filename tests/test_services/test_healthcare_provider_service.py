import unittest

from app.db.db import Database
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    URACodeAlreadyExists,
    AGBCodeAlreadyExists,
    HealthcareProviderNotFoundException,
)


class TestHealthcareProviderService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        # setup service
        self.protocol_service = ProtocolService(db_session_factory=db_session_factory)
        self.protocol_version_service = ProtocolVersionService(
            db_session_factory=db_session_factory,
            protocol_service=self.protocol_service,
        )
        self.healthcare_provider_service = HealthcareProviderService(
            db_session_factory=db_session_factory
        )

        # setup data
        self.mock_protocol = self.protocol_service.create_one(
            protocol_type="Directive",
            name="example",
            description="example",
        )
        self.mock_protocol_version = (
            self.protocol_version_service.add_one_protocol_version(
                protocol_id=self.mock_protocol.id,
                version="example",
                description="example",
            )
        )

    def test_add_one_healthcare_provider(self) -> None:
        expected_healthcare_provider = (
            self.healthcare_provider_service.add_one_provider(
                ura_code="123456",
                agb_code="example agb code",
                trade_name="example trade name",
                statutory_name="example statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )
        )

        actual_healthcare_provider = self.healthcare_provider_service.get_one_by_id(
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

    def test_duplicate_ura_code_shoud_raise_exception(self) -> None:
        ura_code = "123456"
        self.healthcare_provider_service.add_one_provider(
            ura_code=ura_code,
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )

        with self.assertRaises(URACodeAlreadyExists) as context:
            self.healthcare_provider_service.add_one_provider(
                ura_code=ura_code,
                agb_code="some other agb code",
                trade_name="some other trade name",
                statutory_name="some other statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )
            self.assertTrue("ura code does not exits" in str(context.exception))

    def test_duplicate_agb_code_shoud_raise_exception(self) -> None:
        agb_code = "example agb code"
        self.healthcare_provider_service.add_one_provider(
            ura_code="123456",
            agb_code=agb_code,
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )

        with self.assertRaises(AGBCodeAlreadyExists) as context:
            self.healthcare_provider_service.add_one_provider(
                ura_code="456789",
                agb_code=agb_code,
                trade_name="some other trade name",
                statutory_name="some other statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )

            self.assertTrue("agb code does not exits" in str(context.exception))

    def test_delete_one_healthcare_provider(self) -> None:
        expected_healthcare_provider = (
            self.healthcare_provider_service.add_one_provider(
                ura_code="example ura code",
                agb_code="example agb code",
                trade_name="example trade name",
                statutory_name="example statutory name",
                protocol_version_id=self.mock_protocol_version.id,
            )
        )
        self.healthcare_provider_service.delete_one_healthcare_provider(
            provider_id=expected_healthcare_provider.id
        )

        with self.assertRaises(HealthcareProviderNotFoundException) as context:
            self.healthcare_provider_service.get_one_by_id(
                provider_id=expected_healthcare_provider.id
            )

            self.assertTrue("healthcare provider not found" in str(context.exception))

    def test_get_all_healthcare_providers(self) -> None:
        new_healthcare_provider = self.healthcare_provider_service.add_one_provider(
            ura_code="example ura code",
            agb_code="example agb code",
            trade_name="example trade name",
            statutory_name="example statutory name",
            protocol_version_id=self.mock_protocol_version.id,
        )
        expected_healthcare_providers = [new_healthcare_provider.to_dict()]
        actual_db_healthcare_providers = (
            self.healthcare_provider_service.get_all_healthcare_providers()
        )
        actual_healthcare_providers = [
            provider.to_dict() for provider in actual_db_healthcare_providers
        ]

        self.assertCountEqual(
            expected_healthcare_providers, actual_healthcare_providers
        )
