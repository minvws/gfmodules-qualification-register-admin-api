from typing import Sequence, List
from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.repository import RoleRepository, SystemTypeRepository, VendorRepository
from app.db.entities import Application
from app.db.repository import ApplicationRepository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    ApplicationAlreadyExistsException,
)
from app.factory import ApplicationFactory
from app.schemas.application.mapper import map_application_entity_to_dto
from app.schemas.application.schema import ApplicationDto
from app.schemas.meta.schema import Page


class ApplicationService:
    @session_manager
    def get_by_vendor_id(
        self, vendor_id: UUID, *, vendor_repository: VendorRepository = get_repository()
    ) -> Sequence[Application]:
        vendor = vendor_repository.get_or_fail(id=vendor_id)
        return vendor.applications

    @session_manager
    def get_one(
        self,
        application_id: UUID,
        *,
        application_repository: ApplicationRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(id=application_id)
        if application is None:
            raise ApplicationNotFoundException()

        return application

    @session_manager
    def remove_one(
        self,
        application_id: UUID,
        *,
        application_repository: ApplicationRepository = get_repository(),
    ) -> Application:
        application = self.get_one(application_id)
        if application is None:
            raise ApplicationNotFoundException()

        application_repository.delete(application)
        return application

    @session_manager
    def remove_one_by_name(
        self,
        application_name: str,
        vendor_id: UUID,
        *,
        application_repository: ApplicationRepository = get_repository(),
    ) -> Application:
        application = application_repository.get(
            name=application_name, vendor_id=vendor_id
        )
        if application is None:
            raise ApplicationNotFoundException()

        application_repository.delete(application)
        return application

    @session_manager
    def add_one(
        self,
        vendor_id: UUID,
        application_name: str,
        version: str,
        role_names: List[str],
        system_type_names: List[str],
        *,
        application_repository: ApplicationRepository = get_repository(),
        vendor_repository: VendorRepository = get_repository(),
        system_type_repository: SystemTypeRepository = get_repository(),
        roles_repository: RoleRepository = get_repository(),
    ) -> Application:
        vendor = vendor_repository.get_or_fail(id=vendor_id)

        system_types = system_type_repository.get_by_property_exact(
            "name", system_type_names
        )

        roles = roles_repository.get_by_property_exact("name", role_names)

        application = application_repository.get(
            name=application_name, vendor_id=vendor.id
        )
        if application is not None:
            raise ApplicationAlreadyExistsException()

        new_application = ApplicationFactory.create_instance(
            application_name=application_name,
            application_version=version,
            vendor=vendor,
            application_roles=roles,
            application_types=system_types,
        )
        application_repository.create(new_application)

        return new_application

    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        *,
        application_repository: ApplicationRepository = get_repository(),
    ) -> Page[ApplicationDto]:
        applications = application_repository.get_many(limit=limit, offset=offset)
        dto = [map_application_entity_to_dto(app) for app in applications]
        total = application_repository.count()

        return Page(items=dto, limit=limit, offset=offset, total=total)
