from uuid import UUID

from app.schemas.default import BaseModelConfig


class RoleBase(BaseModelConfig):
    description: str | None


class RoleCreateDto(RoleBase):
    name: str


class RoleUpdateDto(RoleBase):
    pass


class RoleDto(RoleBase):
    id: UUID
    name: str
