from app.db.entities.application import Application
from app.db.entities.application_version import ApplicationVersion
from app.db.entities.vendor import Vendor
from app.db.entities.application_role import ApplicationRole
from app.db.entities.application_type import ApplicationType
from app.schemas.vendor.schema import (
    VendorDto,
    VendorApplicationDto,
    VendorApplicationVersionDto,
    VendorApplicationRoleDto,
    VendorApplicationTypeDto,
)


def map_vendor_entity_to_dto(entity: Vendor) -> VendorDto:
    def map_application_version_entity_to_model(
        app_version: ApplicationVersion,
    ) -> VendorApplicationVersionDto:
        return VendorApplicationVersionDto(version=app_version.version)

    def map_application_role_entity_to_model(
        role: ApplicationRole,
    ) -> VendorApplicationRoleDto:
        return VendorApplicationRoleDto(
            name=role.role.name, description=role.role.description
        )

    def map_application_types_entity_to_model(
        application_type: ApplicationType,
    ) -> VendorApplicationTypeDto:
        return VendorApplicationTypeDto(
            name=application_type.system_type.name,
            description=application_type.system_type.description,
        )

    def map_application_entity_to_model(app: Application) -> VendorApplicationDto:
        versions = [
            map_application_version_entity_to_model(version) for version in app.versions
        ]
        roles = [map_application_role_entity_to_model(role) for role in app.roles]
        system_types = [
            map_application_types_entity_to_model(system_type)
            for system_type in app.system_types
        ]
        return VendorApplicationDto(
            id=app.id,
            name=app.name,
            versions=versions,
            roles=roles,
            system_types=system_types,
        )

    return VendorDto(
        id=entity.id,
        kvk_number=entity.kvk_number,
        statutory_name=entity.statutory_name,
        trade_name=entity.trade_name,
        applications=[
            map_application_entity_to_model(app) for app in entity.applications
        ],
    )
