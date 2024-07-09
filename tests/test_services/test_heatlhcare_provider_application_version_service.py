import unittest

import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.healthcare_provider_application_version_service import (
    HealthcareProviderApplicationVersionService,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.db.session_factory import DbSessionFactory
from tests.utils.config_binder import config_binder


class TestHeathlhcareProviderApplicationVersionService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        repository_factory = RepositoryFactory()
        inject.configure(
            lambda binder: config_binder(binder, self.database),
            clear=True,
        )
        # setup service
        self.vendor_service = VendorService()
        self.role_service = RolesService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.system_type_service = SystemTypeService()
        self.application_service = ApplicationService()
        self.application_version_service = ApplicationVersionService(
            application_service=self.application_service,
        )
        self.protocol_service = ProtocolService()
        self.protocol_version_service = ProtocolVersionService(
            protocol_service=self.protocol_service,
        )

        self.healthcare_provider_service = HealthcareProviderService()
        self.healthcare_provider_application_version_service = (
            HealthcareProviderApplicationVersionService(
                healthcare_provider_service=self.healthcare_provider_service,
            )
        )

        # arrange
        self.mock_vendor = self.vendor_service.add_one(
            kvk_number="example", trade_name="example", statutory_name="example"
        )
        self.mock_role = self.role_service.add_one(
            name="example", description="example"
        )
        self.mock_system_type = self.system_type_service.add_one(
            name="example", description="example"
        )
        self.mock_application = self.application_service.add_one(
            vendor_id=self.mock_vendor.id,
            application_name="example",
            version="example",
            role_names=[self.mock_role.name],
            system_type_names=[self.mock_system_type.name],
        )
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
        self.mock_app_versions = self.application_version_service.get_many(
            application_id=self.mock_application.id
        )

    def test_assign_application_version_to_healthcare_provider(self) -> None:
        expected_healthcare_provider = self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=self.mock_app_versions[0].id,
        )

        actual_healthcare_provider = self.healthcare_provider_service.get_one(
            self.mock_healthcare_provider.id
        )

        # assert if objects are equal
        self.assertEqual(expected_healthcare_provider.id, actual_healthcare_provider.id)

        # assert versions are equal
        self.assertEqual(
            [
                version.to_dict()
                for version in expected_healthcare_provider.application_versions
            ],
            [
                version.to_dict()
                for version in actual_healthcare_provider.application_versions
            ],
        )

    def test_unassign_application_version_to_healthcare_provider(self) -> None:
        self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=self.mock_app_versions[0].id,
        )

        self.healthcare_provider_application_version_service.unassing_application_version_to_healthcare_provider(
            healthcare_provider_id=self.mock_healthcare_provider.id,
            application_version_id=self.mock_app_versions[0].id,
        )

        self.assertEqual(len(self.mock_healthcare_provider.application_versions), 0)

    def test_get_all_application_versions(self) -> None:
        expected_provider = self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=self.mock_app_versions[0].id,
        )
        self.healthcare_provider_application_version_service.get_healthcare_provider_application_versions(
            provider_id=self.mock_healthcare_provider.id
        )
        actual_provider = self.healthcare_provider_service.get_one(
            provider_id=self.mock_healthcare_provider.id
        )

        self.assertEqual(expected_provider.id, actual_provider.id)
        self.assertEqual(
            [version.to_dict() for version in expected_provider.application_versions],
            [version.to_dict() for version in actual_provider.application_versions],
        )
