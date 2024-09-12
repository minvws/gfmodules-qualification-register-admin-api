from uuid import UUID

from pydantic import Field

from app.schemas.default import BaseModelConfig


class RoleBase(BaseModelConfig):
    description: str | None


class RoleCreateDto(RoleBase):
    name: str = Field(max_length=150)


class RoleUpdateDto(RoleBase):
    pass


class RoleDto(RoleBase):
    id: UUID
    name: str
