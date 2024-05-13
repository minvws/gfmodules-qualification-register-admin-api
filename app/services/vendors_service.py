from typing import Sequence


from app.factory.vendor_factory import VendorFactory
from app.db.db import Database
from app.db.db_session import DbSession
from app.db.entities.models import Vendor
from app.db.repository.vendors_repository import VendorsRepository
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
)


class VendorService:
    def __init__(
        self,
        database: Database,
    ) -> None:
        self.database = database

    def get_one_vendor(self, kvk_number: str) -> Vendor:
        session = self.get_vendors_repository()
        vendor = session.find_one(kvk_number=kvk_number)
        if vendor is None:
            raise VendorNotFoundException()

        return vendor

    def get_all_vendors(self) -> Sequence[Vendor]:
        session = self.get_vendors_repository()
        vendors = session.find_all()

        return vendors

    def add_one_vendor(
        self, kvk_number: str, trade_name: str, statutory_name: str
    ) -> Vendor:
        repository = self.get_vendors_repository()
        new_vendor = VendorFactory.create_instance(
            trade_name=trade_name, statutory_name=statutory_name, kvk_number=kvk_number
        )
        updated_vendor = repository.create(new_vendor)

        return updated_vendor

    def delete_one_vendor(self, kvk_number: str) -> Vendor:
        repository = self.get_vendors_repository()
        vendor = repository.find_one(kvk_number=kvk_number)
        if vendor is None:
            raise VendorNotFoundException()

        repository.delete(vendor)
        return vendor

    def get_vendors_repository(self) -> VendorsRepository:
        vendors_session = DbSession[VendorsRepository](engine=self.database.engine)
        return vendors_session.get_repository(Vendor)
