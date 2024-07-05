import unittest

import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorCannotBeDeletedException,
)
from app.factory.vendor_factory import VendorFactory
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from tests.utils.config_binder import config_binder


class TestVendorCRUD(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        repository_factory = RepositoryFactory()

        inject.configure(
            lambda binder: binder.bind(DbSessionFactory, db_session_factory).bind(  # type: ignore
                RepositoryFactory, repository_factory
            ),
            clear=True,
        )

        # setup service
        self.vendor_service = VendorService()

        # arrange
        self.mock_vendor = VendorFactory.create_instance(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

    def test_add_one_vendor(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        actual_vendor = self.vendor_service.get_one_by_kvk_number(
            expected_vendor.kvk_number
        )

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

    def test_get_vendor_by_id(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )

        actual_vendor = self.vendor_service.get_one(expected_vendor.id)

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

    def test_delete_one_vendor_by_id(self) -> None:
        # act
        expected_vendor = self.vendor_service.add_one(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        actual_vendor = self.vendor_service.remove_one(expected_vendor.id)

        # assert
        self.assertEqual(expected_vendor.id, actual_vendor.id)
        self.assertEqual(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEqual(expected_vendor.trade_name, actual_vendor.trade_name)

        with self.assertRaises(VendorNotFoundException) as context:
            self.vendor_service.get_one(expected_vendor.id)

            self.assertTrue("does not exist" not in str(context.exception))


class TestDeleteVendorWithRegisterdApplications(unittest.TestCase):
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
        self.application_servcice = ApplicationService()

        # arrange
        self.mock_vendor = VendorFactory.create_instance(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

    def test_delete_vendor_with_registered_applications(self) -> None:
        vendor = self.vendor_service.add_one(
            kvk_number=self.mock_vendor.kvk_number,
            trade_name=self.mock_vendor.trade_name,
            statutory_name=self.mock_vendor.statutory_name,
        )
        self.role_service.add_one("example_role", "example_role")
        self.system_type_service.add_one("example_type", "example_type")

        self.application_servcice.add_one(
            vendor_id=vendor.id,
            application_name="example app",
            version="1.0.0",
            system_type_names=["example_type"],
            role_names=["example_role"],
        )

        with self.assertRaises(VendorCannotBeDeletedException) as context:
            self.vendor_service.remove_one(vendor_id=vendor.id)

            self.assertTrue("does not exist" not in str(context.exception))
