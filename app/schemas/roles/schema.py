from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    class Config:
        from_attributes = True

    description: str


class RoleCreateDTO(RoleBase):
    name: str


class RoleUpdateDTO(RoleBase):
    pass


class RoleDTO(RoleBase):
    id: UUID
    name: str
