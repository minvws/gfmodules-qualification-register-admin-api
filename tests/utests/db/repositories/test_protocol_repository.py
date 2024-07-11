import uuid

import pytest
from sqlalchemy.exc import InvalidRequestError

from app.db.db_session import DbSession
from app.db.entities.protocol import Protocol
from app.db.repository.exception import EntryNotFound
from app.db.repository.protocol_repository import ProtocolRepository


@pytest.fixture()
def protocol_repository(session: DbSession) -> ProtocolRepository:
    return ProtocolRepository(db_session=session)


@pytest.fixture()
def mock_protocol() -> Protocol:
    return Protocol(
        protocol_type="Directive",
        name="example",
        description="example",
    )


@pytest.fixture()
def mock_protocol_2() -> Protocol:
    return Protocol(
        protocol_type="Directive",
        name="example",
        description="example",
    )


class TestProtocolRepository:

    def test_create_should_succeed_when_given_a_valid_protocol_object(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        expected_protocol = mock_protocol

        protocol_repository.create(mock_protocol)
        actual_protocol = protocol_repository.get(id=mock_protocol.id)

        assert actual_protocol == expected_protocol
        assert protocol_repository.count() == 1

    def test_create_should_succeed_when_given_a_different_variant_of_object(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        expected_protocol = mock_protocol
        expected_protocol.protocol_type = "InformationStandard"

        protocol_repository.create(mock_protocol)
        actual_protocol = protocol_repository.get(id=mock_protocol.id)

        assert actual_protocol == expected_protocol

    def test_create_should_raise_exception_when_given_a_non_valid_protocol_type(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        expected_protocol = mock_protocol
        with pytest.raises(ValueError):
            expected_protocol.protocol_type = "InvalidProtocolType"  # type: ignore
            protocol_repository.create(mock_protocol)

    def test_get_should_succeed_when_given_a_valid_properties(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        expected_protocol = mock_protocol
        protocol_repository.create(mock_protocol)

        actual_protocol = protocol_repository.get(id=mock_protocol.id)

        assert actual_protocol == expected_protocol

    def test_get_should_return_none_when_entry_is_not_found(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)

        actual_protocol = protocol_repository.get(name="some name")

        assert actual_protocol is None

    def test_get_should_raise_exception_when_given_a_non_valid_property(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)

        with pytest.raises(InvalidRequestError):
            protocol_repository.get(wrong_property="some property")

    def test_update_should_succeed_when_modifying_correct_properties(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)
        expected_protocol = protocol_repository.get(id=mock_protocol.id)
        # assertion for type-checking
        assert isinstance(expected_protocol, Protocol)
        expected_protocol.name = "some name"
        expected_protocol.protocol_type = "InformationStandard"

        protocol_repository.update(expected_protocol)
        actual_protocol = protocol_repository.get(id=mock_protocol.id)

        assert expected_protocol == actual_protocol

    def test_update_should_raise_exception_when_given_a_non_valid_protocol_object(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)
        expected_protocol = protocol_repository.get(id=mock_protocol.id)
        # assertion for type-checking
        assert isinstance(expected_protocol, Protocol)

        with pytest.raises(ValueError):
            expected_protocol.protocol_type = "InvalidProtocolType"  # type: ignore
            protocol_repository.update(expected_protocol)

    def test_delete_should_succeed_when_given_a_valid_protocol_object(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)

        protocol_repository.delete(mock_protocol)
        actual_protocol = protocol_repository.get(id=mock_protocol.id)

        assert actual_protocol is None

    def test_delete_should_raise_exception_when_given_a_non_valid_protocol_object(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        with pytest.raises(InvalidRequestError):
            protocol_repository.delete(mock_protocol)

    def test_get_or_fail_should_succeed_when_given_a_valid_property(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        expected_protocol = mock_protocol
        protocol_repository.create(mock_protocol)

        actual_protocol = protocol_repository.get_or_fail(id=mock_protocol.id)

        assert actual_protocol == expected_protocol

    def test_get_or_fail_should_raise_exception_when_given_a_non_existent_property(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)
        wrong_id = uuid.uuid4()

        with pytest.raises(EntryNotFound):
            protocol_repository.get_or_fail(id=wrong_id)

    def test_get_many_should_succeed_when_given_a_valid_property(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        expected_protocols = [mock_protocol, mock_protocol_2]
        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)

        actual_protocols = protocol_repository.get_many(name="example")

        assert actual_protocols == expected_protocols
        assert protocol_repository.count() == 2

    def test_get_many_should_return_an_empty_list_when_filter_condition_is_not_met(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)

        actual_protocols = protocol_repository.get_many(name="wrong name")

        assert actual_protocols == []

    def test_count_should_return_exact_number_of_entries_in_data_base(
        self, protocol_repository: ProtocolRepository, mock_protocol: Protocol
    ) -> None:
        protocol_repository.create(mock_protocol)

        assert protocol_repository.count() == 1

    def test_get_by_property_should_return_entries_matching_given_parameters(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        # modify name to add a different property for the test
        mock_protocol_2.name = "example 2"

        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)
        expected_protocols = [mock_protocol, mock_protocol_2]

        actual_protocols = protocol_repository.get_by_property(
            "name", ["example", "example 2"]
        )

        assert actual_protocols == expected_protocols

    def test_get_by_property_should_return_empty_list_when_filter_condition_is_not_met(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)

        actual_protocols = protocol_repository.get_by_property("name", ["wrong name"])

        assert actual_protocols == []

    def test_get_by_property_should_raise_exception_when_given_a_wrong_property(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)

        with pytest.raises(AttributeError):
            protocol_repository.get_by_property("wrong_name", ["example"])

    def get_by_property_exact_should_succeed_when_given_a_valid_property(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)
        expected_protocols = [mock_protocol, mock_protocol_2]

        actual_protocols = protocol_repository.get_by_property_exact(
            "name", ["example"]
        )

        assert expected_protocols == actual_protocols

    def get_by_property_exact_should_raise_exception_when_no_match_is_found(
        self,
        protocol_repository: ProtocolRepository,
        mock_protocol: Protocol,
        mock_protocol_2: Protocol,
    ) -> None:
        protocol_repository.create(mock_protocol)
        protocol_repository.create(mock_protocol_2)

        with pytest.raises(EntryNotFound):
            protocol_repository.get_by_property_exact("name", ["example 2"])
