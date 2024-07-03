import unittest

from app.db.db import Database
from app.db.repository_factory import RepositoryFactory
from app.db.services.protocol_service import ProtocolService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ProtocolNotFoundException


class TestProtocolService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        repository_factory = RepositoryFactory()
        # setup service
        self.protocol_service = ProtocolService(
            db_session_factory=db_session_factory, repository_factory=repository_factory
        )

    def test_add_one_protocol(self) -> None:
        mock_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )

        actual_protocol = self.protocol_service.get_one(mock_protocol.id)
        self.assertEqual(mock_protocol.id, actual_protocol.id)
        self.assertEqual(mock_protocol.protocol_type, actual_protocol.protocol_type)
        self.assertEqual(mock_protocol.description, actual_protocol.description)
        self.assertEqual(mock_protocol.name, actual_protocol.name)

    def test_delete_protocol(self) -> None:
        mock_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )
        self.protocol_service.remove_one(mock_protocol.id)

        with self.assertRaises(ProtocolNotFoundException) as context:
            self.protocol_service.get_one(mock_protocol.id)

            self.assertTrue("does not exist" not in str(context.exception))

    def test_get_many_protocols(self) -> None:
        mock_protocol = self.protocol_service.add_one(
            name="test protocol",
            description="some description",
            protocol_type="Directive",
        )
        mock_protocols = [mock_protocol.to_dict()]

        actual_db_protocols = self.protocol_service.get_all()
        actual_protocols = [protocol.to_dict() for protocol in actual_db_protocols]

        self.assertCountEqual(mock_protocols, actual_protocols)
