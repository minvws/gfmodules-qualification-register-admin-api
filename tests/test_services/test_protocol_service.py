import unittest

import inject

from app.db.db import Database
from app.db.services.protocol_service import ProtocolService
from app.exceptions.app_exceptions import ProtocolNotFoundException
from tests.utils.config_binder import config_binder


class TestProtocolService(unittest.TestCase):
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
        self.protocol_service = ProtocolService()

    def test_add_one_protocol(self) -> None:
        expected_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )
        actual_protocol = self.protocol_service.get_one(expected_protocol.id)

        self.assertEqual(expected_protocol.id, actual_protocol.id)
        self.assertEqual(expected_protocol.protocol_type, actual_protocol.protocol_type)
        self.assertEqual(expected_protocol.description, actual_protocol.description)
        self.assertEqual(expected_protocol.name, actual_protocol.name)

    def test_delete_protocol(self) -> None:
        expected_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )
        actual_protocol = self.protocol_service.remove_one(expected_protocol.id)

        self.assertEqual(expected_protocol.id, actual_protocol.id)
        self.assertEqual(expected_protocol.protocol_type, actual_protocol.protocol_type)
        self.assertEqual(expected_protocol.description, actual_protocol.description)
        self.assertEqual(expected_protocol.name, actual_protocol.name)

        with self.assertRaises(ProtocolNotFoundException) as context:
            self.protocol_service.get_one(expected_protocol.id)

            self.assertTrue("does not exist" not in str(context.exception))

    def test_get_many_protocols(self) -> None:
        expected_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )
        expected_protocols = [expected_protocol.to_dict()]

        actual_db_protocols = self.protocol_service.get_all()
        actual_protocols = [protocol.to_dict() for protocol in actual_db_protocols]

        self.assertCountEqual(expected_protocols, actual_protocols)
