import unittest

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationNotFoundException
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService


class TestApplicationCRUDOperations(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        repository_factory = RepositoryFactory()
        # setup services
        self.role_service = RolesService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.system_type_service = SystemTypeService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
            repository_factory=repository_factory,
        )
        self.vendor_service = VendorService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )

    def test_add_one_application(self) -> None:
        mock_role = self.role_service.add_one(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_by_names([mock_role.name])
        mock_system_types = self.system_type_service.get_many_by_names(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )
        actual_application = self.application_service.get_one(
            expected_application.id
        )

        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

    def test_delete_one_application_by_id(self) -> None:
        mock_role = self.role_service.add_one(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_by_names([mock_role.name])
        mock_system_types = self.system_type_service.get_many_by_names(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )

        actual_application = self.application_service.remove_one(
            expected_application.id
        )
        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.remove_one(actual_application.id)

            self.assertTrue("does not exist" not in str(context.exception))

    def test_delete_one_application_by_name(self) -> None:
        mock_role = self.role_service.add_one(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_by_names([mock_role.name])
        mock_system_types = self.system_type_service.get_many_by_names(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )
        actual_application = self.application_service.remove_one_by_name(
            application_name=expected_application.name, vendor_id=mock_vendor.id
        )

        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.remove_one_by_name(
                application_name=expected_application.name, vendor_id=mock_vendor.id
            )

            self.assertTrue("does not exist" not in str(context.exception))
