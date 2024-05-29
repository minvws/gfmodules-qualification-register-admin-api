from app.db.entities.application import Application
from app.db.entities.application_version import ApplicationVersion
from app.db.entities.application_role import ApplicationRole
from app.db.entities.application_type import ApplicationType
from app.schemas.application.schema import (
    ApplicationDTO,
    ApplicationVersionDTO,
    ApplicationRoleDTO,
    SystemTypeInApplicationDTO,
)


def map_application_version_entity_to_dto(
    version: ApplicationVersion,
) -> ApplicationVersionDTO:
    return ApplicationVersionDTO(version_id=version.id, version=version.version)


def map_application_roles_entity_to_dto(
    app_role: ApplicationRole,
) -> ApplicationRoleDTO:
    return ApplicationRoleDTO(
        id=app_role.role_id,
        name=app_role.role.name,
        description=app_role.role.description,
    )


def map_application_system_type_entity_to_dto(
    app_type: ApplicationType,
) -> SystemTypeInApplicationDTO:
    return SystemTypeInApplicationDTO(
        id=app_type.system_type.id,
        name=app_type.system_type.name,
        description=app_type.system_type.description,
    )


def map_application_entity_to_dto(application: Application) -> ApplicationDTO:

    versions = [
        map_application_version_entity_to_dto(version)
        for version in application.versions
    ]
    roles = [map_application_roles_entity_to_dto(role) for role in application.roles]
    system_types = [
        map_application_system_type_entity_to_dto(system_type)
        for system_type in application.system_types
    ]
    return ApplicationDTO(
        id=application.id,
        name=application.name,
        vendor_id=application.vendor_id,
        vendor_trade_name=application.vendor.trade_name,
        vendor_kvk_number=application.vendor.kvk_number,
        versions=versions,
        roles=roles,
        system_types=system_types,
    )
