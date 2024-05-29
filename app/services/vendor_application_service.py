from typing import Sequence, List
from uuid import UUID

from app.db.entities.application import Application
from app.services.application_service import ApplicationService
from app.services.roles_service import RolesService
from app.services.system_type_service import SystemTypeService
from app.services.vendors_service import VendorService


class VendorApplicationService:

    def __init__(
        self,
        application_service: ApplicationService,
        vendor_service: VendorService,
        system_type_service: SystemTypeService,
        roles_service: RolesService,
    ):
        self.application_service = application_service
        self.vendor_service = vendor_service
        self.system_type_service = system_type_service
        self.roles_service = roles_service

    def deregister_one_vendor_application(
        self, kvk_number: str, application_name: str
    ) -> Application:
        vendor = self.vendor_service.get_one_vendor_by_kvk_number(kvk_number=kvk_number)
        deleted_applications = self.application_service.delete_one_application_by_name(
            application_name=application_name, vendor_id=vendor.id
        )

        return deleted_applications

    def register_one_app(
        self,
        vendor_id: UUID,
        application_name: str,
        application_version: str,
        system_type_names: List[str],
        role_names: List[str],
    ) -> Application:

        vendor = self.vendor_service.get_one_vendor_by_id(vendor_id)
        system_types = self.system_type_service.get_many_system_types(
            system_type_names=system_type_names
        )
        roles = self.roles_service.get_many_roles(role_names=role_names)

        new_application = self.application_service.add_one_application(
            application_name=application_name,
            version=application_version,
            system_types=system_types,
            roles=roles,
            vendor=vendor,
        )

        return new_application

    def get_all_vendor_applications(self, kvk_number: str) -> Sequence[Application]:
        vendor = self.vendor_service.get_one_vendor_by_kvk_number(kvk_number=kvk_number)
        return vendor.applications
