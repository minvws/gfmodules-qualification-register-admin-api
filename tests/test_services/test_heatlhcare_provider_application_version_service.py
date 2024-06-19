import unittest

from app.db.db import Database
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.healthcare_provider_application_version_service import (
    HealthcareProviderApplicationVersionService,
)
from app.db.services.healthcare_provider_service import HealthcareProviderService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.db.session_factory import DbSessionFactory


class TestHeathlhcareProviderApplicationVersionService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        # setup service
        self.vendor_service = VendorService(db_session_factory=db_session_factory)
        self.role_service = RolesService(db_session_factory=db_session_factory)
        self.system_type_service = SystemTypeService(
            db_session_factory=db_session_factory
        )
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
        )
        self.application_version_service = ApplicationVersionService(
            application_service=self.application_service,
            db_session_factory=db_session_factory,
        )

        self.healthcare_provider_service = HealthcareProviderService(
            db_session_factory=db_session_factory
        )
        self.healthcare_provider_application_version_service = (
            HealthcareProviderApplicationVersionService(
                db_session_factory=db_session_factory,
                healthcare_provider_service=self.healthcare_provider_service,
            )
        )

        # setup data
        self.mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="example", trade_name="example", statutory_name="example"
        )
        self.mock_role = self.role_service.create_role(
            name="example", description="example"
        )
        self.mock_system_type = self.system_type_service.add_one_system_type(
            name="example", description="example"
        )
        self.mock_application = self.application_service.add_one_application(
            vendor=self.mock_vendor,
            application_name="example",
            version="example",
            roles=[self.mock_role],
            system_types=[self.mock_system_type],
        )
        self.mock_healthcare_provider = (
            self.healthcare_provider_service.add_one_provider(
                ura_code="example",
                agb_code="example",
                trade_name="example",
                statutory_name="example",
            )
        )

    def test_assign_application_version_to_healthcare_provider(self) -> None:
        mock_app_versions = (
            self.application_version_service.get_one_application_versions(
                application_id=self.mock_application.id
            )
        )
        expected_healthcare_provider = self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=mock_app_versions[0].id,
        )

        actual_healthcare_provider = self.healthcare_provider_service.get_one_by_id(
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
        mock_app_versions = (
            self.application_version_service.get_one_application_versions(
                application_id=self.mock_application.id
            )
        )
        self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=mock_app_versions[0].id,
        )

        self.healthcare_provider_application_version_service.unassing_application_version_to_healthcare_provider(
            healthcare_provider_id=self.mock_healthcare_provider.id,
            application_version_id=mock_app_versions[0].id,
        )

        self.assertEqual(len(self.mock_healthcare_provider.application_versions), 0)

    def test_get_all_application_versions(self) -> None:
        mock_app_versions = (
            self.application_version_service.get_one_application_versions(
                application_id=self.mock_application.id
            )
        )
        expected_provider = self.healthcare_provider_application_version_service.assign_application_version_to_healthcare_provider(
            provider_id=self.mock_healthcare_provider.id,
            application_version_id=mock_app_versions[0].id,
        )
        self.healthcare_provider_application_version_service.get_healthcare_provider_application_versions(
            provider_id=self.mock_healthcare_provider.id
        )
        actual_provider = self.healthcare_provider_service.get_one_by_id(
            provider_id=self.mock_healthcare_provider.id
        )

        self.assertEqual(expected_provider.id, actual_provider.id)
        self.assertEqual(
            [version.to_dict() for version in expected_provider.application_versions],
            [version.to_dict() for version in actual_provider.application_versions],
        )
