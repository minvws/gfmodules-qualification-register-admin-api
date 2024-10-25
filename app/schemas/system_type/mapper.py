from app.db.entities.system_type import SystemType
from app.schemas.system_type.schema import SystemTypeDto


def map_system_type_entity_to_dto(system_type: SystemType) -> SystemTypeDto:
    return SystemTypeDto(
        id=system_type.id, name=system_type.name, description=system_type.description
    )
