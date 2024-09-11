from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from app.schemas.default import BaseModelConfig
from app.schemas.roles.schema import RoleDto
from app.schemas.system_type.schema import SystemTypeDto


class VendorApplicationVersionDto(BaseModelConfig):
    id: UUID
    version: str


class VendorApplicationBase(BaseModelConfig):
    name: str


class VendorApplicationDto(VendorApplicationBase):
    id: UUID = uuid4()
    created_at: datetime
    modified_at: datetime
    versions: List[VendorApplicationVersionDto] = []
    roles: List[RoleDto] = []
    system_types: List[SystemTypeDto] = []


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
