import unittest

from app.db.db import Database
from app.services.vendors_service import VendorService


class TestAddingOneService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(database=self.database)

    def test_add_one_vendor(self) -> None:

        # act
        expected_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example statutory",
        )
        actual_vendor = self.vendor_service.get_one_vendor("123456")

        self.assertEquals(expected_vendor.id, actual_vendor.id)
        self.assertEquals(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEquals(expected_vendor.trade_name, actual_vendor.trade_name)


class TestRetrievingAllVendors(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(database=self.database)

    def test_getting_all_vendors(self) -> None:
        expected_vendors_1 = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example-vendor",
        )
        expected_vendors_2 = self.vendor_service.add_one_vendor(
            kvk_number="456789",
            trade_name="example vendor 2",
            statutory_name="example-vendor-2",
        )

        expected_vendors = [expected_vendors_1.to_dict(), expected_vendors_2.to_dict()]
        actual_vendors_list = self.vendor_service.get_all_vendors()
        actual_vendors = [vendor.to_dict() for vendor in actual_vendors_list]

        self.assertEquals(len(expected_vendors), len(actual_vendors))
        self.assertCountEqual(expected_vendors, actual_vendors)


class TestRemovingOneVendor(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(database=self.database)

    def test_removing_one_vendor(self) -> None:
        expected_vendor = self.vendor_service.add_one_vendor(
            kvk_number="123456",
            trade_name="example vendor",
            statutory_name="example-vendor",
        )

        actual_vendor = self.vendor_service.delete_one_vendor("123456")

        self.assertEquals(expected_vendor.id, actual_vendor.id)
        self.assertEquals(expected_vendor.kvk_number, actual_vendor.kvk_number)
        self.assertEquals(expected_vendor.trade_name, actual_vendor.trade_name)
