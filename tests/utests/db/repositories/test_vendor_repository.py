import uuid
from typing import Sequence

import pytest
from gfmodules_python_shared.repository.exceptions import EntryNotFound
from gfmodules_python_shared.session.db_session import DbSession
from sqlalchemy.exc import InvalidRequestError


from app.db.entities.vendor import Vendor
from app.db.repository.vendor_repository import VendorRepository


@pytest.fixture()
def vendor_repository(session: DbSession) -> VendorRepository:
    return VendorRepository(db_session=session)


@pytest.fixture()
def mock_vendor() -> Vendor:
    return Vendor(kvk_number="example", trade_name="example", statutory_name="example")


class TestVendorRepository:

    def test_create_should_succeed_when_given_vendor_object(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        expected_vendor = mock_vendor

        vendor_repository.create(expected_vendor)

        actual_vendor = vendor_repository.get(id=expected_vendor.id)
        assert actual_vendor == expected_vendor
        assert vendor_repository.count() == 1

    def test_get_should_return_vendor_instance(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)
        actual_vendor = vendor_repository.get(id=mock_vendor.id)

        assert isinstance(actual_vendor, Vendor)

    def test_get_should_return_same_instance_when_given_different_properties(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        expected_vendor = mock_vendor

        vendor_repository.create(expected_vendor)
        actual_vendor_1 = vendor_repository.get(id=expected_vendor.id)
        actual_vendor_2 = vendor_repository.get(kvk_number=expected_vendor.kvk_number)

        assert expected_vendor == actual_vendor_1
        assert expected_vendor == actual_vendor_2

    def test_get_should_raise_exception_when_given_wrong_property(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)
        with pytest.raises(InvalidRequestError):
            vendor_repository.get(wrong_property=mock_vendor.trade_name)

    def test_get_should_return_none_when_given_wrong_property_value(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)
        wrong_id = uuid.uuid4()
        wrong_kvk_number = "wrong kvk number"

        actual_vendor_1 = vendor_repository.get(id=wrong_id)
        assert actual_vendor_1 is None

        actual_vendor_2 = vendor_repository.get(kvk_number=wrong_kvk_number)
        assert actual_vendor_2 is None

    def test_update_should_return_updated_vendor_values(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        new_kvk_number = "example 2"
        vendor_repository.create(mock_vendor)

        expected_vendor = vendor_repository.get(id=mock_vendor.id)
        # assertion to pass type-check
        assert isinstance(expected_vendor, Vendor)
        expected_vendor.kvk_number = new_kvk_number
        vendor_repository.update(expected_vendor)
        actual_vendor = vendor_repository.get(id=expected_vendor.id)

        assert expected_vendor == actual_vendor

    def test_update_should_return_a_vendor_instance(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        new_kvk_number = "example 2"
        vendor_repository.create(mock_vendor)
        new_vendor = vendor_repository.get(id=mock_vendor.id)

        # assertion to pass type-check
        assert isinstance(new_vendor, Vendor)
        new_vendor.kvk_number = new_kvk_number
        vendor_repository.update(new_vendor)
        updated_vendor = vendor_repository.get(id=new_vendor.id)

        assert updated_vendor == new_vendor
        assert isinstance(updated_vendor, Vendor)

    def test_delete_should_remove_vendor_instance(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)

        vendor_repository.delete(mock_vendor)
        expected_vendor = vendor_repository.get(id=mock_vendor.id)

        assert expected_vendor is None

    def test_get_or_fail_should_succeed_when_given_correct_properties(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        expected_vendor = mock_vendor

        vendor_repository.create(mock_vendor)
        actual_vendor = vendor_repository.get(id=expected_vendor.id)

        assert actual_vendor == expected_vendor

    def test_get_or_fail_should_raise_exception_when_given_wrong_property_value(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)
        wrong_kvk_number = "wrong kvk number"
        with pytest.raises(EntryNotFound):
            vendor_repository.get_or_fail(kvk_number=wrong_kvk_number)

    def test_get_or_fail_should_raise_exception_when_given_wrong_property(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)
        with pytest.raises(InvalidRequestError):
            vendor_repository.get_or_fail(wrong_property="wrong property")

    def test_get_many_should_return_all_entries_when_no_parameters_are_given(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        expected_vendors = [mock_vendor]

        vendor_repository.create(mock_vendor)
        actual_vendors = vendor_repository.get_many()

        assert actual_vendors == expected_vendors
        assert len(expected_vendors) == len(actual_vendors)

    def test_get_many_should_return_empty_list_when_no_entries_are_available(
        self, vendor_repository: VendorRepository
    ) -> None:
        expected_vendors: Sequence[Vendor] = []
        actual_vendors = vendor_repository.get_many()

        assert actual_vendors == expected_vendors
        assert len(expected_vendors) == len(actual_vendors)

    def test_count_should_return_zero_when_no_entries_are_available(
        self, vendor_repository: VendorRepository
    ) -> None:
        expected_count = vendor_repository.count()

        assert expected_count == 0

    def test_count_should_return_exact_number_of_entries_available(
        self, vendor_repository: VendorRepository, mock_vendor: Vendor
    ) -> None:
        vendor_repository.create(mock_vendor)

        expected_count = 1
        actual_count = vendor_repository.count()

        assert expected_count == actual_count
