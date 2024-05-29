from app.db.entities.system_type import SystemType


class SystemTypeFactory:

    @staticmethod
    def create_instance(name: str, description: str) -> SystemType:
        return SystemType(name=name, description=description)
