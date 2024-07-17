from typing import List
from uuid import UUID

from app.schemas.default import BaseModelConfig
from app.schemas.enums.protocol_types import ProtocolTypes


class ProtocolVersionBase(BaseModelConfig):
    version: str
    description: str | None


class ProtocolVersionCreateDto(ProtocolVersionBase):
    pass


class ProtocolVersionDto(ProtocolVersionBase):
    id: UUID


class ProtocolBase(BaseModelConfig):
    protocol_type: ProtocolTypes
    name: str
    description: str | None


class ProtocolCreateDto(ProtocolBase):
    pass


class ProtocolDto(ProtocolBase):
    id: UUID
    versions: List[ProtocolVersionDto]
