from app.db.entities.protocol_version import ProtocolVersion


class ProtocolVersionFactory:
    @staticmethod
    def create_instance(version: str, description: str | None) -> ProtocolVersion:
        return ProtocolVersion(version=version, description=description)
