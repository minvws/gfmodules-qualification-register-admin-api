from enum import StrEnum, auto
import re
from typing import Type
from gfmodules_python_shared.schema.sql_model import TSQLModel
from inject import Binder, instance
from sqlalchemy.orm import Session, sessionmaker
from app.db.db import Database
from app.db.services import (
    Service,
    ApplicationRolesService,
    ApplicationService,
    ApplicationTypeService,
    ApplicationVersionService,
    HealthcareProviderApplicationVersionService,
    HealthcareProviderQualificationService,
    HealthcareProviderService,
    ProtocolApplicationQualificationService,
    ProtocolService,
    ProtocolVersionService,
    RoleService,
    SystemTypeService,
    VendorService,
)


def container_config(binder: Binder) -> None:
    database = Database("sqlite:///:memory:", generate_tables=True)
    application_service = ApplicationService()
    healthcare_provider_service = HealthcareProviderService()
    protocol_service = ProtocolService()

    (
        binder.bind(Database, database)
        .bind(sessionmaker[Session], sessionmaker(database.engine))
        .bind(VendorService, VendorService())
        .bind(RoleService, RoleService())
        .bind(SystemTypeService, SystemTypeService())
        .bind(ApplicationService, application_service)
        .bind(ApplicationTypeService, ApplicationTypeService())
        .bind(ProtocolService, protocol_service)
        .bind(HealthcareProviderService, healthcare_provider_service)
        .bind(
            ApplicationVersionService,
            ApplicationVersionService(application_service=application_service),
        )
        .bind(
            ApplicationRolesService,
            ApplicationRolesService(application_service=application_service),
        )
        .bind(
            HealthcareProviderApplicationVersionService,
            HealthcareProviderApplicationVersionService(
                healthcare_provider_service=healthcare_provider_service
            ),
        )
        .bind(
            ProtocolVersionService,
            ProtocolVersionService(protocol_service=protocol_service),
        )
        .bind(
            ProtocolApplicationQualificationService,
            ProtocolApplicationQualificationService(),
        )
        .bind(
            HealthcareProviderQualificationService,
            HealthcareProviderQualificationService(),
        )
    )


class Services(StrEnum):
    APPLICATION_ROLES = auto()
    APPLICATION = auto()
    APPLICATION_TYPE = auto()
    APPLICATION_VERSION = auto()
    HEALTHCARE_PROVIDER_APPLICATION_VERSION = auto()
    HEALTHCARE_PROVIDER_QUALIFICATION = auto()
    HEALTHCARE_PROVIDER = auto()
    PROTOCOL_APPLICATION_QUALIFICATION = auto()
    PROTOCOL = auto()
    PROTOCOL_VERSION = auto()
    ROLE = auto()
    SYSTEM_TYPE = auto()
    VENDOR = auto()

    @property
    def _to_pascal_case(self) -> str:
        return re.sub(
            r"(^|_)([a-z])", lambda match: match.group(2).upper(), self.lower()
        )

    @property
    def _service_type(self) -> Type[Service]:
        return eval(f"{self._to_pascal_case}Service")  # type: ignore

    def get_instance(self) -> Service:
        return instance(self._service_type)  # type: ignore


def are_the_same_entity(actual: TSQLModel, comparer: TSQLModel) -> bool:
    return all(
        getattr(actual, key) == getattr(comparer, key)
        for key in actual.__table__.columns.keys()  # noqa: SIM118
    )
