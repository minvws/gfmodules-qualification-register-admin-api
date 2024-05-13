from datetime import datetime
from typing import List, get_args, Literal
from uuid import UUID, uuid4

from sqlalchemy import (
    types,
    String,
    TIMESTAMP,
    Enum,
    ForeignKey,
    PrimaryKeyConstraint,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.entities.base import Base


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

    applications: Mapped[List["Application"]] = relationship(
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


ProtocolTypes = Literal["InformationStandard", "Directive"]


class Protocol(Base):
    __tablename__ = "protocols"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    protocol_type: Mapped[ProtocolTypes] = mapped_column(
        "protocol_type",
        Enum(
            *get_args(ProtocolTypes),
            name="protocol_type",
            create_constraint=True,
            validate_strings=True,
        ),
    )
    protocol_name: Mapped[str] = mapped_column(
        "protocol_name", String(150), nullable=False
    )
    description: Mapped[datetime] = mapped_column("description", String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    versions: Mapped[List["ProtocolVersion"]] = relationship(back_populates="protocol")

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            protocol_type=self.protocol_type,
            protocol_name=self.protocol_name,
            description=self.description,
            created_at=self.created_at,
            modified_at=self.modified_at,
            versions=self.versions,
        )


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

    protocol: Mapped["Protocol"] = relationship(back_populates="versions")
    qualified_healthcare_providers: Mapped[List["HealthcareProviderQualification"]] = (
        relationship(back_populates="protocol_version")
    )
    qualified_application_versions: Mapped[List["ApplicationVersionQualification"]] = (
        relationship(back_populates="protocol_version")
    )

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


class SystemType(Base):
    __tablename__ = "system_types"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column("name", String(150), nullable=False)
    description: Mapped[str] = mapped_column("description", String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    applications: Mapped[List["ApplicationType"]] = relationship(
        back_populates="system_type"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            modified_at=self.modified_at,
            applications=self.applications,
        )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(
        "id", types.Uuid, primary_key=True, nullable=False, default=uuid4
    )
    name: Mapped[str] = mapped_column("name", String(150), nullable=False, unique=True)
    description: Mapped[str] = mapped_column("description", String)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    applications: Mapped[List["ApplicationRole"]] = relationship(
        back_populates="role", lazy="selectin", cascade="all, delete, delete-orphan"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            modified_at=self.modified_at,
        )


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
    created_at: Mapped[TIMESTAMP] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[TIMESTAMP] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    vendor: Mapped["Vendor"] = relationship(
        back_populates="applications", cascade="all, delete"
    )
    versions: Mapped[List["ApplicationVersion"]] = relationship(
        back_populates="application", lazy="selectin", cascade="all, delete"
    )
    system_types: Mapped[List["ApplicationType"]] = relationship(
        back_populates="application"
    )
    roles: Mapped[List["ApplicationRole"]] = relationship(
        back_populates="application",
        lazy="selectin",
        cascade="all, delete, delete-orphan",
    )

    def __repr__(self) -> str:
        return self._repr(
            id=self.id,
            name=self.name,
            vendor_id=self.vendor_id,
            created_at=self.created_at,
            modified_at=self.modified_at,
            vendor=self.vendor,
            versions=self.versions,
            system_types=self.system_types,
        )


class ApplicationVersion(Base):
    __tablename__ = "application_versions"

    id: Mapped[UUID] = mapped_column(
        "id",
        types.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid4,
    )
    version: Mapped[str] = mapped_column("version", String(50), nullable=False)
    application_id: Mapped[UUID] = mapped_column(
        ForeignKey("applications.id", name="applications_versions_application_fk")
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application: Mapped["Application"] = relationship(
        back_populates="versions", lazy="selectin"
    )
    healthcare_providers: Mapped[List["HealthcareProviderApplicationVersion"]] = (
        relationship(back_populates="application_version")
    )
    qualified_protocol_versions: Mapped[List["ApplicationVersionQualification"]] = (
        relationship(back_populates="application_version")
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            version=self.version,
            application_id=self.application_id,
            created_at=self.created_at,
            modified_at=self.modified_at,
            application=self.application,
            healcare_providers=self.healthcare_providers,
            qualified_protocol_versions=self.qualified_protocol_versions,
        )


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

    application: Mapped["Application"] = relationship(
        back_populates="roles",
        lazy="selectin",
    )
    role: Mapped["Role"] = relationship(
        back_populates="applications",
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


class ApplicationType(Base):
    """
    Association object between Application and a SystemType
    """

    __tablename__ = "applications_types"
    __table_args__ = (
        PrimaryKeyConstraint(
            "application_id", "system_type_id", name="applications_types_pk"
        ),
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
    system_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("system_types.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    application: Mapped["Application"] = relationship(back_populates="system_types")
    system_type: Mapped["SystemType"] = relationship(back_populates="applications")

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            application_id=str(self.application_id),
            system_type_id=str(self.system_type_id),
            created_at=self.created_at,
            modified_at=self.modified_at,
            application=self.application,
            system_type=self.system_type,
        )


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
    abg_code: Mapped[str] = mapped_column(
        "abg_code", String(50), nullable=False, unique=True
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

    application_versions: Mapped[List["HealthcareProviderApplicationVersion"]] = (
        relationship(back_populates="healthcare_provider")
    )
    qualified_protocols: Mapped[List["HealthcareProviderQualification"]] = relationship(
        back_populates="healthcare_provider"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            ura_code=self.ura_code,
            abg_code=self.abg_code,
            trade_name=self.trade_name,
            statutory_name=self.statutory_name,
            created_at=self.created_at,
            modified_at=self.modified_at,
            application_versions=self.application_versions,
            qualified_protocols=self.qualified_protocols,
        )


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

    healthcare_provider: Mapped["HealthcareProvider"] = relationship(
        back_populates="application_versions"
    )
    application_version: Mapped["ApplicationVersion"] = relationship(
        back_populates="healthcare_providers"
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


class HealthcareProviderQualification(Base):
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
    created_at: Mapped[datetime] = mapped_column(
        "created_at", TIMESTAMP, nullable=False, default=datetime.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        "modified_at", TIMESTAMP, nullable=False, default=datetime.now()
    )

    healthcare_provider: Mapped["HealthcareProvider"] = relationship(
        back_populates="qualified_protocols"
    )
    protocol_version: Mapped["ProtocolVersion"] = relationship(
        back_populates="qualified_healthcare_providers"
    )

    def __repr__(self) -> str:
        return self._repr(
            id=str(self.id),
            healthcare_provider_id=str(self.healthcare_provider_id),
            protocol_version_id=str(self.protocol_version_id),
            qualification_date=self.qualification_date,
            created_at=self.created_at,
            modified_at=self.modified_at,
            healthcare_provider=self.healthcare_provider,
            protocol_version=self.protocol_version,
        )


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

    application_version: Mapped["ApplicationVersion"] = relationship(
        back_populates="qualified_protocol_versions"
    )
    protocol_version: Mapped["ProtocolVersion"] = relationship(
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
