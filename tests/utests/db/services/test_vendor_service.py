import pytest

from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.exceptions.app_exceptions import (
    VendorNotFoundException,
    VendorCannotBeDeletedException,
)
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RoleService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.schemas.meta.schema import Page
from app.schemas.vendor.mapper import map_vendor_entity_to_dto


class TestVendorCRUD:
    def test_add_one_should_succeed(
        self, mock_vendor: Vendor, vendor_service: VendorService
    ) -> None:
        # act
        expected_vendor = vendor_service.add_one(
            kvk_number=mock_vendor.kvk_number,
            trade_name=mock_vendor.trade_name,
            statutory_name=mock_vendor.statutory_name,
        )
        actual_vendor = vendor_service.get_one_by_kvk_number(expected_vendor.kvk_number)

        assert (
            expected_vendor.__table__.columns.keys()
            == actual_vendor.__table__.columns.keys()
        )

        for key in actual_vendor.__table__.columns.keys():
            getattr(expected_vendor, key)
            assert getattr(actual_vendor, key) == getattr(expected_vendor, key)

    def test_get_one_by_id_should_succeed(
        self, mock_vendor: Vendor, vendor_service: VendorService
    ) -> None:
        # act
        expected_vendor = vendor_service.add_one(
            kvk_number=mock_vendor.kvk_number,
            trade_name=mock_vendor.trade_name,
            statutory_name=mock_vendor.statutory_name,
        )

        actual_vendor = vendor_service.get_one(expected_vendor.id)

        # assert
        assert (
            expected_vendor.__table__.columns.keys()
            == actual_vendor.__table__.columns.keys()
        )

        for key in actual_vendor.__table__.columns.keys():
            print(getattr(actual_vendor, key))
            getattr(expected_vendor, key)
            assert getattr(actual_vendor, key) == getattr(expected_vendor, key)

    def test_delete_one_vendor_by_id_should_succeed(
        self, mock_vendor: Vendor, vendor_service: VendorService
    ) -> None:
        # act
        expected_vendor = vendor_service.add_one(
            kvk_number=mock_vendor.kvk_number,
            trade_name=mock_vendor.trade_name,
            statutory_name=mock_vendor.statutory_name,
        )
        actual_vendor = vendor_service.remove_one(expected_vendor.id)

        # assert
        assert (
            expected_vendor.__table__.columns.keys()
            == actual_vendor.__table__.columns.keys()
        )

        for key in actual_vendor.__table__.columns.keys():
            print(getattr(actual_vendor, key))
            getattr(expected_vendor, key)
            assert getattr(actual_vendor, key) == getattr(expected_vendor, key)

        with pytest.raises(VendorNotFoundException):
            vendor_service.get_one(expected_vendor.id)

    def test_get_vendors_paginated_should_succeed(
        self, mock_vendor: Vendor, vendor_service: VendorService
    ) -> None:
        mock_vendor = vendor_service.add_one(
            kvk_number=mock_vendor.kvk_number,
            trade_name=mock_vendor.trade_name,
            statutory_name=mock_vendor.statutory_name,
        )
        expected_vendors = vendor_service.get_paginated(limit=10, offset=0)
        actual_vendors = Page(
            items=[map_vendor_entity_to_dto(mock_vendor)], limit=10, offset=0, total=1
        )

        assert expected_vendors == actual_vendors

    def test_delete_one_should_raise_exception_when_vendor_has_applications(
        self,
        mock_vendor: Vendor,
        mock_role: Role,
        mock_system_type: SystemType,
        role_service: RoleService,
        system_type_service: SystemTypeService,
        application_service: ApplicationService,
        vendor_service: VendorService,
    ) -> None:
        vendor = vendor_service.add_one(
            kvk_number=mock_vendor.kvk_number,
            trade_name=mock_vendor.trade_name,
            statutory_name=mock_vendor.statutory_name,
        )
        role_service.add_one(name=mock_role.name, description=mock_role.description)
        system_type_service.add_one(
            name=mock_system_type.name, description=mock_system_type.description
        )

        application_service.add_one(
            vendor_id=vendor.id,
            application_name="example app",
            version="1.0.0",
            system_type_names=["example"],
            role_names=["example"],
        )

        with pytest.raises(VendorCannotBeDeletedException):
            vendor_service.remove_one(vendor_id=vendor.id)
