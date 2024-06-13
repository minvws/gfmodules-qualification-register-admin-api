from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import types, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import protocol
from app.db.entities import healthcare_provider_qualification
from app.db.entities import application_version_qualification


class ProtocolVersion(Base):
    __tablename__ = "protocol_versions"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    version: Mapped[str] = mapped_column("version", String(50), nullable=False)
    description: Mapped[str] = mapped_column("description", String, nullable=True)
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
        List["application_version_qualification.ApplicationVersionQualification"]
    ] = relationship(back_populates="protocol_version")

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            version=self.version,
            description=self.description,
            protocol_id=str(self.protocol_id),
            created_at=self.created_at,
            modified_at=self.modified_at,
            protocol=self.protocol,
            qualified_healthcare_providers=self.qualified_healthcare_providers,
            qualified_application_versions=self.qualified_application_versions,
        )
