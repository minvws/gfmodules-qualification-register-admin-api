from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_protocol_service
from app.db.services.protocol_service import ProtocolService
from app.schemas.protocol.mapper import map_protocol_entity_to_dto
from app.schemas.protocol.schema import ProtocolDTO, ProtocolCreateDTO

router = APIRouter(prefix="/administration/protocols", tags=["Protocols"])


@router.get("", response_model=List[ProtocolDTO])
def get_all_protocols(
    service: ProtocolService = Depends(get_protocol_service),
) -> List[ProtocolDTO]:
    protocols = service.get_all()
    return [map_protocol_entity_to_dto(protocol) for protocol in protocols]


@router.post("/", response_model=ProtocolDTO)
def define_a_protocol(
    data: ProtocolCreateDTO, service: ProtocolService = Depends(get_protocol_service)
) -> ProtocolDTO:
    protocol = service.create_one(**data.model_dump())
    return map_protocol_entity_to_dto(protocol)


@router.get("/{protocol_id}", response_model=ProtocolDTO)
def get_one_protocol_by_id(
    protocol_id: UUID,
    service: ProtocolService = Depends(get_protocol_service),
) -> ProtocolDTO:
    protocol = service.get_one_by_id(protocol_id)
    return map_protocol_entity_to_dto(protocol)


@router.delete("/{protocol_id}", response_model=ProtocolDTO)
def delete_protocol(
    protocol_id: UUID, service: ProtocolService = Depends(get_protocol_service)
) -> ProtocolDTO:
    protocol = service.delete_one_by_id(protocol_id)
    return map_protocol_entity_to_dto(protocol)
