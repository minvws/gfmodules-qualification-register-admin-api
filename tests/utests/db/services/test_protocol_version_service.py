import pytest

from app.db.entities import Protocol, ProtocolVersion
from app.db.services import ProtocolService, ProtocolVersionService
from app.exceptions.app_exceptions import ProtocolVersionNotFoundException

from .utils import are_the_same_entity


def test_add_one_protocol_version(
    protocol: Protocol,
    protocol_version_service: ProtocolVersionService,
) -> None:
    expected_protocol_version = protocol_version_service.add_one(
        protocol_id=protocol.id,
        version="some version",
        description="some description",
    )

    actual_protocol_version = protocol_version_service.get_one(
        protocol_id=protocol.id, version_id=expected_protocol_version.id
    )
    are_the_same_entity(actual_protocol_version, expected_protocol_version)


def test_get_one_protocol_versions(
    protocol: Protocol,
    protocol_version: ProtocolVersion,
    protocol_service: ProtocolService,
) -> None:
    actual_db_protocol_version = protocol_service.get_one(
        protocol_id=protocol.id
    ).versions[0]

    are_the_same_entity(actual_db_protocol_version, protocol_version)


def test_fetching_a_deleted_version_should_raise_exception(
    protocol: Protocol,
    protocol_version: ProtocolVersion,
    protocol_version_service: ProtocolVersionService,
) -> None:
    assert protocol_version_service.get_one(
        protocol_id=protocol.id, version_id=protocol_version.id
    )

    protocol_version_service.remove_one(
        protocol_id=protocol.id, version_id=protocol_version.id
    )

    with pytest.raises(
        ProtocolVersionNotFoundException, match="404: Protocol version not found"
    ):
        protocol_version_service.get_one(
            protocol_id=protocol.id, version_id=protocol_version.id
        )
