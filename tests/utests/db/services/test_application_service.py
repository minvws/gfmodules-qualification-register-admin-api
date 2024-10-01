from uuid import UUID

import pytest

from app.db.entities import Application
from app.db.entities import Vendor
from app.exceptions.app_exceptions import ApplicationNotFoundException
from app.db.services import ApplicationService
from app.schemas.application.mapper import map_application_entity_to_dto
from app.schemas.meta.schema import Page
from .utils import are_the_same_entity


def test_add_one_application(
    application: Application, application_service: ApplicationService
) -> None:
    assert are_the_same_entity(application_service.get_one(application.id), application)


def test_remove_one_application_by_id(
    application: Application, application_service: ApplicationService
) -> None:
    assert are_the_same_entity(
        application_service.get_one(application.id),
        application_service.remove_one(application.id),
    )
    with pytest.raises(ApplicationNotFoundException):
        application_service.get_one(application.id)


def test_remove_one_by_id_application_dont_exist(
    application_service: ApplicationService,
) -> None:
    with pytest.raises(
        ApplicationNotFoundException, match="404: Application not found"
    ):
        application_service.remove_one(UUID("1f5991fd-260d-4bd6-8889-b79e5e98a623"))


def test_remove_one_application_by_name(
    vendor: Vendor, application: Application, application_service: ApplicationService
) -> None:
    assert are_the_same_entity(
        application_service.get_one(application.id),
        application_service.remove_one_by_name(
            application_name=application.name,
            vendor_id=vendor.id,
        ),
    )
    with pytest.raises(ApplicationNotFoundException):
        application_service.get_one(application.id)


def test_remove_one_by_name_application_dont_exist(
    application_service: ApplicationService,
) -> None:
    with pytest.raises(
        ApplicationNotFoundException, match="404: Application not found"
    ):
        application_service.remove_one_by_name(
            "does not exist", UUID("1f5991fd-260d-4bd6-8889-b79e5e98a623")
        )


def test_applications_paginated(
    application: Application, application_service: ApplicationService
) -> None:
    assert application_service.get_paginated(limit=10, offset=0) == Page(
        items=[map_application_entity_to_dto(application)],
        limit=10,
        offset=0,
        total=1,
    )
