from uuid import UUID

import pytest

from app.db.entities.application import Application
from app.db.services import (
    ApplicationRolesService,
    ApplicationService,
    RoleService,
)
from app.exceptions.app_exceptions import (
    ApplicationRoleDeleteException,
    RoleNotFoundException,
)


@pytest.fixture
def application_two_roles(
    role_service: RoleService,
    application_service: ApplicationService,
    application: Application,
    application_role_service: ApplicationRolesService,
) -> Application:
    role = role_service.add_one("another example role", description="some description")
    application_role_service.assign_role_to_application(
        application_id=application.id, role_id=role.id
    )
    return application_service.get_one(application.id)


def test_assign_role_to_application(
    role_service: RoleService,
    application_service: ApplicationService,
    application_role_service: ApplicationRolesService,
    application: Application,
) -> None:
    expected_role = role_service.add_one(
        "new example role", description="some description"
    )
    updated_app = application_role_service.assign_role_to_application(
        application_id=application.id, role_id=expected_role.id
    )
    expected_roles = [role.to_dict() for role in updated_app.roles]
    actual_roles = [
        role.to_dict() for role in application_service.get_one(application.id).roles
    ]
    assert expected_roles == actual_roles


def test_unassign_role_from_application(
    application_service: ApplicationService,
    application_role_service: ApplicationRolesService,
    application_two_roles: Application,
) -> None:
    role_id = application_two_roles.roles[-1].role_id
    application_role_service.unassign_role_from_application(
        application_id=application_two_roles.id, role_id=role_id
    )
    assert role_id not in [
        application_role.role_id
        for application_role in application_service.get_one(
            application_two_roles.id
        ).roles
    ]


def test_unassign_non_existing_role_from_application(
    application_role_service: ApplicationRolesService,
    application_two_roles: Application,
) -> None:
    with pytest.raises(
        RoleNotFoundException,
        match="404: Role not found",
    ):
        application_role_service.unassign_role_from_application(
            application_id=application_two_roles.id,
            role_id=UUID("cb81aff3-ec2f-4c12-ac88-bea619313ffb"),
        )


# WARNING: This should raise role not found
# even though there is only one role assign,
# since we are removing non-existing role
def test_unassign_last_role_from_application(
    application_role_service: ApplicationRolesService,
    application: Application,
) -> None:
    with pytest.raises(
        ApplicationRoleDeleteException,
        match="Cannot delete role, application should at least contain one role",
    ):
        application_role_service.unassign_role_from_application(
            application_id=application.id,
            role_id=UUID("cb81aff3-ec2f-4c12-ac88-bea619313ffb"),
        )
