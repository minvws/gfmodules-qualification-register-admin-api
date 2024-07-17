from typing import List
from uuid import UUID, uuid4

from app.schemas.default import BaseModelConfig


class VendorApplicationVersionDto(BaseModelConfig):
    version: str


class VendorApplicationBase(BaseModelConfig):
    name: str


class VendorApplicationRoleDto(BaseModelConfig):
    name: str
    description: str | None = None


class VendorApplicationTypeDto(BaseModelConfig):
    name: str
    description: str | None = None


class VendorApplicationDto(VendorApplicationBase):
    id: UUID = uuid4()
    versions: List[VendorApplicationVersionDto] = []
    roles: List[VendorApplicationRoleDto] = []
    system_types: List[VendorApplicationTypeDto] = []


class VendorBase(BaseModelConfig):
    kvk_number: str
    trade_name: str
    statutory_name: str


class VendorDto(VendorBase):
    id: UUID
    applications: List[VendorApplicationDto] = []


class VendorCreateDto(VendorBase):
    pass


class VendorApplicationCreateDto(VendorApplicationBase):
    version: str
    roles: List[str]
    system_types: List[str]
