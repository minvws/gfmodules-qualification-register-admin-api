from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.container import get_roles_service
from app.schemas.meta.schema import Page
from app.schemas.pagination_query_params.schema import PaginationQueryParams
from app.schemas.roles.mapper import map_role_model_to_dto
from app.schemas.roles.schema import RoleCreateDto, RoleUpdateDto, RoleDto
from app.db.services.roles_service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("")
def get_roles(
    query: Annotated[PaginationQueryParams, Depends()],
    service: RoleService = Depends(get_roles_service),
) -> Page[RoleDto]:
    return service.get_paginated(limit=query.limit, offset=query.offset)


@router.get("/{role_id}")
def get_one_role(
    role_id: UUID, service: RoleService = Depends(get_roles_service)
) -> RoleDto:
    role = service.get_one(role_id)
    return map_role_model_to_dto(role)


@router.post("", response_model=RoleDto, status_code=status.HTTP_201_CREATED)
def create_role(
    data: RoleCreateDto, service: RoleService = Depends(get_roles_service)
) -> RoleDto:
    new_role = service.add_one(**data.model_dump())
    return map_role_model_to_dto(new_role)


@router.put("/{role_id}", response_model=RoleDto, status_code=status.HTTP_201_CREATED)
def update_role_description(
    role_id: UUID,
    data: RoleUpdateDto,
    service: RoleService = Depends(get_roles_service),
) -> RoleDto:
    role = service.update_role_description(
        role_id=role_id, description=data.description
    )
    return map_role_model_to_dto(role)


@router.delete("/{role_id}")
def delete_role(
    role_id: UUID, service: RoleService = Depends(get_roles_service)
) -> RoleDto:
    deleted_role = service.remove_one(role_id)
    return map_role_model_to_dto(deleted_role)
