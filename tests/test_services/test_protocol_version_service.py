import unittest

import inject

from app.db.db import Database
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.exceptions.app_exceptions import ProtocolVersionNotFoundException
from tests.utils.config_binder import config_binder


class TestProtocolVersionService(unittest.TestCase):
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
        self.protocol_version_service = ProtocolVersionService(
            protocol_service=self.protocol_service,
        )
        # arrange
        self.mock_protocol = self.protocol_service.add_one(
            protocol_type="Directive",
            name="example name",
            description="example description",
        )

    def test_add_one_protocol_version(self) -> None:
        expected_protocol_version = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="some version",
            description="some description",
        )

        actual_protocol_version = self.protocol_version_service.get_one(
            version_id=expected_protocol_version.id
        )

        self.assertEqual(expected_protocol_version.id, actual_protocol_version.id)
        self.assertEqual(
            expected_protocol_version.version, actual_protocol_version.version
        )

    def test_get_one_protocol_versions(self) -> None:
        expected_db_protocol_version = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="some version",
            description="some description",
        )
        expected_protocol_versions = [expected_db_protocol_version.to_dict()]

        actual_db_protocol_versions = self.protocol_service.get_one(
            protocol_id=self.mock_protocol.id
        ).versions
        actual_protocol_versions = [
            version.to_dict() for version in actual_db_protocol_versions
        ]

        self.assertCountEqual(expected_protocol_versions, actual_protocol_versions)

    def test_get_one_protocol_version(self) -> None:
        expected_protocol_version = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="some version",
            description="some description",
        )

        actual_protocol_version = self.protocol_version_service.get_one(
            expected_protocol_version.id
        )

        self.assertEqual(expected_protocol_version.id, actual_protocol_version.id)
        self.assertEqual(
            expected_protocol_version.version, actual_protocol_version.version
        )
        self.assertEqual(
            expected_protocol_version.description, actual_protocol_version.description
        )

    def test_fetching_a_deleted_version_should_raise_exception(self) -> None:
        mock_protocol_version = self.protocol_version_service.add_one(
            protocol_id=self.mock_protocol.id,
            version="some version",
            description="some description",
        )

        self.protocol_version_service.remove_one(
            protocol_id=self.mock_protocol.id, version_id=mock_protocol_version.id
        )

        with self.assertRaises(ProtocolVersionNotFoundException) as context:
            self.protocol_version_service.get_one(self.mock_protocol.id)

            self.assertTrue("not found" in str(context.exception))
