from uuid import UUID

from app.schemas.default import BaseModelConfig


class SystemTypeBase(BaseModelConfig):
    name: str
    description: str | None


class SystemTypeCreateDto(SystemTypeBase):
    pass


class SystemTypeDto(SystemTypeBase):
    id: UUID
