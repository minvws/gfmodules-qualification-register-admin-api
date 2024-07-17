from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class ApplicationQualificationCreateDto(BaseModel):
    qualification_date: date


class QualifiedApplicationVersionDto(BaseModel):
    qualification_id: UUID
    application_id: UUID
    version_id: UUID
    version: str
    qualification_date: date
    archived_date: datetime | None = None


class ProtocolApplicationQualificationDto(BaseModel):
    id: UUID
    protocol_id: UUID
    version: str
    description: str | None
    application_versions: List[QualifiedApplicationVersionDto] = []
