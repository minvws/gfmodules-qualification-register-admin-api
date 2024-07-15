from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.schema import ApplicationVersionDTO


class QualifiedProtocolVersionsDTO(BaseModel):
    id: UUID
    protocol_id: UUID
    version_id: UUID
    version: str
    description: str | None
    qualification_date: date
    archived_date: datetime | None = None


class HealthcareProviderQualificationCreateDTO(BaseModel):
    qualification_date: date


class HealthcareProviderApplicationVersionDTO(ApplicationVersionDTO):
    pass


class HealthcareProviderBase(BaseModel):
    ura_code: str
    agb_code: str
    trade_name: str
    statutory_name: str


class HealthcareProviderCreateDTO(HealthcareProviderBase):
    protocol_version_id: UUID


class HealthcareProviderDTO(HealthcareProviderBase):
    id: UUID
    application_versions: List[HealthcareProviderApplicationVersionDTO] = []
    qualified_protocols: List[QualifiedProtocolVersionsDTO] = []
