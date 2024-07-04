from typing import Sequence
from uuid import UUID

from app.db.entities.protocol_version import ProtocolVersion
from app.db.repository.protocol_repository import ProtocolRepository
from app.db.repository.protocol_version_repository import ProtocolVersionRepository
from app.db.repository_factory import RepositoryFactory
from app.db.services.protocol_service import ProtocolService
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    ProtocolNotFoundException,
    ProtocolVersionNotFoundException,
)
from app.factory.protocol_version_factory import ProtocolVersionFactory


class ProtocolVersionService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        protocol_service: ProtocolService,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.protocol_service = protocol_service
        self.repository_factory = repository_factory

    def get_one(self, version_id: UUID) -> ProtocolVersion:
        db_session = self.db_session_factory.create()
        protocol_version_repository = self.repository_factory.create(
            ProtocolVersionRepository, db_session
        )
        with db_session:
            protocol_version = protocol_version_repository.get(id=version_id)
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

        return protocol_version

    def get_many(self, protocol_id: UUID) -> Sequence[ProtocolVersion]:
        protocol = self.protocol_service.get_one(protocol_id)
        return protocol.versions

    def add_one(
        self, protocol_id: UUID, version: str, description: str
    ) -> ProtocolVersion:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        with db_session:
            protocol = protocol_repository.get(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

            new_protocol_version = ProtocolVersionFactory.create_instance(
                version=version, description=description
            )
            protocol.versions.append(new_protocol_version)
            protocol_repository.update(protocol)

        return new_protocol_version

    def remove_one(
        self, protocol_id: UUID, version_id: UUID
    ) -> Sequence[ProtocolVersion]:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        protocol_version_repository = self.repository_factory.create(
            ProtocolVersionRepository, db_session
        )
        with db_session:
            protocol = protocol_repository.get(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

            protocol_version = protocol_version_repository.get(id=version_id)
            if protocol_version is None:
                raise ProtocolVersionNotFoundException()

            protocol.versions.remove(protocol_version)
            protocol_repository.update(protocol)

        return protocol.versions
