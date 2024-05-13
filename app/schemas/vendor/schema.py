from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel



class VendorApplicationVersion(BaseModel):
    version: str


class VendorApplicationBase(BaseModel):
    class Config:
        from_attributes = True

    name: str


class VendorApplicationRole(BaseModel):
    name: str
    description: str | None = None


class VendorApplicationType(BaseModel):
    name: str
    description: str | None = None


class VendorApplication(VendorApplicationBase):
    class Config:
        from_attributes = True

    id: UUID = uuid4()
    versions: List[VendorApplicationVersion] = []
    roles: List[VendorApplicationRole] = []
    system_types: List[VendorApplicationType] = []


class VendorBase(BaseModel):
    class Config:
        from_attributes = True

    kvk_number: str
    trade_name: str
    statutory_name: str


class VendorDTO(VendorBase):
    id: UUID
    applications: List[VendorApplication] = []


class VendorCreate(VendorBase):
    pass


class VendorApplicationCreate(VendorApplicationBase):
    version: str
