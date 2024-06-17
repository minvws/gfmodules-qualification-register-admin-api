from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import types, ForeignKey, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.entities.base import Base
from app.db.entities import application
from app.db.entities import role


class ApplicationRole(Base):
    """
    Association object between Applications and Roles
    """

    __tablename__ = "applications_roles"
    __table_args__ = (
        PrimaryKeyConstraint("application_id", "role_id", name="applications_roles_pk"),
    )

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        unique=True,
        nullable=False,
        default=uuid4,
    )
    application_id: Mapped[UUID] = mapped_column(
        ForeignKey("applications.id"), nullable=False
    )
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application: Mapped["application.Application"] = relationship(
        back_populates="roles",
    )
    role: Mapped["role.Role"] = relationship(
        back_populates="applications", lazy="selectin"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            application_id=str(self.application_id),
            role_id=str(self.role_id),
            created_at=self.created_at,
            modified_at=self.modified_at,
            application=self.application,
            role=self.role,
        )