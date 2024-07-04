from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint, types, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entities.base import Base
from app.db.entities import application_version
from app.db.entities import healthcare_provider


class HealthcareProviderApplicationVersion(Base):
    """
    Association object between HealthcareProvider and ApplicationVersion
    """

    __tablename__ = "healthcare_providers_application_versions"
    __table_args__ = (
        PrimaryKeyConstraint(
            "healthcare_provider_id",
            "application_version_id",
            name="healthcare_providers_application_version_pk",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        unique=True,
        nullable=False,
        default=uuid4,
    )
    healthcare_provider_id: Mapped[UUID] = mapped_column(
        ForeignKey("healthcare_providers.id"), nullable=False
    )
    application_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("application_versions.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    healthcare_provider: Mapped["healthcare_provider.HealthcareProvider"] = (
        relationship(back_populates="application_versions")
    )
    application_version: Mapped["application_version.ApplicationVersion"] = (
        relationship(back_populates="healthcare_providers", lazy="selectin")
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            healthcare_provider_id=str(self.healthcare_provider_id),
            application_version_id=str(self.application_version_id),
            created_at=self.created_at,
            modified_at=self.modified_at,
            heathcare_provider=self.healthcare_provider,
            application_version=self.application_version,
        )
