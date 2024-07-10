from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_protocol_service, get_protocol_version_service
from app.db.services.protocol_service import ProtocolService
from app.db.services.protocol_version_service import ProtocolVersionService
from app.schemas.meta.schema import Page
from app.schemas.protocol.mapper import (
    map_protocol_entity_to_dto,
    map_protocol_version_entity_to_dto,
)
from app.schemas.protocol.schema import (
    ProtocolDTO,
    ProtocolCreateDTO,
    ProtocolVersionCreateDTO,
    ProtocolVersionDTO,
)
from app.schemas.pagination_query_params.schema import PaginationQueryParams

router = APIRouter(prefix="/protocols", tags=["Protocols"])


@router.get("")
def get_protocols(
    query: Annotated[PaginationQueryParams, Depends()],
    service: ProtocolService = Depends(get_protocol_service),
) -> Page[ProtocolDTO]:
    return service.get_paginated(limit=query.limit, offset=query.offset)


@router.post("", response_model=ProtocolDTO)
def define_a_protocol(
    data: ProtocolCreateDTO, service: ProtocolService = Depends(get_protocol_service)
) -> ProtocolDTO:
    protocol = service.add_one(**data.model_dump())
    return map_protocol_entity_to_dto(protocol)


@router.get("/{protocol_id}", response_model=ProtocolDTO)
def get_one_protocol_by_id(
    protocol_id: UUID,
    service: ProtocolService = Depends(get_protocol_service),
) -> ProtocolDTO:
    protocol = service.get_one(protocol_id)
    return map_protocol_entity_to_dto(protocol)


@router.delete("/{protocol_id}", response_model=ProtocolDTO)
def delete_protocol(
    protocol_id: UUID, service: ProtocolService = Depends(get_protocol_service)
) -> ProtocolDTO:
    protocol = service.remove_one(protocol_id)
    return map_protocol_entity_to_dto(protocol)


@router.post("/{protocol_id}/versions")
def add_protocol_version(
    protocol_id: UUID,
    data: ProtocolVersionCreateDTO,
    service: ProtocolVersionService = Depends(get_protocol_version_service),
) -> ProtocolVersionDTO:
    version = service.add_one(
        protocol_id=protocol_id, version=data.version, description=data.description
    )
    return map_protocol_version_entity_to_dto(version)


@router.delete("/{protocol_id}/versions/{version_id}")
def delete_protocol_version(
    protocol_id: UUID,
    version_id: UUID,
    service: ProtocolVersionService = Depends(get_protocol_version_service),
) -> List[ProtocolVersionDTO]:
    versions = service.remove_one(protocol_id=protocol_id, version_id=version_id)
    return [map_protocol_version_entity_to_dto(version) for version in versions]


@router.get("/versions/{version_id}")
def get_protocol_version(
    version_id: UUID,
    service: ProtocolVersionService = Depends(get_protocol_version_service),
) -> ProtocolVersionDTO:
    protocol_version = service.get_one(version_id)
    return map_protocol_version_entity_to_dto(protocol_version)
