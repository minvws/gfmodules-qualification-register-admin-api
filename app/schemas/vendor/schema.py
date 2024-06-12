from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel


class VendorApplicationVersionDTO(BaseModel):
    version: str


class VendorApplicationBase(BaseModel):
    class Config:
        from_attributes = True

    name: str


class VendorApplicationRoleDTO(BaseModel):
    name: str
    description: str | None = None


class VendorApplicationTypeDTO(BaseModel):
    name: str
    description: str | None = None


class VendorApplicationDTO(VendorApplicationBase):
    class Config:
        from_attributes = True

    id: UUID = uuid4()
    versions: List[VendorApplicationVersionDTO] = []
    roles: List[VendorApplicationRoleDTO] = []
    system_types: List[VendorApplicationTypeDTO] = []


class VendorBase(BaseModel):
    class Config:
        from_attributes = True

    kvk_number: str
    trade_name: str
    statutory_name: str


class VendorDTO(VendorBase):
    id: UUID
    applications: List[VendorApplicationDTO] = []


class VendorCreateDTO(VendorBase):
    pass


class VendorApplicationCreateDTO(VendorApplicationBase):
    version: str
    roles: List[str]
    system_types: List[str]
