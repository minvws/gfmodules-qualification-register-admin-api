from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.application.schema import ApplicationVersionDto


class QualifiedProtocolVersionsDto(BaseModel):
    id: UUID
    protocol_id: UUID
    version_id: UUID
    version: str
    description: str | None
    qualification_date: date
    archived_date: datetime | None = None


class HealthcareProviderQualificationCreateDto(BaseModel):
    qualification_date: date


class HealthcareProviderApplicationVersionDto(ApplicationVersionDto):
    pass


class HealthcareProviderBase(BaseModel):
    ura_code: str
    agb_code: str
    trade_name: str
    statutory_name: str


class HealthcareProviderCreateDto(HealthcareProviderBase):
    protocol_version_id: UUID


class HealthcareProviderDto(HealthcareProviderBase):
    id: UUID
    application_versions: List[HealthcareProviderApplicationVersionDto] = []
    qualified_protocols: List[QualifiedProtocolVersionsDto] = []
