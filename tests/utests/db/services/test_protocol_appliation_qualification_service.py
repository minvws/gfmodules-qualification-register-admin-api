from datetime import date

import pytest

from app.db.entities import Application, Protocol, ProtocolVersion
from app.db.services import (
    ProtocolApplicationQualificationService,
    ProtocolVersionService,
)
from app.exceptions.app_exceptions import (
    AppVersionAlreadyArchivedException,
    AppVersionAlreadyQualifiedException,
)

from .utils import are_the_same_entity


def test_qualify_protocol_version_to_application_version(
    application: Application,
    protocol: Protocol,
    protocol_version: ProtocolVersion,
    protocol_version_service: ProtocolVersionService,
    protocol_application_qualification_service: ProtocolApplicationQualificationService,
) -> None:
    expected_protocol_version = protocol_application_qualification_service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version.id,
        application_version_id=application.versions[0].id,
        qualification_date=date.today(),
    )

    actual_protocol_version = protocol_version_service.get_one(
        protocol_id=protocol.id, version_id=protocol_version.id
    )

    assert expected_protocol_version.id == actual_protocol_version.id
    assert expected_protocol_version.version == actual_protocol_version.version
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            actual_protocol_version.qualified_application_versions,
            expected_protocol_version.qualified_application_versions,
        )
    )


def test_archive_one_protocol_application_qualification(
    application: Application,
    protocol: Protocol,
    protocol_version: ProtocolVersion,
    protocol_version_service: ProtocolVersionService,
    protocol_application_qualification_service: ProtocolApplicationQualificationService,
) -> None:
    application_version = application.versions[0]
    protocol_application_qualification_service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version.id,
        application_version_id=application_version.id,
        qualification_date=date.today(),
    )
    expected_protocol_version = protocol_application_qualification_service.archive_protocol_application_qualification(
        protocol_version_id=protocol_version.id,
        application_version_id=application_version.id,
    )

    actual_protocol_version = protocol_version_service.get_one(
        protocol_id=protocol.id, version_id=protocol_version.id
    )

    assert actual_protocol_version.id == expected_protocol_version.id
    assert (
        actual_protocol_version.qualified_application_versions[0].archived_date
        is not None
    )


def test_qualify_existing_application_should_raise_exception(
    application: Application,
    protocol_version: ProtocolVersion,
    protocol_application_qualification_service: ProtocolApplicationQualificationService,
) -> None:
    application_version = application.versions[0]
    protocol_application_qualification_service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version.id,
        application_version_id=application_version.id,
        qualification_date=date.today(),
    )

    with pytest.raises(
        AppVersionAlreadyQualifiedException,
        match="409: Application version is already qualified for the protocol",
    ):
        protocol_application_qualification_service.qualify_protocol_version_to_application_version(
            protocol_version_id=protocol_version.id,
            application_version_id=application_version.id,
            qualification_date=date.today(),
        )


def test_archive_an_already_archived_app_should_raise_exception(
    application: Application,
    protocol_version: ProtocolVersion,
    protocol_application_qualification_service: ProtocolApplicationQualificationService,
) -> None:
    application_version = application.versions[0]
    protocol_application_qualification_service.qualify_protocol_version_to_application_version(
        protocol_version_id=protocol_version.id,
        application_version_id=application_version.id,
        qualification_date=date.today(),
    )
    protocol_application_qualification_service.archive_protocol_application_qualification(
        protocol_version_id=protocol_version.id,
        application_version_id=application_version.id,
    )

    with pytest.raises(
        AppVersionAlreadyArchivedException,
        match="409: Application Version is already archived for protocol",
    ):
        protocol_application_qualification_service.archive_protocol_application_qualification(
            protocol_version_id=protocol_version.id,
            application_version_id=application_version.id,
        )
