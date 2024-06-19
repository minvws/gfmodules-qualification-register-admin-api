from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.schema import ApplicationVersionDTO


class HealthcareProviderApplicationVersionDTO(ApplicationVersionDTO):
    pass


class HealthcareProviderBase(BaseModel):
    ura_code: str
    agb_code: str
    trade_name: str
    statutory_name: str


class HealthcareProviderCreateDTO(HealthcareProviderBase):
    pass


class HealthcareProviderDTO(HealthcareProviderBase):
    id: UUID
    application_versions: List[HealthcareProviderApplicationVersionDTO] = []
