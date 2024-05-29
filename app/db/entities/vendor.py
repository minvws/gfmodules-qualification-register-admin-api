from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import types, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import application


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    kvk_number: Mapped[str] = mapped_column(
        "kvk_number", String(50), nullable=False, unique=True
    )
    trade_name: Mapped[str] = mapped_column(
        "trade_name", String(150), nullable=False, unique=True
    )
    statutory_name: Mapped[str] = mapped_column(
        "statutory_name", String(150), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    applications: Mapped[List["application.Application"]] = relationship(
        back_populates="vendor", lazy="selectin", cascade="all, delete, delete-orphan"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            kvk_number=self.kvk_number,
            trade_name=self.trade_name,
            statutory_name=self.statutory_name,
            applications=self.applications,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )
