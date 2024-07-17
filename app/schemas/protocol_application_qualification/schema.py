from datetime import date, datetime
from typing import List
from uuid import UUID

from app.schemas.default import BaseModelConfig


class ApplicationQualificationCreateDto(BaseModelConfig):
    qualification_date: date


class QualifiedApplicationVersionDto(BaseModelConfig):
    qualification_id: UUID
    application_id: UUID
    version_id: UUID
    version: str
    qualification_date: date
    archived_date: datetime | None = None


class ProtocolApplicationQualificationDto(BaseModelConfig):
    id: UUID
    protocol_id: UUID
    version: str
    description: str | None
    application_versions: List[QualifiedApplicationVersionDto] = []
