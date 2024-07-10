from uuid import UUID

from app.db.entities.protocol import Protocol
from app.db.repository.protocol_repository import ProtocolRepository
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import ProtocolNotFoundException
from app.factory.protocol_factory import ProtocolFactory
from app.schemas.meta.schema import Page
from app.schemas.protocol.mapper import map_protocol_entity_to_dto
from app.schemas.protocol.schema import ProtocolDTO


class ProtocolService:
    @session_manager
    def get_one(
        self,
        protocol_id: UUID,
        protocol_repository: ProtocolRepository = get_repository(),
    ) -> Protocol:
        protocol = protocol_repository.get(id=protocol_id)
        if protocol is None:
            raise ProtocolNotFoundException()

        return protocol

    @session_manager
    def add_one(
        self,
        protocol_type: str,
        name: str,
        description: str,
        protocol_repository: ProtocolRepository = get_repository(),
    ) -> Protocol:
        new_protocol = ProtocolFactory.create_instance(
            name=name, description=description, protocol_type=protocol_type
        )
        protocol_repository.create(new_protocol)

        return new_protocol

    @session_manager
    def remove_one(
        self,
        protocol_id: UUID,
        protocol_repository: ProtocolRepository = get_repository(),
    ) -> Protocol:
        protocol = protocol_repository.get(id=protocol_id)
        if protocol is None:
            raise ProtocolNotFoundException()

        protocol_repository.delete(protocol)

        return protocol

    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        protocol_repository: ProtocolRepository = get_repository(),
    ) -> Page[ProtocolDTO]:
        protocols = protocol_repository.get_many(limit=limit, offset=offset)
        dto = [map_protocol_entity_to_dto(protocol) for protocol in protocols]
        total = protocol_repository.count()

        return Page(items=dto, limit=limit, offset=offset, total=total)
