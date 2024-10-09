from typing import Sequence
from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities import ProtocolVersion
from app.db.repository import ProtocolRepository, ProtocolVersionRepository
from .protocol_service import ProtocolService
from app.exceptions.app_exceptions import (
    ProtocolNotFoundException,
    ProtocolVersionNotFoundException,
)
from app.factory import ProtocolVersionFactory


class ProtocolVersionService:
    def __init__(
        self,
        protocol_service: ProtocolService,
    ) -> None:
        self.protocol_service = protocol_service

    @session_manager
    def get_one(
        self,
        protocol_id: UUID,
        version_id: UUID,
        *,
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> ProtocolVersion:
        protocol_version = protocol_version_repository.get(
            id=version_id, protocol_id=protocol_id
        )
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        return protocol_version

    @session_manager
    def add_one(
        self,
        protocol_id: UUID,
        version: str,
        description: str | None,
        *,
        protocol_repository: ProtocolRepository = get_repository(),
    ) -> ProtocolVersion:
        protocol = protocol_repository.get(id=protocol_id)
        if protocol is None:
            raise ProtocolNotFoundException()

        new_protocol_version = ProtocolVersionFactory.create_instance(
            version=version, description=description
        )
        protocol.versions.append(new_protocol_version)

        return new_protocol_version

    @session_manager
    def remove_one(
        self,
        protocol_id: UUID,
        version_id: UUID,
        *,
        protocol_repository: ProtocolRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> Sequence[ProtocolVersion]:
        protocol = protocol_repository.get(id=protocol_id)
        if protocol is None:
            raise ProtocolNotFoundException()

        protocol_version = protocol_version_repository.get(id=version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        protocol.versions.remove(protocol_version)

        return protocol.versions
