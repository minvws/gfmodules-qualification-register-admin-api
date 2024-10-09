from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from gfmodules_python_shared.schema.sql_model import SQLModelBase
from sqlalchemy import TIMESTAMP, ForeignKey, String, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entities import (
    application,
    application_version_qualification,
    healthcare_provider_application_version,
)


class ApplicationVersion(SQLModelBase):
    __tablename__ = "application_versions"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    version: Mapped[str] = mapped_column("version", String(50), nullable=False)
    application_id: Mapped[UUID] = mapped_column(
        ForeignKey("applications.id", name="applications_versions_application_fk")
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application: Mapped["application.Application"] = relationship(
        back_populates="versions"
    )
    healthcare_providers: Mapped[
        List[
            "healthcare_provider_application_version.HealthcareProviderApplicationVersion"
        ]
    ] = relationship(back_populates="application_version", lazy="selectin")
    qualified_protocol_versions: Mapped[
        List["application_version_qualification.ProtocolApplicationQualification"]
    ] = relationship(back_populates="application_version", lazy="selectin")
