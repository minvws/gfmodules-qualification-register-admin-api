from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import types, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import application
from app.db.entities import healthcare_provider_application_version
from app.db.entities import application_version_qualification


class ApplicationVersion(Base):
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
    ] = relationship(
        back_populates="application_version",
        lazy="selectin",
        cascade="delete, delete-orphan",
    )
    qualified_protocol_versions: Mapped[
        List["application_version_qualification.ApplicationVersionQualification"]
    ] = relationship(back_populates="application_version")

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            version=self.version,
            application_id=self.application_id,
            created_at=self.created_at,
            modified_at=self.modified_at,
            application=self.application,
            healcare_providers=self.healthcare_providers,
            qualified_protocol_versions=self.qualified_protocol_versions,
        )
