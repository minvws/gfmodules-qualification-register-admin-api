from datetime import date, datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class ApplicationQualificationCreateDTO(BaseModel):
    qualification_date: date


class QualifiedApplicationVersionDTO(BaseModel):
    qualification_id: UUID
    application_id: UUID
    version_id: UUID
    version: str
    qualification_date: date
    archived_date: datetime | None = None


class ProtocolApplicationQualificationDTO(BaseModel):
    id: UUID
    protocol_id: UUID
    version: str
    description: str
    application_versions: List[QualifiedApplicationVersionDTO] = []
