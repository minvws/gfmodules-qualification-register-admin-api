from uuid import UUID

import pytest

from app.db.entities import Application
from app.db.entities import Vendor
from app.db.services import VendorService
from app.exceptions.app_exceptions import (
    VendorCannotBeDeletedException,
    VendorNotFoundException,
)
from app.schemas.meta.schema import Page
from app.schemas.vendor.mapper import map_vendor_entity_to_dto
from .utils import are_the_same_entity


def test_add_one_should_succeed(vendor_service: VendorService) -> None:
    vendor = vendor_service.add_one(
        kvk_number="12456",
        trade_name="example vendor",
        statutory_name="example vendor bv",
    )
    actual_vendor = vendor_service.get_one_by_kvk_number(vendor.kvk_number)
    are_the_same_entity(actual_vendor, vendor)


def test_get_one_by_id_should_succeed(
    vendor: Vendor, vendor_service: VendorService
) -> None:
    actual_vendor = vendor_service.get_one(vendor.id)
    are_the_same_entity(actual_vendor, vendor)


def test_delete_one_vendor_by_id_should_succeed(
    vendor: Vendor, vendor_service: VendorService
) -> None:
    actual_vendor = vendor_service.remove_one(vendor.id)
    are_the_same_entity(actual_vendor, vendor)

    with pytest.raises(VendorNotFoundException, match="404: Vendor not found"):
        vendor_service.get_one(vendor.id)


def test_delete_non_existing_vendor_by_id_should_raise(
    vendor_service: VendorService,
) -> None:
    with pytest.raises(VendorNotFoundException, match="404: Vendor not found"):
        vendor_service.get_one(UUID("2c907623-a8e7-4bdd-8fd5-3eb3feb16d35"))


def test_get_vendors_paginated_should_succeed(
    vendor: Vendor, vendor_service: VendorService
) -> None:
    assert vendor_service.get_paginated(limit=10, offset=0) == Page(
        items=[map_vendor_entity_to_dto(vendor)], limit=10, offset=0, total=1
    )


def test_delete_one_should_raise_exception_when_vendor_has_applications(
    vendor: Vendor,
    application: Application,
    vendor_service: VendorService,
) -> None:
    with pytest.raises(
        VendorCannotBeDeletedException, match="405: Vendor cannot be deleted"
    ):
        vendor_service.remove_one(vendor_id=vendor.id)
