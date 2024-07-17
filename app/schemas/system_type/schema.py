from uuid import UUID

from pydantic import BaseModel


class SystemTypeBase(BaseModel):
    name: str
    description: str | None


class SystemTypeCreateDto(SystemTypeBase):
    pass


class SystemTypeDto(SystemTypeBase):
    id: UUID
