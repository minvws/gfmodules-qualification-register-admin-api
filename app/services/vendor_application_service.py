from typing import Sequence

from app.db.entities.models import Application, Vendor
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    ApplicationAlreadyExistsException,
    ApplicationNotFoundException,
)
from app.factory.application_factory import ApplicationFactory
from app.services.application_service import ApplicationService
from app.services.vendors_service import VendorService


class VendorApplicationService:

    def __init__(
        self, application_service: ApplicationService, vendor_service: VendorService
    ):
        self.application_service = application_service
        self.vendor_service = vendor_service

    def register_one_application(
        self, kvk_number: str, application_name: str, application_version: str
    ) -> Vendor:
        vendor_repository = self.vendor_service.get_vendors_repository()
        vendor = vendor_repository.find_one(kvk_number=kvk_number)
        if vendor is None:
            raise VendorNotFoundException()

        new_app_exists = isinstance(
            self.application_service.get_one_vendor_application(
                vendor_id=vendor.id, application_name=application_name
            ),
            Application,
        )
        if new_app_exists:
            raise ApplicationAlreadyExistsException()

        new_application = ApplicationFactory.create_instance(
            application_name, application_version
        )
        vendor.applications.append(new_application)
        vendor_repository.update(vendor)

        return vendor

    def deregister_one_vendor_application(
        self, kvk_number: str, application_name: str
    ) -> Vendor:
        vendor_repository = self.vendor_service.get_vendors_repository()
        vendor = vendor_repository.find_one(kvk_number=kvk_number)
        if vendor is None:
            raise VendorNotFoundException()

        application = self.application_service.get_one_vendor_application(
            vendor_id=vendor.id, application_name=application_name
        )
        if application is None:
            raise ApplicationNotFoundException()

        for app in vendor.applications:
            if app.name == application.name and app.vendor_id == application.vendor_id:
                vendor.applications.remove(app)
                vendor_repository.update(vendor)
                break

        return vendor

    def get_all_vendor_applications(self, kvk_number: str) -> Sequence[Application]:
        application_repository = self.application_service.get_applications_repository()
        vendor = self.vendor_service.get_one_vendor(kvk_number=kvk_number)

        applications = application_repository.find_many(vendor_id=vendor.id)

        return applications

    def get_one_vendor_application(
        self, kvk_number: str, application_name: str
    ) -> Application:
        vendor = self.vendor_service.get_one_vendor(kvk_number=kvk_number)
        application = self.application_service.get_one_vendor_application(
            application_name=application_name, vendor_id=vendor.id
        )
        if application is None:
            raise ApplicationNotFoundException()

        return application
