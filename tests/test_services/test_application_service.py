import unittest

from app.db.db import Database
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationNotFoundException
from app.services.application_service import ApplicationService
from app.services.roles_service import RolesService
from app.services.system_type_service import SystemTypeService
from app.services.vendors_service import VendorService


class TestApplicationCRUDOperations(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)

        # setup services
        self.role_service = RolesService(db_session_factory=db_session_factory)
        self.system_type_service = SystemTypeService(
            db_session_factory=db_session_factory
        )
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
        )
        self.vendor_service = VendorService(db_session_factory=db_session_factory)

    def test_add_one_application(self) -> None:
        mock_role = self.role_service.create_role(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one_system_type(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_roles([mock_role.name])
        mock_system_types = self.system_type_service.get_many_system_types(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one_application(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )
        actual_application = self.application_service.get_one_application_by_id(
            expected_application.id
        )

        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

    def test_delete_one_application_by_id(self) -> None:
        mock_role = self.role_service.create_role(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one_system_type(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_roles([mock_role.name])
        mock_system_types = self.system_type_service.get_many_system_types(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one_application(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )

        actual_application = self.application_service.delete_one_application_by_id(
            expected_application.id
        )
        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.delete_one_application_by_id(actual_application.id)

            self.assertTrue("does not exist" not in str(context.exception))

    def test_delete_one_application_by_name(self) -> None:
        mock_role = self.role_service.create_role(
            name="example_role_1", description="some description"
        )
        mock_system_type = self.system_type_service.add_one_system_type(
            name="example_system_type", description="some description"
        )
        mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        mock_roles = self.role_service.get_many_roles([mock_role.name])
        mock_system_types = self.system_type_service.get_many_system_types(
            [mock_system_type.name]
        )

        expected_application = self.application_service.add_one_application(
            vendor=mock_vendor,
            roles=mock_roles,
            system_types=mock_system_types,
            application_name="example application",
            version="v1.0.0",
        )
        actual_application = self.application_service.delete_one_application_by_name(
            application_name=expected_application.name, vendor_id=mock_vendor.id
        )

        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(expected_application.name, actual_application.name)
        self.assertEqual(expected_application.vendor.id, actual_application.vendor.id)

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.delete_one_application_by_name(
                application_name=expected_application.name, vendor_id=mock_vendor.id
            )

            self.assertTrue("does not exist" not in str(context.exception))
