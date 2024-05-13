import unittest

from app.db.db import Database
from app.exceptions.app_exceptions import RoleNotInApplicationException
from app.factory.application_factory import ApplicationFactory
from app.services.application_roles_service import ApplicationRolesService
from app.services.application_service import ApplicationService
from app.services.roles_service import RolesService
from app.services.vendor_application_service import VendorApplicationService
from app.services.vendors_service import VendorService


class TestAssignRoleToApplication(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(self.database)
        self.role_service = RolesService(database=self.database)
        self.application_service = ApplicationService(database=self.database)
        self.application_roles_service = ApplicationRolesService(
            application_service=self.application_service,
            roles_service=self.role_service,
        )
        self.vendor_application_service = VendorApplicationService(
            vendor_service=self.vendor_service,
            application_service=self.application_service,
        )

        # setup factory
        self.application_factory = ApplicationFactory()

    def test_assigning_one_role_to_application(self) -> None:
        new_vendor = self.vendor_service.add_one_vendor(
            "123456", "example vendor", "example-vendor"
        )
        self.vendor_application_service.register_one_application(
            new_vendor.kvk_number, "example app", "123456"
        )
        new_application = self.application_service.get_one_vendor_application(
            new_vendor.id, "example app"
        )
        expected_role = self.role_service.create_role(
            "example role", "example description"
        )
        if new_application is None:
            self.fail("Error creating new application")

        actual_app = self.application_roles_service.assign_role_to_application(
            new_application.id, expected_role.id
        )
        actual_role = actual_app.roles[0]

        self.assertEqual(expected_role.id, actual_role.role_id)


class TestUnassignRoleToApplication(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.vendor_service = VendorService(self.database)
        self.role_service = RolesService(database=self.database)
        self.application_service = ApplicationService(database=self.database)
        self.application_roles_service = ApplicationRolesService(
            application_service=self.application_service,
            roles_service=self.role_service,
        )
        self.vendor_application_service = VendorApplicationService(
            vendor_service=self.vendor_service,
            application_service=self.application_service,
        )

        # setup factory
        self.application_factory = ApplicationFactory()

    def test_unassigning_one_role_to_application(self) -> None:
        new_vendor = self.vendor_service.add_one_vendor(
            "123456", "example vendor", "example-vendor"
        )
        self.vendor_application_service.register_one_application(
            new_vendor.kvk_number, "example app", "123456"
        )
        new_application = self.application_service.get_one_vendor_application(
            new_vendor.id, "example app"
        )
        if new_application is None:
            self.fail("Error occurred while creating new application")

        new_role = self.role_service.create_role("example role", "example description")
        self.application_roles_service.assign_role_to_application(
            new_application.id, new_role.id
        )

        self.application_roles_service.remove_role_from_application(
            new_application.id, new_role.id
        )

        with self.assertRaises(RoleNotInApplicationException) as context:
            self.application_roles_service.remove_role_from_application(
                new_application.id, new_role.id
            )

            self.assertTrue("does not exist" in str(context.exception))
