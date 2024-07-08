from typing import Sequence, List
from uuid import UUID

from app.db.repository.roles_repository import RolesRepository
from app.db.repository.system_types_repository import SystemTypesRepository
from app.db.repository.vendors_repository import VendorsRepository
from app.db.entities.application import Application
from app.db.repository.applications_repository import ApplicationsRepository
from app.db.session_manager import session_manager, get_repository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    ApplicationAlreadyExistsException,
)
from app.factory.application_factory import ApplicationFactory


class ApplicationService:

    @session_manager
    def get_all(
        self, application_repository: ApplicationsRepository = get_repository()
    ) -> Sequence[Application]:
        applications = application_repository.get_all()
        return applications

    @session_manager
    def get_by_vendor_id(
        self, vendor_id: UUID, vendor_repository: VendorsRepository = get_repository()
    ) -> Sequence[Application]:
        vendor = vendor_repository.get_or_fail(id=vendor_id)
        return vendor.applications

    @session_manager
    def get_one(
        self,
        application_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        return application

    @session_manager
    def remove_one(
        self,
        application_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
    ) -> Application:
        application = self.get_one(application_id)
        if application is None:
            raise ApplicationNotFoundException()

        application_repository.delete(application)
        return application

    @session_manager
    def remove_one_by_name(
        self,
        application_name: str,
        vendor_id: UUID,
        application_repository: ApplicationsRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(
            name=application_name, vendor_id=vendor_id
        )
        if application is None:
            raise ApplicationNotFoundException()

        application_repository.delete(application)
        return application

    @session_manager
    def add_one(
        self,
        vendor_id: UUID,
        application_name: str,
        version: str,
        role_names: List[str],
        system_type_names: List[str],
        application_repository: ApplicationsRepository = get_repository(),
        vendor_repository: VendorsRepository = get_repository(),
        system_type_repository: SystemTypesRepository = get_repository(),
        roles_repository: RolesRepository = get_repository(),
    ) -> Application:
        vendor = vendor_repository.get_or_fail(id=vendor_id)

        system_types = system_type_repository.get_by_property_exact(
            "name", system_type_names
        )

        roles = roles_repository.get_by_property_exact("name", role_names)

        application = application_repository.get(
            name=application_name, vendor_id=vendor.id
        )
        if application is not None:
            raise ApplicationAlreadyExistsException()

        new_application = ApplicationFactory.create_instance(
            application_name=application_name,
            application_version=version,
            vendor=vendor,
            application_roles=roles,
            application_types=system_types,
        )
        application_repository.create(new_application)

        return new_application
