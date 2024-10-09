from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from gfmodules_python_shared.schema.sql_model import SQLModelBase
from sqlalchemy import types, TIMESTAMP, PrimaryKeyConstraint, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from app.db.entities import healthcare_provider
from app.db.entities import protocol_version


class HealthcareProviderQualification(SQLModelBase):
    """
    Association between HealthcareProvider and ProtocolVersion. This entity determines
    The qualification of healthcare provider with a protocol
    """

    __tablename__ = "healthcare_providers_qualifications"
    __table_args__ = (
        PrimaryKeyConstraint(
            "healthcare_provider_id",
            "protocol_version_id",
            name="healthcare_providers_qualifications_pk",
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
    protocol_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("protocol_versions.id"), nullable=False
    )
    qualification_date: Mapped[datetime] = mapped_column(
        "qualification_date", Date, nullable=False
    )
    archived_date: Mapped[Optional[datetime]] = mapped_column(
        "archived_date", TIMESTAMP, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    healthcare_provider: Mapped["healthcare_provider.HealthcareProvider"] = (
        relationship(back_populates="qualified_protocols")
    )
    protocol_version: Mapped["protocol_version.ProtocolVersion"] = relationship(
        back_populates="qualified_healthcare_providers", lazy="selectin"
    )

    def __repr__(self) -> str:
        return self._repr(**self.to_dict(exclude={"archived_date"}))
