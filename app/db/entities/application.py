from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint, types, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import vendor
from app.db.entities import application_version
from app.db.entities import application_type
from app.db.entities import application_role


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("id", "name"),)

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column("name", String(150), unique=True, nullable=False)
    vendor_id: Mapped[UUID] = mapped_column(
        ForeignKey("vendors.id", name="applications_vendors_fk")
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    vendor: Mapped["vendor.Vendor"] = relationship(
        back_populates="applications", lazy="joined"
    )
    versions: Mapped[List["application_version.ApplicationVersion"]] = relationship(
        back_populates="application",
        lazy="selectin",
        cascade="all, delete, delete-orphan",
    )
    system_types: Mapped[List["application_type.ApplicationType"]] = relationship(
        back_populates="application",
        lazy="selectin",
        cascade="save-update, delete, delete-orphan",
    )
    roles: Mapped[List["application_role.ApplicationRole"]] = relationship(
        back_populates="application",
        lazy="selectin",
        cascade="save-update, delete, delete-orphan",
    )

    def __repr__(self) -> str:
        return self._repr(
            id=self.id,
            name=self.name,
            vendor_id=self.vendor_id,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )
