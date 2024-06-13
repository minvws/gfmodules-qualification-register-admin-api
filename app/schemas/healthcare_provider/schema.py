from uuid import UUID

from pydantic import BaseModel


class HealthcareProviderBase(BaseModel):
    ura_code: str
    agb_code: str
    trade_name: str
    statutory_name: str


class HealthcareProviderCreateDTO(HealthcareProviderBase):
    pass


class HealthcareProviderDTO(HealthcareProviderBase):
    id: UUID
