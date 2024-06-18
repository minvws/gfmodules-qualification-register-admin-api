from uuid import UUID

from pydantic import BaseModel

from app.schemas.enums.protocol_types import ProtocolTypes


class ProtocolBase(BaseModel):
    protocol_type: ProtocolTypes
    name: str
    description: str


class ProtocolCreateDTO(ProtocolBase):
    pass


class ProtocolDTO(ProtocolBase):
    id: UUID
