from app.db.entities.protocol import Protocol


class ProtocolFactory:
    @staticmethod
    def create_instance(protocol_type: str, name: str, description: str) -> Protocol:
        new_protocol = Protocol(
            name=name, protocol_type=protocol_type, description=description
        )
        return new_protocol
