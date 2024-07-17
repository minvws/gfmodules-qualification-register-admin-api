from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel


class ApplicationVersionBase(BaseModel):
    version: str


class ApplicationVersionCreateDto(ApplicationVersionBase):
    pass


class ApplicationVersionDto(ApplicationVersionBase):
    id: UUID


class ApplicationRoleDto(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class ApplicationTypeDto(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class ApplicationBase(BaseModel):
    name: str


class ApplicationDto(ApplicationBase):
    id: UUID = uuid4()
    vendor_id: UUID
    vendor_kvk_number: str
    vendor_trade_name: str
    versions: List[ApplicationVersionDto] = []
    roles: List[ApplicationRoleDto] = []
    system_types: List[ApplicationTypeDto] = []
