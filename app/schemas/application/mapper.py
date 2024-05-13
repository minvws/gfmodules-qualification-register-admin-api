from app.db.entities.models import (
    Application,
    ApplicationVersion,
    ApplicationRole,
    ApplicationType,
)
from app.schemas.application.schema import (
    ApplicationDTO,
    VersionInApplicationDTO,
    RoleInApplicationDTO,
    SystemTypeInApplicationDTO,
)


def map_application_entity_to_dto(application: Application) -> ApplicationDTO:
    def map_application_version_entity_to_dto(
        version: ApplicationVersion,
    ) -> VersionInApplicationDTO:
        return VersionInApplicationDTO(version_id=version.id, version=version.version)

    def map_application_roles_entity_to_dto(
        app_role: ApplicationRole,
    ) -> RoleInApplicationDTO:
        return RoleInApplicationDTO(
            role_id=app_role.role_id,
            name=app_role.role.name,
            description=app_role.role.description,
        )

    def map_application_system_type_entity_to_dto(
        app_type: ApplicationType,
    ) -> SystemTypeInApplicationDTO:
        return SystemTypeInApplicationDTO(
            name=app_type.system_type.name, description=app_type.system_type.description
        )

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
