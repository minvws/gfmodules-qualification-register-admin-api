import unittest

from app.db.db import Database
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationVersionDeleteException
from app.factory.vendor_factory import VendorFactory
from app.services.application_service import ApplicationService
from app.services.application_version_service import ApplicationVersionService
from app.services.roles_service import RolesService
from app.services.system_type_service import SystemTypeService
from app.services.vendor_application_service import VendorApplicationService
from app.services.vendors_service import VendorService


class TestApplicationVersionService(unittest.TestCase):
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
            role_service=self.role_service,
            system_type_service=self.system_type_service,
            db_session_factory=db_session_factory,
        )
        self.application_version_service = ApplicationVersionService(
            application_service=self.application_service,
            db_session_factory=db_session_factory,
        )
        self.vendor_application_service = VendorApplicationService(
            application_service=self.application_service,
            vendor_service=self.vendor_service,
            system_type_service=self.system_type_service,
            roles_service=self.role_service,
        )

        # arrange
        self.mock_vendor = VendorFactory.create_instance(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

    def test_add_application_version(self) -> None:
        vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        self.role_service.create_role("example_role", "example_role")
        self.system_type_service.add_one_system_type("example_type", "example_type")

        mock_app = self.vendor_application_service.register_one_app(
            vendor_id=vendor.id,
            application_name="example app",
            application_version="1.0.0",
            system_type_names=["example_type"],
            role_names=["example_role"],
        )

        expected_app_versions = [version.to_dict() for version in mock_app.versions]
        actual_db_app_version = (
            self.application_version_service.get_one_application_versions(
                mock_app.id,
            )
        )
        actual_app_version = [version.to_dict() for version in actual_db_app_version]

        self.assertListEqual(expected_app_versions, actual_app_version)

    def test_delete_application_version(self) -> None:
        vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        self.role_service.create_role("example_role", "example_role")
        self.system_type_service.add_one_system_type("example_type", "example_type")

        mock_app = self.vendor_application_service.register_one_app(
            vendor_id=vendor.id,
            application_name="example app",
            application_version="1.0.0",
            system_type_names=["example_type"],
            role_names=["example_role"],
        )
        new_versions = self.application_version_service.add_application_version(
            mock_app.id, "v1.0.1"
        )
        version_1 = new_versions[1]
        version_2 = new_versions[0]
        self.application_version_service.delete_application_version(
            application_id=mock_app.id, version_id=version_1.id
        )

        with self.assertRaises(ApplicationVersionDeleteException) as context:
            self.application_version_service.delete_application_version(
                mock_app.id, version_2.id
            )

            self.assertTrue("does not exist" not in str(context.exception))
