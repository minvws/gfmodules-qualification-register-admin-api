from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    class Config:
        from_attributes = True

    description: str


class RoleCreate(RoleBase):
    name: str


class RoleUpdate(RoleBase):
    pass


class RoleDTO(RoleBase):
    id: UUID
    name: str
