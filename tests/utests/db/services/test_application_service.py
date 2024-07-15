import unittest

import inject

from app.db.db import Database
from app.exceptions.app_exceptions import ApplicationNotFoundException
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RoleService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.schemas.application.mapper import map_application_entity_to_dto
from app.schemas.meta.schema import Page
from tests.utils.config_binder import config_binder


class TestApplicationCRUDOperations(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        inject.configure(
            lambda binder: config_binder(binder, self.database),
            clear=True,
        )
        # setup services
        self.role_service = RoleService()
        self.system_type_service = SystemTypeService()
        self.application_service = ApplicationService()
        self.vendor_service = VendorService()
        self.mock_role = self.role_service.add_one(
            name="example_role_1", description="some description"
        )
        self.mock_system_type = self.system_type_service.add_one(
            name="example_system_type", description="some description"
        )
        self.mock_vendor = self.vendor_service.add_one(
            kvk_number="123456", trade_name="example", statutory_name="example bv"
        )

        self.expected_application = self.application_service.add_one(
            vendor_id=self.mock_vendor.id,
            application_name="example application",
            version="v1.0.0",
            system_type_names=[self.mock_system_type.name],
            role_names=[self.mock_role.name],
        )

    def test_add_one_application(self) -> None:
        actual_application = self.application_service.get_one(
            self.expected_application.id
        )

        self.assertEqual(self.expected_application.id, actual_application.id)
        self.assertEqual(self.expected_application.name, actual_application.name)
        self.assertEqual(
            self.expected_application.vendor.id, actual_application.vendor.id
        )

    def test_delete_one_application_by_id(self) -> None:
        actual_application = self.application_service.remove_one(
            self.expected_application.id
        )
        self.assertEqual(self.expected_application.id, actual_application.id)
        self.assertEqual(self.expected_application.name, actual_application.name)
        self.assertEqual(
            self.expected_application.vendor.id, actual_application.vendor.id
        )

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.remove_one(actual_application.id)

            self.assertTrue("does not exist" not in str(context.exception))

    def test_delete_one_application_by_name(self) -> None:
        actual_application = self.application_service.remove_one_by_name(
            application_name=self.expected_application.name,
            vendor_id=self.mock_vendor.id,
        )

        self.assertEqual(self.expected_application.id, actual_application.id)
        self.assertEqual(self.expected_application.name, actual_application.name)
        self.assertEqual(
            self.expected_application.vendor.id, actual_application.vendor.id
        )

        with self.assertRaises(ApplicationNotFoundException) as context:
            self.application_service.remove_one_by_name(
                application_name=self.expected_application.name,
                vendor_id=self.mock_vendor.id,
            )

            self.assertTrue("does not exist" not in str(context.exception))

    def test_applications_paginated(self) -> None:
        expected_application = Page(
            items=[map_application_entity_to_dto(self.expected_application)],
            limit=10,
            offset=0,
            total=1,
        )
        actual_applications = self.application_service.get_paginated(limit=10, offset=0)

        self.assertEqual(expected_application, actual_applications)
