from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from gfmodules_python_shared.schema.sql_model import SQLModelBase
from sqlalchemy import TIMESTAMP, Date, ForeignKey, PrimaryKeyConstraint, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entities import application_version, protocol_version


class ProtocolApplicationQualification(SQLModelBase):
    """
    Association object between ApplicationVersion and ProtocolVersion.
    This object determines the qualification of an application version against a
    defined protocol version.
    """

    __tablename__ = "protocol_application_qualifications"
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
    qualification_date: Mapped[date] = mapped_column(
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

    protocol_version: Mapped["protocol_version.ProtocolVersion"] = relationship(
        back_populates="qualified_application_versions"
    )
    application_version: Mapped["application_version.ApplicationVersion"] = (
        relationship(back_populates="qualified_protocol_versions", lazy="selectin")
    )

    def __repr__(self) -> str:
        return self._repr(**self.to_dict(exclude={"archived_date"}))
