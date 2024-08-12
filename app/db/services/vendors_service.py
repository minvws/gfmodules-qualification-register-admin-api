from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.repository.vendor_repository import VendorRepository
from app.factory.vendor_factory import VendorFactory
from app.db.entities.vendor import Vendor
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorAlreadyExistsException,
    VendorCannotBeDeletedException,
)
from app.schemas.meta.schema import Page
from app.schemas.vendor.mapper import map_vendor_entity_to_dto
from app.schemas.vendor.schema import VendorDto


class VendorService:
    @session_manager
    def get_one_by_kvk_number(
        self, kvk_number: str, vendor_repository: VendorRepository = get_repository()
    ) -> Vendor:
        vendor = vendor_repository.get(kvk_number=kvk_number)
        if vendor is None:
            raise VendorNotFoundException()

        return vendor

    @session_manager
    def get_one(
        self, vendor_id: UUID, vendor_repository: VendorRepository = get_repository()
    ) -> Vendor:
        vendor = vendor_repository.get(id=vendor_id)
        if vendor is None:
            raise VendorNotFoundException()

        return vendor

    @session_manager
    def add_one(
        self,
        kvk_number: str,
        trade_name: str,
        statutory_name: str,
        vendor_repository: VendorRepository = get_repository(),
    ) -> Vendor:
        vendor = vendor_repository.get(kvk_number=kvk_number)
        if vendor is not None:
            raise VendorAlreadyExistsException()

        new_vendor = VendorFactory.create_instance(
            trade_name=trade_name,
            statutory_name=statutory_name,
            kvk_number=kvk_number,
        )
        vendor_repository.create(new_vendor)

        return new_vendor

    @session_manager
    def remove_one(
        self, vendor_id: UUID, vendor_repository: VendorRepository = get_repository()
    ) -> Vendor:
        vendor = vendor_repository.get(id=vendor_id)
        if vendor is None:
            raise VendorNotFoundException()

        vendor_has_applications = self._vendor_has_applications(vendor)
        if vendor_has_applications:
            raise VendorCannotBeDeletedException()

        vendor_repository.delete(vendor)

        return vendor

    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        vendor_repository: VendorRepository = get_repository(),
    ) -> Page[VendorDto]:
        vendors = vendor_repository.get_many(limit=limit, offset=offset)
        total = vendor_repository.count()

        vendors_dto = [map_vendor_entity_to_dto(vendor) for vendor in vendors]
        return Page(items=vendors_dto, total=total, offset=offset, limit=limit)

    @staticmethod
    def _vendor_has_applications(vendor: Vendor) -> bool:
        return len(vendor.applications) > 0
