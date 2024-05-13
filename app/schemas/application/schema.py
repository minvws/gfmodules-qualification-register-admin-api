from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel


class VersionInApplicationDTO(BaseModel):
    version_id: UUID
    version: str


class RoleInApplicationDTO(BaseModel):
    role_id: UUID
    name: str
    description: str | None = None


class SystemTypeInApplicationDTO(BaseModel):
    name: str
    description: str | None = None


class ApplicationBase(BaseModel):
    name: str


class ApplicationDTO(ApplicationBase):
    id: UUID = uuid4()
    vendor_id: UUID
    vendor_kvk_number: str
    vendor_trade_name: str
    versions: List[VersionInApplicationDTO] = []
    roles: List[RoleInApplicationDTO] = []
    system_types: List[SystemTypeInApplicationDTO] = []
