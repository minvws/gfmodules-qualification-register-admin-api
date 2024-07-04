from typing import Sequence
from uuid import UUID

from app.db.entities.protocol import Protocol
from app.db.repository.protocol_repository import ProtocolRepository
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ProtocolNotFoundException
from app.factory.protocol_factory import ProtocolFactory


class ProtocolService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.repository_factory = repository_factory

    def get_one(self, protocol_id: UUID) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        with db_session:
            protocol = protocol_repository.get(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

        return protocol

    def get_all(self) -> Sequence[Protocol]:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        with db_session:
            protocols = protocol_repository.get_all()

        return protocols

    def add_one(self, protocol_type: str, name: str, description: str) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        with db_session:
            new_protocol = ProtocolFactory.create_instance(
                name=name, description=description, protocol_type=protocol_type
            )
            protocol_repository.create(new_protocol)

        return new_protocol

    def remove_one(self, protocol_id: UUID) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository = self.repository_factory.create(
            ProtocolRepository, db_session
        )
        with db_session:
            protocol = protocol_repository.get(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

            protocol_repository.delete(protocol)

        return protocol
