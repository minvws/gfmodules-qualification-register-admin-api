from typing import Sequence
from uuid import UUID

from app.db.entities.protocol import Protocol
from app.db.repository.protocol_repository import ProtocolRepository
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import ProtocolNotFoundException
from app.factory.protocol_factory import ProtocolFactory


class ProtocolService:
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def get_one_by_id(self, protocol_id: UUID) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository: ProtocolRepository = db_session.get_repository(Protocol)
        session = db_session.session
        with session:
            protocol = protocol_repository.find_one(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

        return protocol

    def get_all(self) -> Sequence[Protocol]:
        db_session = self.db_session_factory.create()
        protocol_repository: ProtocolRepository = db_session.get_repository(Protocol)
        session = db_session.session
        with session:
            protocols = protocol_repository.find_many()

        return protocols

    def create_one(self, protocol_type: str, name: str, description: str) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository: ProtocolRepository = db_session.get_repository(Protocol)
        session = db_session.session
        with session:
            new_protocol = ProtocolFactory.create_instance(
                name=name, description=description, protocol_type=protocol_type
            )
            protocol_repository.create(new_protocol)

        return new_protocol

    def delete_one_by_id(self, protocol_id: UUID) -> Protocol:
        db_session = self.db_session_factory.create()
        protocol_repository: ProtocolRepository = db_session.get_repository(Protocol)
        session = db_session.session
        with session:
            protocol = protocol_repository.find_one(id=protocol_id)
            if protocol is None:
                raise ProtocolNotFoundException()

            protocol_repository.delete(protocol)

        return protocol
