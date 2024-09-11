from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.container import get_system_type_service
from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams
from app.schemas.system_type.mapper import map_system_type_entity_to_dto
from app.schemas.system_type.schema import SystemTypeCreateDto, SystemTypeDto
from app.db.services.system_type_service import SystemTypeService

router = APIRouter(prefix="/system-types", tags=["System Types"])


@router.get("")
def get_system_types(
    query: Annotated[PaginationQueryParams, Depends()],
    service: SystemTypeService = Depends(get_system_type_service),
) -> Page[SystemTypeDto]:
    return service.get_paginated(limit=query.limit, offset=query.offset)


@router.get("/{system_type_id}")
def get_system_type_by_id(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDto:
    system_type = service.get_one(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(system_type)


@router.post("", response_model=SystemTypeDto, status_code=status.HTTP_201_CREATED)
def create_new_system_type(
    data: SystemTypeCreateDto,
    service: SystemTypeService = Depends(get_system_type_service),
) -> SystemTypeDto:
    new_system_type = service.add_one(
        name=data.name,
        description=data.description,
    )
    return map_system_type_entity_to_dto(new_system_type)


@router.delete("/{system_type_id}")
def remove_system_type(
    system_type_id: UUID, service: SystemTypeService = Depends(get_system_type_service)
) -> SystemTypeDto:
    deleted_system_type = service.delete_one(system_type_id=system_type_id)
    return map_system_type_entity_to_dto(deleted_system_type)
