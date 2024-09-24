from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from gfmodules_python_shared.schema.sql_model import SQLModelBase
from sqlalchemy import TIMESTAMP, ForeignKey, String, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entities import (
    application_version_qualification,
    healthcare_provider_qualification,
    protocol,
)


class ProtocolVersion(SQLModelBase):
    __tablename__ = "protocol_versions"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    version: Mapped[str] = mapped_column("version", String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(
        "description", String, nullable=True
    )
    protocol_id: Mapped[UUID] = mapped_column(
        ForeignKey("protocols.id", name="protocols_versions_protocols_fk")
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    protocol: Mapped["protocol.Protocol"] = relationship(back_populates="versions")
    qualified_healthcare_providers: Mapped[
        List["healthcare_provider_qualification.HealthcareProviderQualification"]
    ] = relationship(back_populates="protocol_version")
    qualified_application_versions: Mapped[
        List["application_version_qualification.ProtocolApplicationQualification"]
    ] = relationship(
        back_populates="protocol_version",
        lazy="selectin",
        cascade="save-update, delete, delete-orphan",
    )
