from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import types, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import healthcare_provider_application_version
from app.db.entities import healthcare_provider_qualification


class HealthcareProvider(Base):
    __tablename__ = "healthcare_providers"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    ura_code: Mapped[str] = mapped_column(
        "ura_code", String(50), nullable=False, unique=True
    )
    agb_code: Mapped[str] = mapped_column(
        "agb_code", String(50), nullable=False, unique=True
    )
    trade_name: Mapped[str] = mapped_column("trade_name", String(150), nullable=False)
    statutory_name: Mapped[str] = mapped_column(
        "statutory_name", String(150), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application_versions: Mapped[
        List[
            "healthcare_provider_application_version.HealthcareProviderApplicationVersion"
        ]
    ] = relationship(
        back_populates="healthcare_provider",
        lazy="selectin",
        cascade="save-update, delete, delete-orphan",
    )
    qualified_protocols: Mapped[
        List["healthcare_provider_qualification.HealthcareProviderQualification"]
    ] = relationship(back_populates="healthcare_provider")

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            ura_code=self.ura_code,
            agb_code=self.agb_code,
            trade_name=self.trade_name,
            statutory_name=self.statutory_name,
            created_at=self.created_at,
            modified_at=self.modified_at,
            application_versions=self.application_versions,
            qualified_protocols=self.qualified_protocols,
        )
