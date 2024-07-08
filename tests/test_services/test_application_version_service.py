import unittest

import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationVersionDeleteException
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from tests.utils.config_binder import config_binder


class TestApplicationVersionService(unittest.TestCase):
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
            db_session_factory=db_session_factory,
            repository_factory=repository_factory,
        )

        # arrange
        self.mock_vendor = self.vendor_service.add_one(
            kvk_number="123456",
            trade_name="example",
            statutory_name="example bv",
        )
        self.mock_role = self.role_service.add_one("example_role", "example_role")
        self.mock_system_type = self.system_type_service.add_one(
            "example_type", "example_type"
        )

        self.mock_app = self.application_service.add_one(
            vendor_id=self.mock_vendor.id,
            application_name="example app",
            version="1.0.0",
            system_type_names=[self.mock_system_type.name],
            role_names=[self.mock_role.name],
        )

    def test_add_application_version(self) -> None:
        expected_app_versions = [
            version.to_dict() for version in self.mock_app.versions
        ]
        actual_db_app_version = self.application_version_service.get_many(
            self.mock_app.id,
        )
        actual_app_version = [version.to_dict() for version in actual_db_app_version]

        self.assertListEqual(expected_app_versions, actual_app_version)

    def test_delete_application_version(self) -> None:
        new_versions = self.application_version_service.add_one(
            self.mock_app.id, "v1.0.1"
        )
        version_1 = new_versions[1]
        version_2 = new_versions[0]
        self.application_version_service.remove_one(
            application_id=self.mock_app.id, version_id=version_1.id
        )

        with self.assertRaises(ApplicationVersionDeleteException) as context:
            self.application_version_service.remove_one(self.mock_app.id, version_2.id)

            self.assertTrue("does not exist" not in str(context.exception))
