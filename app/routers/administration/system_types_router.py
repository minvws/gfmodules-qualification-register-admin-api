from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_system_type_service
from app.schemas.system_type.mapper import map_system_type_entity_to_dto
from app.schemas.system_type.schema import SystemTypeCreateDTO, SystemTypeDTO
from app.db.services.system_type_service import SystemTypeService

router = APIRouter(prefix="/administration/system_types", tags=["System Types"])


@router.get("/")
def get_all_system_types(
    service: SystemTypeService = Depends(get_system_type_service),
) -> List[SystemTypeDTO]:
    system_types = service.get_all_system_types()
    return [
        map_system_type_entity_to_dto(system_types) for system_types in system_types
    ]


@router.get("/{system_type_id}")
def get_system_type_by_id(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDTO:
    system_type = service.get_one_by_id(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(system_type)


@router.post("/")
def create_new_system_type(
    data: SystemTypeCreateDTO,
    service: SystemTypeService = Depends(get_system_type_service),
) -> SystemTypeDTO:
    new_system_type = service.add_one_system_type(
        name=data.name,
        description=data.description,
    )
    return map_system_type_entity_to_dto(new_system_type)


@router.delete("/{system_type_id}")
def remove_system_type(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDTO:
    deleted_system_type = service.delete_one_system_type(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(deleted_system_type)
