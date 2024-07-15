from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums.protocol_types import ProtocolTypes


class ProtocolVersionBase(BaseModel):
    version: str
    description: str | None


class ProtocolVersionCreateDTO(ProtocolVersionBase):
    pass


class ProtocolVersionDTO(ProtocolVersionBase):
    id: UUID


class ProtocolBase(BaseModel):
    protocol_type: ProtocolTypes
    name: str
    description: str | None


class ProtocolCreateDTO(ProtocolBase):
    pass


class ProtocolDTO(ProtocolBase):
    id: UUID
    versions: List[ProtocolVersionDTO]
