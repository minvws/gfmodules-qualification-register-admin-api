import unittest

from app.db.db import Database
from app.exceptions.app_exceptions import ApplicationNotFoundException
from app.factory.application_factory import ApplicationFactory
from app.services.application_service import ApplicationService
from app.services.vendor_application_service import VendorApplicationService
from app.services.vendors_service import VendorService


class TestRegisterVendorApplication(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(self.database)
        self.application_service = ApplicationService(self.database)
        self.vendor_application_service = VendorApplicationService(
            vendor_service=self.vendor_service,
            application_service=self.application_service,
        )

        # setup factory
        self.application_factory = ApplicationFactory()

    def test_register_vendor_application(self) -> None:
        new_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example-vendor",
        )
        expected_application = self.application_factory.create_instance(
            "example-application", "1.0.0"
        )

        self.vendor_application_service.register_one_application(
            kvk_number=new_vendor.kvk_number,
            application_name=expected_application.name,
            application_version="1.0.0",
        )
        actual_application = self.vendor_application_service.get_one_vendor_application(
            kvk_number=new_vendor.kvk_number,
            application_name=expected_application.name,
        )

        self.assertEqual(actual_application.vendor_id, new_vendor.id)
        self.assertEqual(actual_application.name, actual_application.name)


class TestDeregisterVendorApplication(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(self.database)
        self.application_service = ApplicationService(self.database)
        self.vendor_application_service = VendorApplicationService(
            vendor_service=self.vendor_service,
            application_service=self.application_service,
        )

        # setup factory
        self.application_factory = ApplicationFactory()

    def test_deregister_one_vendor_application(self) -> None:
        new_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example-vendor",
        )
        expected_application = self.application_factory.create_instance(
            "example-application", "1.0.0"
        )
        self.vendor_application_service.register_one_application(
            kvk_number=new_vendor.kvk_number,
            application_name=expected_application.name,
            application_version="1.0.0",
        )

        self.vendor_application_service.deregister_one_vendor_application(
            kvk_number=new_vendor.kvk_number,
            application_name=expected_application.name,
        )

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.vendor_application_service.get_one_vendor_application(
                kvk_number=new_vendor.kvk_number,
                application_name=expected_application.name,
            )

            self.assertTrue("No such application" in str(context.exception))


class TestRetrievingAllVendorApplication(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(self.database)
        self.application_service = ApplicationService(self.database)
        self.vendor_application_service = VendorApplicationService(
            vendor_service=self.vendor_service,
            application_service=self.application_service,
        )

        # setup factory
        self.application_factory = ApplicationFactory()

    def test_retrieving_all_vendor_applications(self) -> None:
        new_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example-vendor",
        )
        new_app_1 = self.application_factory.create_instance(
            "example-application-1", "1.0.0"
        )
        new_app_2 = self.application_factory.create_instance(
            "example-application-2", "1.0.0"
        )

        expected_vendor_apps = [new_app_1, new_app_2]
        self.vendor_application_service.register_one_application(
            kvk_number=new_vendor.kvk_number,
            application_name=new_app_1.name,
            application_version="1.0.0",
        )
        self.vendor_application_service.register_one_application(
            kvk_number=new_vendor.kvk_number,
            application_name=new_app_2.name,
            application_version="1.0.0",
        )

        actual_vendor_apps = (
            self.vendor_application_service.get_all_vendor_applications(
                new_vendor.kvk_number
            )
        )

        self.assertEqual(len(expected_vendor_apps), len(actual_vendor_apps))
