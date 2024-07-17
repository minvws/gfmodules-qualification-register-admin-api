import logging

from app.db.entities.protocol import Protocol
from app.db.entities.protocol_version import ProtocolVersion
from app.schemas.enums.protocol_types import ProtocolTypes
from app.schemas.protocol.schema import ProtocolDto, ProtocolVersionDto

logger = logging.getLogger(__name__)


def map_protocol_type_to_enum(protocol_type: str) -> ProtocolTypes:
    try:
        new_protocol = ProtocolTypes(protocol_type)
        return new_protocol
    except ValueError as e:
        logger.error(e)
        raise ValueError(f"Unknown protocol type: {protocol_type}")


def map_protocol_version_entity_to_dto(entity: ProtocolVersion) -> ProtocolVersionDto:
    return ProtocolVersionDto(
        id=entity.id, version=entity.version, description=entity.description
    )


def map_protocol_entity_to_dto(entity: Protocol) -> ProtocolDto:
    protocol_type = map_protocol_type_to_enum(entity.protocol_type)

    versions = [
        map_protocol_version_entity_to_dto(version) for version in entity.versions
    ]

    return ProtocolDto(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        protocol_type=protocol_type,
        versions=versions,
    )
