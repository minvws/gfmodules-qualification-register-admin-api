import logging

from app.db.entities.protocol import Protocol
from app.schemas.enums.protocol_types import ProtocolTypes
from app.schemas.protocol.schema import ProtocolDTO


logger = logging.getLogger(__name__)


def map_protocol_type_to_enum(protocol_type: str) -> ProtocolTypes:
    try:
        new_protocol = ProtocolTypes(protocol_type)
        return new_protocol
    except ValueError as e:
        logger.error(e)
        raise ValueError(f"Unknown protocol type: {protocol_type}")


def map_protocol_entity_to_dto(entity: Protocol) -> ProtocolDTO:
    protocol_type = map_protocol_type_to_enum(entity.protocol_type)

    return ProtocolDTO(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        protocol_type=protocol_type,
    )
