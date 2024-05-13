import unittest

from app.db.db import Database
from app.db.entities.models import Role
from app.exceptions.app_exceptions import RoleNotFoundException
from app.services.roles_service import RolesService


class TestAddingOneRole(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()

        # setup service
        self.role_service = RolesService(database=self.database)

    def test_retrieving_one_role(self) -> None:
        new_role = Role(name="test", description="test")
        role_repistory = self.role_service.get_roles_repository()

        role_repistory.create(new_role)
        actual_role = self.role_service.get_one_role(role_id=new_role.id)

        self.assertEqual(new_role.to_dict(), actual_role.to_dict())

    def test_updating_one_role(self) -> None:
        modified_description = "new description"
        new_role = Role(name="test", description="old description")
        role_repistory = self.role_service.get_roles_repository()
        role_repistory.create(new_role)

        self.role_service.update_role_description(new_role.id, modified_description)
        actual_role = self.role_service.get_one_role(role_id=new_role.id)

        self.assertEqual(actual_role.description, modified_description)

    def test_deleting_role(self) -> None:
        new_role = Role(name="test", description="old description")
        role_repistory = self.role_service.get_roles_repository()
        role_repistory.create(new_role)

        self.role_service.delete_role(new_role.id)
        with self.assertRaises(RoleNotFoundException) as context:
            self.role_service.delete_role(new_role.id)

            self.assertTrue("Role not found" in str(context.exception))
