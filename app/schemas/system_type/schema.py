from uuid import UUID

from pydantic import BaseModel


class SystemTypeBase(BaseModel):
    name: str
    description: str


class SystemTypeCreateDTO(SystemTypeBase):
    pass


class SystemTypeDTO(SystemTypeBase):
    id: UUID
