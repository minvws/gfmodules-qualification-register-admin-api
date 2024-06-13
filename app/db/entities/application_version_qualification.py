from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import types, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import application_version
from app.db.entities import protocol_version


class ApplicationVersionQualification(Base):
    """
    Association object between ApplicationVersion and ProtocolVersion.
    This object determines the qualification of an application version against a
    defined protocol version.
    """

    __tablename__ = "application_versions_qualifications"
    __table_args__ = (
        PrimaryKeyConstraint(
            "application_version_id",
            "protocol_version_id",
            name="application_versions_qualifications_pk",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        unique=True,
        nullable=False,
        default=uuid4,
    )
    application_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("application_versions.id"), nullable=False
    )
    protocol_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("protocol_versions.id"), nullable=False
    )
    qualification_date: Mapped[datetime] = mapped_column(
        "qualification_date", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application_version: Mapped["application_version.ApplicationVersion"] = (
        relationship(back_populates="qualified_protocol_versions")
    )
    protocol_version: Mapped["protocol_version.ProtocolVersion"] = relationship(
        back_populates="qualified_application_versions"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            application_version_id=str(self.application_version_id),
            protocol_version_id=str(self.protocol_version_id),
            qualification_date=self.qualification_date,
            created_at=self.created_at,
            modified_at=self.modified_at,
            application_version=self.application_version,
            protocol_version=self.protocol_version,
        )
