from typing import Sequence
from uuid import UUID

from app.db.session_factory import DbSessionFactory
from app.factory.vendor_factory import VendorFactory
from app.db.entities.vendor import Vendor
from app.db.repository.vendors_repository import VendorsRepository
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorAlreadyExistsException,
    VendorCannotBeDeletedException,
)


class VendorService:
    def __init__(self, db_session_factory: DbSessionFactory) -> None:
        self.db_session_factory = db_session_factory

    def get_one_vendor_by_kvk_number(self, kvk_number: str) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendor = vendor_repository.find_one(kvk_number=kvk_number)
            if vendor is None:
                raise VendorNotFoundException()

        return vendor

    def get_one_vendor_by_id(self, vendor_id: UUID) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendor = vendor_repository.find_one(id=vendor_id)
            if vendor is None:
                raise VendorNotFoundException()

        return vendor

    def get_all_vendors(self) -> Sequence[Vendor]:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendors = vendor_repository.find_all()

        return vendors

    def add_one_vendor(
        self, kvk_number: str, trade_name: str, statutory_name: str
    ) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendor = vendor_repository.find_one(kvk_number=kvk_number)
            if vendor is not None:
                raise VendorAlreadyExistsException()

            new_vendor = VendorFactory.create_instance(
                trade_name=trade_name,
                statutory_name=statutory_name,
                kvk_number=kvk_number,
            )
            session.add(new_vendor)
            session.commit()
            session.refresh(new_vendor)

        return new_vendor

    def delete_one_vendor_by_kvk_number(self, kvk_number: str) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendor = vendor_repository.find_one(kvk_number=kvk_number)
            if vendor is None:
                raise VendorNotFoundException()

            vendor_cannot_be_deleted = self._validate_vendor_deletion(vendor)
            if vendor_cannot_be_deleted:
                raise VendorCannotBeDeletedException()

            vendor_repository.delete(vendor)

        return vendor

    def delete_one_vendor_by_id(self, vendor_id: UUID) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository: VendorsRepository = db_session.get_repository(Vendor)
        session = db_session.session
        with session:
            vendor = vendor_repository.find_one(id=vendor_id)
            if vendor is None:
                raise VendorNotFoundException()

            vendor_cannot_be_deleted = self._validate_vendor_deletion(vendor)
            if vendor_cannot_be_deleted:
                raise VendorCannotBeDeletedException()

            vendor_repository.delete(vendor)

        return vendor

    @staticmethod
    def _validate_vendor_deletion(vendor: Vendor) -> bool:
        return len(vendor.applications) > 0
