import unittest

import inject

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import RoleNotFoundException
from app.db.services.roles_service import RolesService
from tests.utils.config_binder import config_binder


class TestRoleService(unittest.TestCase):

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
        self.role_service = RolesService(db_session_factory, repository_factory)

    def test_create_role(self) -> None:
        # act
        expected_role = self.role_service.add_one(
            name="example role", description="some description"
        )
        actual_role = self.role_service.get_one(role_id=expected_role.id)

        # assert
        self.assertEqual(expected_role.id, actual_role.id)
        self.assertEqual(expected_role.name, actual_role.name)
        self.assertEqual(expected_role.description, actual_role.description)

    def test_update_role_description(self) -> None:
        mock_role = self.role_service.add_one(
            name="example role", description="old description"
        )

        expected_role = self.role_service.update_role_description(
            role_id=mock_role.id, description="new description"
        )
        actual_role = self.role_service.get_one(role_id=mock_role.id)

        self.assertEqual(expected_role.description, actual_role.description)
        self.assertEqual(expected_role.id, actual_role.id)

    def test_delete_role(self) -> None:
        expected_role = self.role_service.add_one(
            name="example role", description="some description"
        )
        actual_role = self.role_service.remove_one(role_id=expected_role.id)

        self.assertEqual(expected_role.id, actual_role.id)

        with self.assertRaises(RoleNotFoundException) as context:
            self.role_service.get_one(expected_role.id)

            self.assertTrue("does not exist" in str(context.exception))

    def test_get_many_roles(self) -> None:
        mock_role = self.role_service.add_one(
            name="example role", description="some description"
        )
        expected_roles = [mock_role.to_dict()]
        actual_db_roles = self.role_service.get_many_by_names([mock_role.name])
        actual_roles = [role.to_dict() for role in actual_db_roles]

        self.assertSequenceEqual(expected_roles, actual_roles)

    def test_get_all_roles(self) -> None:
        mock_role = self.role_service.add_one(
            name="example role", description="some description"
        )
        expected_roles = [mock_role.to_dict()]
        actual_db_roles = self.role_service.get_many()
        actual_roles = [role.to_dict() for role in actual_db_roles]

        self.assertSequenceEqual(expected_roles, actual_roles)
