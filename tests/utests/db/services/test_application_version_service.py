from uuid import UUID

import pytest

from app.db.entities import Application
from app.db.services import ApplicationService, ApplicationVersionService
from app.exceptions.app_exceptions import ApplicationVersionDeleteException
from .utils import are_the_same_entity


@pytest.fixture
def application_two_versions(
    application: Application,
    application_service: ApplicationService,
    application_version_service: ApplicationVersionService,
) -> Application:
    application_version_service.add_one(application.id, "v1.0.1")
    return application_service.get_one(application.id)


def test_add_application_version(
    application: Application,
    application_version_service: ApplicationVersionService,
    application_service: ApplicationService,
) -> None:
    assert all(
        are_the_same_entity(actual, expected)
        for expected, actual in zip(
            application_version_service.add_one(application.id, "v1.1.0"),
            application_service.get_one(application.id).versions,
        )
    )


def test_delete_application_version(
    application_two_versions: Application,
    application_version_service: ApplicationVersionService,
    application_service: ApplicationService,
) -> None:
    version, *_ = application_two_versions.versions
    assert all(
        are_the_same_entity(actual, expected)
        for expected, actual in zip(
            application_version_service.remove_one(
                application_id=application_two_versions.id,
                version_id=version.id,
            ),
            application_service.get_one(application_two_versions.id).versions,
        )
    )


def test_unassign_role_from_application(
    application: Application,
    application_version_service: ApplicationVersionService,
) -> None:
    with pytest.raises(
        ApplicationVersionDeleteException,
        match="409: Cannot delete version, application should at least contain one version",
    ):
        application_version_service.remove_one(
            application.id, UUID("69cfd9ea-0f8b-48a5-a01e-aea444e45b19")
        )


@pytest.mark.parametrize(
    "app, length",
    (
        pytest.param("application", 1, id="one system type"),
        pytest.param("application_two_versions", 2, id="two system types"),
    ),
)
def test_get_application_versions(
    app: str,
    length: int,
    application_service: ApplicationService,
    request: pytest.FixtureRequest,
) -> None:
    application = request.getfixturevalue(app)
    expected_versions = application.versions
    assert len(expected_versions) == length
    assert all(
        are_the_same_entity(actual, expected)
        for actual, expected in zip(
            application_service.get_one(application.id).versions, expected_versions
        )
    )
