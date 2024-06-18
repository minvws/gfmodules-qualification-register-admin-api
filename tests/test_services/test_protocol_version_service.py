import unittest

from app.db.db import Database
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ProtocolVersionNotFoundException


class TestProtocolVersionService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        # setup service
        self.protocol_service = ProtocolService(db_session_factory=db_session_factory)
        self.protocol_version_service = ProtocolVersionService(
            db_session_factory=db_session_factory,
            protocol_service=self.protocol_service,
        )

    def test_add_one_protocol_version(self) -> None:
        mock_protocol = self.protocol_service.create_one(
            protocol_type="Directive",
            name="example name",
            description="example description",
        )
        expected_protocol_version = (
            self.protocol_version_service.add_one_protocol_version(
                protocol_id=mock_protocol.id,
                version="some version",
                description="some description",
            )
        )

        actual_protocol_version = (
            self.protocol_version_service.get_one_protocol_version(
                version_id=expected_protocol_version.id
            )
        )

        self.assertEqual(expected_protocol_version.id, actual_protocol_version.id)
        self.assertEqual(
            expected_protocol_version.version, actual_protocol_version.version
        )

    def test_get_one_protocol_versions(self) -> None:
        mock_protocol = self.protocol_service.create_one(
            protocol_type="Directive",
            name="example name",
            description="example description",
        )
        expected_db_protocol_version = (
            self.protocol_version_service.add_one_protocol_version(
                protocol_id=mock_protocol.id,
                version="some version",
                description="some description",
            )
        )
        expected_protocol_versions = [expected_db_protocol_version.to_dict()]

        actual_db_protocol_versions = (
            self.protocol_version_service.get_one_protocol_versions(
                protocol_id=mock_protocol.id
            )
        )
        actual_protocol_versions = [
            version.to_dict() for version in actual_db_protocol_versions
        ]

        self.assertCountEqual(expected_protocol_versions, actual_protocol_versions)

    def test_get_one_protocol_version(self) -> None:
        mock_protocol = self.protocol_service.create_one(
            protocol_type="Directive",
            name="example name",
            description="example description",
        )
        expected_protocol_version = (
            self.protocol_version_service.add_one_protocol_version(
                protocol_id=mock_protocol.id,
                version="some version",
                description="some description",
            )
        )

        actual_protocol_version = (
            self.protocol_version_service.get_one_protocol_version(
                expected_protocol_version.id
            )
        )

        self.assertEqual(expected_protocol_version.id, actual_protocol_version.id)
        self.assertEqual(
            expected_protocol_version.version, actual_protocol_version.version
        )
        self.assertEqual(
            expected_protocol_version.description, actual_protocol_version.description
        )

    def test_fetching_a_deleted_version_should_raise_exception(self) -> None:
        mock_protocol = self.protocol_service.create_one(
            protocol_type="Directive",
            name="example name",
            description="example description",
        )
        mock_protocol_version = self.protocol_version_service.add_one_protocol_version(
            protocol_id=mock_protocol.id,
            version="some version",
            description="some description",
        )

        self.protocol_version_service.delete_one_protocol_version(
            protocol_id=mock_protocol.id, version_id=mock_protocol_version.id
        )

        with self.assertRaises(ProtocolVersionNotFoundException) as context:
            self.protocol_version_service.get_one_protocol_version(mock_protocol.id)

            self.assertTrue("not found" in str(context.exception))
