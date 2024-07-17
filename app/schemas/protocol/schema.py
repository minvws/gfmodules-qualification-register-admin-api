from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums.protocol_types import ProtocolTypes


class ProtocolVersionBase(BaseModel):
    version: str
    description: str | None


class ProtocolVersionCreateDto(ProtocolVersionBase):
    pass


class ProtocolVersionDto(ProtocolVersionBase):
    id: UUID


class ProtocolBase(BaseModel):
    protocol_type: ProtocolTypes
    name: str
    description: str | None


class ProtocolCreateDto(ProtocolBase):
    pass


class ProtocolDto(ProtocolBase):
    id: UUID
    versions: List[ProtocolVersionDto]
