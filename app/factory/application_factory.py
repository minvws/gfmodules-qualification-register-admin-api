from typing import Sequence

from app.db.entities.application import Application
from app.db.entities.application_version import ApplicationVersion
from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.factory.application_roles_factory import ApplicationRolesFactory
from app.factory.application_type_factory import ApplicationTypeFactory


class ApplicationFactory:

    @staticmethod
    def create_instance(
        application_name: str,
    ) -> Application:
        return Application(name=application_name)

    @staticmethod
    def create_rich_instance(
        application_name: str,
        application_version: str,
        vendor: Vendor,
        application_types: Sequence[SystemType],
        application_roles: Sequence[Role],
    ) -> Application:
        """
        Creates a new Application instance with populated children properties.
        """
        new_application = Application(name=application_name)
        version = ApplicationVersion(version=application_version)
        new_application.versions.append(version)
        new_application.vendor = vendor

        for role in application_roles:
            new_application_role = ApplicationRolesFactory.create_instance()
            new_application_role.role = role
            new_application_role.application = new_application
            new_application.roles.append(new_application_role)

        for system_type in application_types:
            new_application_type = ApplicationTypeFactory.create_instance()
            new_application_type.system_type = system_type
            new_application_type.application = new_application
            new_application.system_types.append(new_application_type)

        return new_application
