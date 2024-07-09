import unittest

import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationRoleDeleteException
from app.db.services.application_roles_service import ApplicationRolesService
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from tests.utils.config_binder import config_binder


class TestApplicationRoleService(unittest.TestCase):
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
        # set up services
        self.vendor_service = VendorService()
        self.role_service = RolesService(db_session_factory, repository_factory)
        self.system_type_service = SystemTypeService()
        self.application_service = ApplicationService()
        self.application_role_service = ApplicationRolesService(
            application_service=self.application_service
        )
        self.mock_vendor = self.vendor_service.add_one(
            kvk_number="12456",
            trade_name="example vendor",
            statutory_name="example vendor bv",
        )
        self.mock_role = self.role_service.add_one(
            name="example role", description="some description"
        )
        self.mock_system_type = self.system_type_service.add_one(
            name="example system type", description="some description"
        )
        self.mock_application = self.application_service.add_one(
            vendor_id=self.mock_vendor.id,
            application_name="example application",
            version="v1.0.0",
            system_type_names=[self.mock_system_type.name],
            role_names=[self.mock_role.name],
        )

    def test_assign_role_to_application(self) -> None:
        expected_role = self.role_service.add_one(
            "new example role", description="some description"
        )
        updated_app = self.application_role_service.assign_role_to_application(
            application_id=self.mock_application.id, role_id=expected_role.id
        )
        expected_db_roles = updated_app.roles
        expected_roles = [role.to_dict() for role in expected_db_roles]

        actual_db_roles = self.application_role_service.get_application_roles(
            self.mock_application.id
        )
        actual_roles = [role.to_dict() for role in actual_db_roles]

        self.assertListEqual(expected_roles, actual_roles)

    def test_unassign_role_from_application(self) -> None:
        role_to_unassign = self.role_service.add_one(
            name="role_to_unassign", description="some description"
        )
        self.application_role_service.assign_role_to_application(
            application_id=self.mock_application.id, role_id=role_to_unassign.id
        )

        updated_application = (
            self.application_role_service.unassign_role_from_application(
                application_id=self.mock_application.id, role_id=role_to_unassign.id
            )
        )
        expected_db_roles = updated_application.roles
        expected_roles = [
            expected_role.to_dict() for expected_role in expected_db_roles
        ]

        actual_db_roles = self.application_role_service.get_application_roles(
            application_id=updated_application.id
        )
        actual_roles = [actual_role.to_dict() for actual_role in actual_db_roles]

        self.assertListEqual(expected_roles, actual_roles)

        with self.assertRaises(ApplicationRoleDeleteException) as context:
            self.application_role_service.unassign_role_from_application(
                application_id=self.mock_application.id, role_id=self.mock_role.id
            )

            self.assertTrue("does not exist" not in str(context.exception))
