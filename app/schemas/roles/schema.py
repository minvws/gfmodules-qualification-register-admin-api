from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    class Config:
        from_attributes = True

    description: str | None


class RoleCreateDto(RoleBase):
    name: str


class RoleUpdateDto(RoleBase):
    pass


class RoleDto(RoleBase):
    id: UUID
    name: str
