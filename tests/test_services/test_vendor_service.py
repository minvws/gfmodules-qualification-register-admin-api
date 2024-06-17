import unittest

from app.db.db import Database
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorCannotBeDeletedException,
)
from app.factory.vendor_factory import VendorFactory
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendor_application_service import VendorApplicationService
from app.db.services.vendors_service import VendorService


class TestVendorCRUD(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        # setup service
        self.vendor_service = VendorService(db_session_factory=db_session_factory)

        # arrange
        self.mock_vendor = VendorFactory.create_instance(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

    def test_add_one_vendor(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        actual_vendor = self.vendor_service.get_one_vendor_by_kvk_number(
            expected_vendor.kvk_number
        )

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

    def test_get_vendor_by_id(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )

        actual_vendor = self.vendor_service.get_one_vendor_by_id(expected_vendor.id)

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

    def test_delete_one_vendor_by_id(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        actual_vendor = self.vendor_service.delete_one_vendor_by_id(expected_vendor.id)

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

        with self.assertRaises(VendorNotFoundException) as context:
            self.vendor_service.get_one_vendor_by_id(expected_vendor.id)

            self.assertTrue("does not exist" not in str(context.exception))


class TestDeleteVendorWithRegisterdApplications(unittest.TestCase):
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
        self.application_servcice = ApplicationService(
            role_service=self.role_service,
            system_type_service=self.system_type_service,
            db_session_factory=db_session_factory,
        )
        self.vendor_application_service = VendorApplicationService(
            application_service=self.application_servcice,
            vendor_service=self.vendor_service,
            system_type_service=self.system_type_service,
            roles_service=self.role_service,
        )

        # arrange
        self.mock_vendor = VendorFactory.create_instance(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

    def test_delete_vendor_with_registered_applications(self) -> None:
        vendor = self.vendor_service.add_one_vendor(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        self.role_service.create_role("example_role", "example_role")
        self.system_type_service.add_one_system_type("example_type", "example_type")

        self.vendor_application_service.register_one_app(
            vendor_id=vendor.id,
            application_name="example app",
            application_version="1.0.0",
            system_type_names=["example_type"],
            role_names=["example_role"],
        )

        with self.assertRaises(VendorCannotBeDeletedException) as context:
            self.vendor_service.delete_one_vendor_by_id(vendor_id=vendor.id)

            self.assertTrue("does not exist" not in str(context.exception))
