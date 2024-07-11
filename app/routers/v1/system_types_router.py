from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_system_type_service
from app.schemas.system_type.mapper import map_system_type_entity_to_dto
from app.schemas.system_type.schema import SystemTypeCreateDTO, SystemTypeDTO
from app.db.services.system_type_service import SystemTypeService

router = APIRouter(prefix="/system-types", tags=["System Types"])


@router.get("")
def get_system_types(
    service: SystemTypeService = Depends(get_system_type_service),
) -> list[SystemTypeDTO]:
    system_types = service.get_many()
    return [map_system_type_entity_to_dto(system_type) for system_type in system_types]


@router.get("/{system_type_id}")
def get_system_type_by_id(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDTO:
    system_type = service.get_one(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(system_type)


@router.post("")
def create_new_system_type(
    data: SystemTypeCreateDTO,
    service: SystemTypeService = Depends(get_system_type_service),
) -> SystemTypeDTO:
    new_system_type = service.add_one(
        name=data.name,
        description=data.description,
    )
    return map_system_type_entity_to_dto(new_system_type)


@router.delete("/{system_type_id}")
def remove_system_type(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDTO:
    deleted_system_type = service.delete_one(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(deleted_system_type)
