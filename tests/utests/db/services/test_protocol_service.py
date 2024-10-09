from uuid import UUID

import pytest

from app.db.entities import Protocol
from app.db.services import ProtocolService
from app.exceptions.app_exceptions import ProtocolNotFoundException
from app.schemas.meta.schema import Page
from app.schemas.protocol.mapper import map_protocol_entity_to_dto

from .utils import are_the_same_entity


def test_add_one_protocol(protocol_service: ProtocolService) -> None:
    expected_protocol = protocol_service.add_one(
        name="test protocol",
        description="some description",
        protocol_type="Directive",
    )
    actual_protocol = protocol_service.get_one(expected_protocol.id)
    assert are_the_same_entity(actual_protocol, expected_protocol)


def test_delete_protocol(protocol: Protocol, protocol_service: ProtocolService) -> None:
    assert are_the_same_entity(protocol_service.remove_one(protocol.id), protocol)


def test_delete_non_existing_protocol(protocol_service: ProtocolService) -> None:
    with pytest.raises(ProtocolNotFoundException, match="404: Protocol not found"):
        protocol_service.get_one(UUID("7b0aa8ef-9235-41c6-9838-3d2f5ba84282"))


def test_get_protocols_paginated(
    protocol: Protocol, protocol_service: ProtocolService
) -> None:
    assert protocol_service.get_paginated(limit=10, offset=0) == Page(
        items=[map_protocol_entity_to_dto(protocol)],
        limit=10,
        offset=0,
        total=1,
    )
