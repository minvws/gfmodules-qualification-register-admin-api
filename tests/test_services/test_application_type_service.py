import unittest

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.services.application_service import ApplicationService
from app.db.services.application_type_service import ApplicationTypeService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import SystemTypeNotUsedByApplicationException


class TestApplicationTypeService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        repository_factory = RepositoryFactory()
        # setup service
        self.vendor_service = VendorService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.role_service = RolesService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.system_type_service = SystemTypeService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
            repository_factory=repository_factory,
        )
        self.application_service = ApplicationService(
            role_service=self.role_service,
            system_type_service=self.system_type_service,
            db_session_factory=db_session_factory,
            repository_factory=repository_factory,
        )
        self.application_type_service = ApplicationTypeService(
            db_session_factory=db_session_factory,
            application_service=self.application_service,
            repository_factory=repository_factory,
        )

        # setup data
        self.mock_vendor = self.vendor_service.add_one(
            kvk_number="example", trade_name="example", statutory_name="example"
        )
        self.mock_role = self.role_service.add_one(
            name="example", description="example"
        )
        self.mock_system_type = self.system_type_service.add_one(
            name="example", description="example"
        )
        self.mock_application = self.application_service.add_one(
            vendor=self.mock_vendor,
            application_name="example",
            version="example",
            roles=[self.mock_role],
            system_types=[self.mock_system_type],
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
        actual_application = self.application_service.get_one(
            self.mock_application.id
        )

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
