import unittest
from datetime import date

from app.db.db import Database
from app.db.services.application_service import ApplicationService
from app.db.services.application_version_service import ApplicationVersionService
from app.db.services.protocol_application_qualification_service import (
    ProtocolApplicationQualificationService,
)
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    AppVersionAlreadyQualifiedException,
    AppVersionAlreadyArchivedException,
)


class TestProtocolApplianceQualificationService(unittest.TestCase):
    def setUp(self) -> None:
        # setup tables
        self.database = Database("sqlite:///:memory:")
        self.database.generate_tables()
        # setup factory
        db_session_factory = DbSessionFactory(engine=self.database.engine)
        # setup service
        self.vendor_service = VendorService(db_session_factory=db_session_factory)
        self.role_service = RolesService(db_session_factory=db_session_factory)
        self.system_type_service = SystemTypeService(
            db_session_factory=db_session_factory
        )
        self.application_service = ApplicationService(
            db_session_factory=db_session_factory,
            role_service=self.role_service,
            system_type_service=self.system_type_service,
        )
        self.application_version_service = ApplicationVersionService(
            application_service=self.application_service,
            db_session_factory=db_session_factory,
        )
        self.protocol_service = ProtocolService(db_session_factory=db_session_factory)
        self.protocol_version_service = ProtocolVersionService(
            db_session_factory=db_session_factory,
            protocol_service=self.protocol_service,
        )
        self.application_qualification_service = (
            ProtocolApplicationQualificationService(
                db_session_factory=db_session_factory
            )
        )
        # setup data
        self.mock_vendor = self.vendor_service.add_one_vendor(
            kvk_number="example", trade_name="example", statutory_name="example"
        )
        self.mock_role = self.role_service.create_role(
            name="example", description="example"
        )
        self.mock_system_type = self.system_type_service.add_one_system_type(
            name="example", description="example"
        )
        self.mock_application = self.application_service.add_one_application(
            vendor=self.mock_vendor,
            application_name="example",
            version="example",
            roles=[self.mock_role],
            system_types=[self.mock_system_type],
        )
        self.mock_protocol = self.protocol_service.create_one(
            name="example", description="example", protocol_type="Directive"
        )
        self.mock_protocol_version = (
            self.protocol_version_service.add_one_protocol_version(
                protocol_id=self.mock_protocol.id,
                version="example",
                description="example",
            )
        )

    def test_qualify_protocol_version_to_application_version(self) -> None:
        mock_application_version = self.mock_application.versions[0]
        expected_protocol_version = self.application_qualification_service.qualify_protocol_version_to_application_version(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
            qualification_date=date.today(),
        )

        actual_protocol_version = (
            self.protocol_version_service.get_one_protocol_version(
                version_id=self.mock_protocol_version.id
            )
        )

        self.assertEqual(expected_protocol_version.id, actual_protocol_version.id)
        self.assertEqual(
            expected_protocol_version.version, actual_protocol_version.version
        )
        self.assertEqual(
            [
                versions.to_dict()
                for versions in expected_protocol_version.qualified_application_versions
            ],
            [
                versions.to_dict()
                for versions in actual_protocol_version.qualified_application_versions
            ],
        )

    def test_archive_one_protocol_application_qualification(self) -> None:
        mock_application_version = self.mock_application.versions[0]
        self.application_qualification_service.qualify_protocol_version_to_application_version(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
            qualification_date=date.today(),
        )
        expected_protocol_version = self.application_qualification_service.archive_protocol_application_qualification(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
        )

        actual_protocol_version = (
            self.protocol_version_service.get_one_protocol_version(
                version_id=self.mock_protocol_version.id
            )
        )

        self.assertEqual(actual_protocol_version.id, expected_protocol_version.id)
        self.assertNotEqual(
            actual_protocol_version.qualified_application_versions[0].archived_date,
            None,
        )

    def test_qualify_existing_application_should_raise_exception(self) -> None:
        mock_application_version = self.mock_application.versions[0]
        self.application_qualification_service.qualify_protocol_version_to_application_version(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
            qualification_date=date.today(),
        )

        with self.assertRaises(AppVersionAlreadyQualifiedException) as context:
            self.application_qualification_service.qualify_protocol_version_to_application_version(
                protocol_version_id=self.mock_protocol_version.id,
                application_version_id=mock_application_version.id,
                qualification_date=date.today(),
            )

            self.assertTrue("Already qualified" in str(context.exception))

    def test_archive_an_already_archived_app_should_raise_exception(self) -> None:
        mock_application_version = self.mock_application.versions[0]
        self.application_qualification_service.qualify_protocol_version_to_application_version(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
            qualification_date=date.today(),
        )
        self.application_qualification_service.archive_protocol_application_qualification(
            protocol_version_id=self.mock_protocol_version.id,
            application_version_id=mock_application_version.id,
        )

        with self.assertRaises(AppVersionAlreadyArchivedException) as context:
            self.application_qualification_service.archive_protocol_application_qualification(
                protocol_version_id=self.mock_protocol_version.id,
                application_version_id=mock_application_version.id,
            )
            self.assertTrue("Already archived" in str(context.exception))
