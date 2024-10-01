from uuid import UUID

import pytest

from app.db.entities import Application
from app.db.services import (
    ApplicationService,
    ApplicationTypeService,
    SystemTypeService,
)
from app.exceptions.app_exceptions import (
    SystemTypeNotFoundException,
    SystemTypeNotUsedByApplicationException,
)
from tests.utests.db.services.utils import are_the_same_entity


@pytest.fixture
def application_two_service_types(
    application: Application,
    application_service: ApplicationService,
    application_type_service: ApplicationTypeService,
    system_type_service: SystemTypeService,
) -> Application:
    application_type_service.assign_system_type_to_application(
        application_id=application.id,
        system_type_id=system_type_service.add_one(
            name="example 2", description="some description"
        ).id,
    )
    return application_service.get_one(application.id)


@pytest.mark.parametrize(
    "app, length",
    (
        pytest.param("application", 1, id="one system type"),
        pytest.param("application_two_service_types", 2, id="two system types"),
    ),
)
def test_get_all_application_types(
    app: str,
    length: int,
    application_service: ApplicationService,
    request: pytest.FixtureRequest,
) -> None:
    application = request.getfixturevalue(app)
    expected_types = application.system_types
    assert len(expected_types) == length
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            application_service.get_one(application.id).system_types, expected_types
        )
    )


def test_assign_system_type_to_application(
    application: Application,
    application_service: ApplicationService,
    application_type_service: ApplicationTypeService,
    system_type_service: SystemTypeService,
) -> None:
    system_type = system_type_service.add_one(
        name="example 2", description="some description"
    )
    assert all(
        are_the_same_entity(actual, expected)
        for expected, actual in zip(
            application_type_service.assign_system_type_to_application(
                application_id=application.id, system_type_id=system_type.id
            ).system_types,
            application_service.get_one(application.id).system_types,
        )
    )


def test_unassign_system_type_from_application(
    application_two_service_types: Application,
    application_service: ApplicationService,
    application_type_service: ApplicationTypeService,
) -> None:
    application_type, *_ = application_two_service_types.system_types
    assert all(
        are_the_same_entity(actual, expected)
        for expected, actual in zip(
            application_type_service.unassign_system_type_to_application(
                application_id=application_two_service_types.id,
                system_type_id=application_type.system_type.id,
            ).system_types,
            application_service.get_one(application_two_service_types.id).system_types,
        )
    )


def test_unassign_non_existing_system_type_to_application(
    application_two_service_types: Application,
    application_type_service: ApplicationTypeService,
) -> None:
    with pytest.raises(
        SystemTypeNotFoundException,
        match="404: System type not found",
    ):
        application_type_service.unassign_system_type_to_application(
            application_id=application_two_service_types.id,
            system_type_id=UUID("cb81aff3-ec2f-4c12-ac88-bea619313ffb"),
        )


def test_unassign_system_type_to_application_mismatch(
    application: Application,
    application_type_service: ApplicationTypeService,
    system_type_service: SystemTypeService,
) -> None:
    with pytest.raises(
        SystemTypeNotUsedByApplicationException,
        match="409: System type does not exist in application",
    ):
        application_type_service.unassign_system_type_to_application(
            application_id=application.id,
            system_type_id=system_type_service.add_one(
                name="example 3", description="some description"
            ).id,
        )
