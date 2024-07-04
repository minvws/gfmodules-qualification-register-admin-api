from typing import Sequence
from uuid import UUID

from app.db.repository.vendors_repository import VendorsRepository
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.factory.vendor_factory import VendorFactory
from app.db.entities.vendor import Vendor
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorAlreadyExistsException,
    VendorCannotBeDeletedException,
)


class VendorService:
    def __init__(
        self,
        db_session_factory: DbSessionFactory,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.db_session_factory = db_session_factory
        self.repository_factory = repository_factory

    def get_one_by_kvk_number(self, kvk_number: str) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository = self.repository_factory.create(
            VendorsRepository, db_session
        )
        with db_session:
            vendor = vendor_repository.get(kvk_number=kvk_number)
            if vendor is None:
                raise VendorNotFoundException()

        return vendor

    def get_one(self, vendor_id: UUID) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository = self.repository_factory.create(
            VendorsRepository, db_session
        )
        with db_session:
            vendor = vendor_repository.get(id=vendor_id)
            if vendor is None:
                raise VendorNotFoundException()

        return vendor

    def get_all(self) -> Sequence[Vendor]:
        db_session = self.db_session_factory.create()
        vendor_repository = self.repository_factory.create(
            VendorsRepository, db_session
        )
        with db_session:
            vendors = vendor_repository.get_all()

        return vendors

    def add_one(self, kvk_number: str, trade_name: str, statutory_name: str) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository = self.repository_factory.create(
            VendorsRepository, db_session
        )
        with db_session:
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

    def remove_one(self, vendor_id: UUID) -> Vendor:
        db_session = self.db_session_factory.create()
        vendor_repository = self.repository_factory.create(
            VendorsRepository, db_session
        )
        with db_session:
            vendor = vendor_repository.get(id=vendor_id)
            if vendor is None:
                raise VendorNotFoundException()

            vendor_has_applications = self._vendor_has_applications(vendor)
            if vendor_has_applications:
                raise VendorCannotBeDeletedException()

            vendor_repository.delete(vendor)

        return vendor

    @staticmethod
    def _vendor_has_applications(vendor: Vendor) -> bool:
        return len(vendor.applications) > 0
