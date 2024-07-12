import unittest
from datetime import date

import inject

from app.db.db import Database
from app.db.services.healthcare_provider_qualification_service import (
    HealthcareProviderQualificationService,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.exceptions.app_exceptions import (
    HealthcareProviderAlreadyQualifiedException,
    HealthcareProviderQualificationAlreadyArchivedException,
    HealthcareProviderNotQualifiedForProtocolException,
)
from tests.utils.config_binder import config_binder


class TestHealthcareProviderQualificationService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup injector
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
        self.healthcare_provider_qualification_service = (
            HealthcareProviderQualificationService()
        )

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

        self.mock_healthcare_provider = self.healthcare_provider_service.add_one(
            ura_code="example",
            agb_code="example",
            trade_name="example",
            statutory_name="example",
            protocol_version_id=self.mock_protocol_version.id,
        )

    def test_qualify_healthcare_provider(self) -> None:
        mock_protocol_version_2 = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="example",
            description="example",
        )

        expected_healthcare_provider = (
            self.healthcare_provider_qualification_service.qualify_healthcare_provider(
                healthcare_provider_id=self.mock_healthcare_provider.id,
                protocol_version_id=mock_protocol_version_2.id,
                qualification_date=date.today(),
            )
        )
        actual_healthcare_provider = self.healthcare_provider_service.get_one(
            self.mock_healthcare_provider.id
        )

        self.assertEqual(expected_healthcare_provider.id, actual_healthcare_provider.id)
        self.assertEqual(
            [
                version.to_dict()
                for version in expected_healthcare_provider.qualified_protocols
            ],
            [
                version.to_dict()
                for version in actual_healthcare_provider.qualified_protocols
            ],
        )

    def test_duplicate_healthcare_provider_qualification_should_raise_exception(
        self,
    ) -> None:
        with self.assertRaises(HealthcareProviderAlreadyQualifiedException) as context:
            self.healthcare_provider_qualification_service.qualify_healthcare_provider(
                healthcare_provider_id=self.mock_healthcare_provider.id,
                protocol_version_id=self.mock_protocol_version.id,
                qualification_date=date.today(),
            )

            self.assertTrue(
                "Healthcare provider already qualified" in str(context.exception)
            )

    def test_archive_healthcare_provider_qualification(self) -> None:
        expected_healthcare_provider = self.healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
            healthcare_provider_id=self.mock_healthcare_provider.id,
            protocol_version_id=self.mock_protocol_version.id,
        )
        actual_healthcare_provider = self.healthcare_provider_service.get_one(
            provider_id=self.mock_healthcare_provider.id
        )

        self.assertEqual(expected_healthcare_provider.id, actual_healthcare_provider.id)
        self.assertEqual(
            [
                version.to_dict()
                for version in expected_healthcare_provider.qualified_protocols
            ],
            [
                version.to_dict()
                for version in actual_healthcare_provider.qualified_protocols
            ],
        )

    def test_archive_an_archived_healthcare_provider_qualification_should_raise_exception(
        self,
    ) -> None:
        self.healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
            healthcare_provider_id=self.mock_healthcare_provider.id,
            protocol_version_id=self.mock_protocol_version.id,
        )

        with self.assertRaises(
            HealthcareProviderQualificationAlreadyArchivedException
        ) as context:
            self.healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
                healthcare_provider_id=self.mock_healthcare_provider.id,
                protocol_version_id=self.mock_protocol_version.id,
            )

            self.assertTrue("already archived" in str(context.exception))

    def test_archive_a_non_qualified_healthcare_provider_should_raise_exception(
        self,
    ) -> None:
        mock_protocol_version_2 = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="example",
            description="example",
        )

        with self.assertRaises(
            HealthcareProviderNotQualifiedForProtocolException
        ) as context:
            self.healthcare_provider_qualification_service.archive_healthcare_provider_qualification(
                healthcare_provider_id=self.mock_healthcare_provider.id,
                protocol_version_id=mock_protocol_version_2.id,
            )

            self.assertTrue("not qualified" in str(context.exception))
