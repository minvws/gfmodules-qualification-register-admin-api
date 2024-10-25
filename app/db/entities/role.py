from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from gfmodules_python_shared.schema.sql_model import SQLModelBase
from sqlalchemy import types, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities import application_role


class Role(SQLModelBase):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(
        "id", types.Uuid, primary_key=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column("name", String(150), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(
        "description", String, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    applications: Mapped[List["application_role.ApplicationRole"]] = relationship(
        back_populates="role", cascade="delete,delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return self._repr(**self.to_dict(exclude={"applications"}))
