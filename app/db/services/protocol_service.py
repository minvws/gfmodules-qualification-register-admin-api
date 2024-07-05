from typing import Sequence
from uuid import UUID

from app.db.entities.protocol import Protocol
from app.db.repository.protocol_repository import ProtocolRepository
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import ProtocolNotFoundException
from app.factory.protocol_factory import ProtocolFactory


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
    def get_all(
        self, protocol_repository: ProtocolRepository = get_repository()
    ) -> Sequence[Protocol]:
        protocols = protocol_repository.get_all()
        return protocols

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
