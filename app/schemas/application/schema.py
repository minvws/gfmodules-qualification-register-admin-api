from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel


class ApplicationVersionBase(BaseModel):
    version: str


class ApplicationVersionCreateDTO(ApplicationVersionBase):
    pass


class ApplicationVersionDTO(ApplicationVersionBase):
    id: UUID


class ApplicationRoleDTO(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class ApplicationTypeDTO(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class ApplicationBase(BaseModel):
    name: str


class ApplicationDTO(ApplicationBase):
    id: UUID = uuid4()
    vendor_id: UUID
    vendor_kvk_number: str
    vendor_trade_name: str
    versions: List[ApplicationVersionDTO] = []
    roles: List[ApplicationRoleDTO] = []
    system_types: List[ApplicationTypeDTO] = []
