import unittest

import inject

from app.db.db import Database
from app.exceptions.app_exceptions import SystemTypeNotFoundException
from app.db.services.system_type_service import SystemTypeService
from tests.utils.config_binder import config_binder


class TestSystemTypeService(unittest.TestCase):
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
        self.system_type_service = SystemTypeService()

    def test_add_one_single_type(self) -> None:
        expected_system_type = self.system_type_service.add_one(
            name="example", description="some description"
        )
        actual_system_type = self.system_type_service.get_one(expected_system_type.id)

        self.assertEqual(expected_system_type.id, actual_system_type.id)
        self.assertEqual(expected_system_type.name, actual_system_type.name)
        self.assertEqual(
            expected_system_type.description, actual_system_type.description
        )

    def test_delete_one_system_type(self) -> None:
        expected_system_type = self.system_type_service.add_one(
            name="example", description="some description"
        )
        actual_system_type = self.system_type_service.delete_one(
            expected_system_type.id
        )

        self.assertEqual(expected_system_type.id, actual_system_type.id)
        self.assertEqual(expected_system_type.name, actual_system_type.name)
        self.assertEqual(
            expected_system_type.description, actual_system_type.description
        )

        with self.assertRaises(SystemTypeNotFoundException) as context:
            self.system_type_service.get_one(expected_system_type.id)

            self.assertTrue("does not exist" in str(context.exception))

    def test_get_many_system_types(self) -> None:
        mock_system_type = self.system_type_service.add_one(
            name="example", description="some description"
        )
        expected_system_types = [mock_system_type.to_dict()]

        system_types = self.system_type_service.get_many_by_names(
            [mock_system_type.name]
        )
        actual_system_types = [system_type.to_dict() for system_type in system_types]

        self.assertListEqual(expected_system_types, actual_system_types)

    def test_get_all_system_types(self) -> None:
        mock_system_type = self.system_type_service.add_one(
            name="example", description="some description"
        )
        expected_system_types = [mock_system_type.to_dict()]

        actual_db_system_types = self.system_type_service.get_all()
        actual_system_types = [
            system_type.to_dict() for system_type in actual_db_system_types
        ]

        self.assertListEqual(expected_system_types, actual_system_types)
