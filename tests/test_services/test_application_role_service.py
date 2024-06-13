import unittest

from app.db.db import Database
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ApplicationRoleDeleteException
from app.db.services.application_roles_service import ApplicationRolesService
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendor_application_service import VendorApplicationService
from app.db.services.vendors_service import VendorService


class TestApplicationRoleService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)

        # set up services
        self.vendor_service = VendorService(db_session_factory)
        self.role_service = RolesService(db_session_factory)
        self.system_type_service = SystemTypeService(db_session_factory)
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
        )
        self.vendor_application_service = VendorApplicationService(
            application_service=self.application_service,
            vendor_service=self.vendor_service,
            system_type_service=self.system_type_service,
            roles_service=self.role_service,
        )
        self.application_role_service = ApplicationRolesService(
            roles_service=self.role_service,
            application_service=self.application_service,
            db_session_factory=db_session_factory,
        )

    def test_assign_role_to_application(self) -> None:
        mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="12456",
            trade_name="example vendor",
            statutory_name="example vendor bv",
        )
        mock_role = self.role_service.create_role(
            name="example role", description="some description"
        )
        mock_system_type = self.system_type_service.add_one_system_type(
            name="example system type", description="some description"
        )
        mock_application = self.vendor_application_service.register_one_app(
            vendor_id=mock_vendor.id,
            application_name="example application",
            application_version="v1.0.0",
            system_type_names=[mock_system_type.name],
            role_names=[mock_role.name],
        )

        expected_role = self.role_service.create_role(
            "new example role", description="some description"
        )
        updated_app = self.application_role_service.assign_role_to_application(
            application_id=mock_application.id, role_id=expected_role.id
        )
        expected_db_roles = updated_app.roles
        expected_roles = [role.to_dict() for role in expected_db_roles]

        actual_db_roles = self.application_role_service.get_application_roles(
            mock_application.id
        )
        actual_roles = [role.to_dict() for role in actual_db_roles]

        self.assertListEqual(expected_roles, actual_roles)

    def test_unassign_role_from_application(self) -> None:
        mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="12456",
            trade_name="example vendor",
            statutory_name="example vendor bv",
        )
        mock_role = self.role_service.create_role(
            name="example role", description="some description"
        )
        mock_system_type = self.system_type_service.add_one_system_type(
            name="example system type", description="some description"
        )
        mock_application = self.vendor_application_service.register_one_app(
            vendor_id=mock_vendor.id,
            application_name="example application",
            application_version="v1.0.0",
            system_type_names=[mock_system_type.name],
            role_names=[mock_role.name],
        )

        role_to_unassign = self.role_service.create_role(
            name="role_to_unassign", description="some description"
        )
        self.application_role_service.assign_role_to_application(
            application_id=mock_application.id, role_id=role_to_unassign.id
        )

        updated_application = (
            self.application_role_service.unassign_role_from_application(
                application_id=mock_application.id, role_id=role_to_unassign.id
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
                application_id=mock_application.id, role_id=mock_role.id
            )

            self.assertTrue("does not exist" not in str(context.exception))
