from app.db.entities.application import Application
from app.db.entities.application_version import ApplicationVersion
from app.db.entities.application_role import ApplicationRole
from app.db.entities.application_type import ApplicationType
from app.schemas.application.schema import (
    ApplicationDto,
    ApplicationVersionDto,
    ApplicationRoleDto,
    ApplicationTypeDto,
)
from app.schemas.vendor.mapper import map_vendor_entity_to_summary_dto


def map_application_version_entity_to_dto(
    version: ApplicationVersion,
) -> ApplicationVersionDto:
    return ApplicationVersionDto(id=version.id, version=version.version)


def map_application_roles_entity_to_dto(
    app_role: ApplicationRole,
) -> ApplicationRoleDto:
    return ApplicationRoleDto(
        id=app_role.role_id,
        name=app_role.role.name,
        description=app_role.role.description,
    )


def map_application_system_type_entity_to_dto(
    app_type: ApplicationType,
) -> ApplicationTypeDto:
    return ApplicationTypeDto(
        id=app_type.system_type.id,
        name=app_type.system_type.name,
        description=app_type.system_type.description,
    )


def map_application_entity_to_dto(application: Application) -> ApplicationDto:

    versions = [
        map_application_version_entity_to_dto(version)
        for version in application.versions
    ]
    roles = [map_application_roles_entity_to_dto(role) for role in application.roles]
    system_types = [
        map_application_system_type_entity_to_dto(system_type)
        for system_type in application.system_types
    ]
    vendor = map_vendor_entity_to_summary_dto(application.vendor)

    return ApplicationDto(
        id=application.id,
        name=application.name,
        vendor=vendor,
        versions=versions,
        roles=roles,
        system_types=system_types,
        created_at=application.created_at,
        modified_at=application.modified_at,
    )
