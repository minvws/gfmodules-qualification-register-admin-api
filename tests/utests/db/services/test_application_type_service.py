import unittest

import inject

from app.db.db import Database
from app.db.entities.application import Application
from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.db.services.application_service import ApplicationService
from app.db.services.application_type_service import ApplicationTypeService
from app.db.services.roles_service import RoleService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.exceptions.app_exceptions import SystemTypeNotUsedByApplicationException
from tests.utils.config_binder import config_binder


class TestApplicationTypeService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        inject.configure(
            lambda binder: config_binder(binder, self.database),
            clear=True,
        )
        # setup service
        self.vendor_service = VendorService()
        self.role_service = RoleService()
        self.system_type_service = SystemTypeService()
        self.application_service = ApplicationService()
        self.application_type_service = ApplicationTypeService()

        # setup data
        self.mock_vendor: Vendor = self.vendor_service.add_one(
            kvk_number="example", trade_name="example", statutory_name="example"
        )
        self.mock_role: Role = self.role_service.add_one(
            name="example", description="example"
        )
        self.mock_system_type: SystemType = self.system_type_service.add_one(
            name="example", description="example"
        )
        self.mock_application: Application = self.application_service.add_one(
            vendor_id=self.mock_vendor.id,
            application_name="example",
            version="example",
            role_names=[self.mock_role.name],
            system_type_names=[self.mock_system_type.name],
        )

    def test_get_all_application_types(self) -> None:
        test_system_type = self.system_type_service.add_one(
            name="example 2", description="some description"
        )
        expected_application = (
            self.application_type_service.assign_system_type_to_application(
                application_id=self.mock_application.id,
                system_type_id=test_system_type.id,
            )
        )
        actual_application = self.application_service.get_one(self.mock_application.id)

        self.assertEqual(expected_application.id, actual_application.id)
        self.assertEqual(
            len(expected_application.system_types), len(actual_application.system_types)
        )
        self.assertEqual(
            [
                system_type.to_dict()
                for system_type in expected_application.system_types
            ],
            [system_type.to_dict() for system_type in actual_application.system_types],
        )

    def test_assign_system_type_to_application(self) -> None:
        test_system_type = self.system_type_service.add_one(
            name="example 2", description="some description"
        )
        expected_application = (
            self.application_type_service.assign_system_type_to_application(
                application_id=self.mock_application.id,
                system_type_id=test_system_type.id,
            )
        )
        actual_application = self.application_service.get_one(
            application_id=self.mock_application.id
        )

        self.assertEqual(actual_application.id, expected_application.id)
        self.assertEqual(
            [
                system_type.to_dict()
                for system_type in expected_application.system_types
            ],
            [system_type.to_dict() for system_type in actual_application.system_types],
        )

    def test_unassign_system_type_to_application(self) -> None:
        test_system_type = self.system_type_service.add_one(
            name="example 2", description="some description"
        )
        self.application_type_service.assign_system_type_to_application(
            application_id=self.mock_application.id, system_type_id=test_system_type.id
        )
        self.application_type_service.unassign_system_type_to_application(
            application_id=self.mock_application.id, system_type_id=test_system_type.id
        )

        with self.assertRaises(SystemTypeNotUsedByApplicationException) as context:
            self.application_type_service.unassign_system_type_to_application(
                application_id=self.mock_application.id,
                system_type_id=test_system_type.id,
            )

            self.assertTrue("does not exist" not in str(context.exception))
