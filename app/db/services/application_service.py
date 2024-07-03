from typing import Sequence
from uuid import UUID

from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.db.repository_factory import RepositoryFactory
from app.db.session_factory import DbSessionFactory
from app.db.entities.application import Application
from app.db.entities.role import Role
from app.db.repository.applications_repository import ApplicationsRepository
from app.exceptions.app_exceptions import (
    ApplicationNotFoundException,
    ApplicationAlreadyExistsException,
)
from app.factory.application_factory import ApplicationFactory
from app.db.services.roles_service import RolesService
from app.db.services.system_type_service import SystemTypeService


class ApplicationService:
    def __init__(
        self,
        role_service: RolesService,
        system_type_service: SystemTypeService,
        db_session_factory: DbSessionFactory,
        repository_factory: RepositoryFactory,
    ) -> None:
        self.role_service = role_service
        self.system_type_service = system_type_service
        self.db_session_factory = db_session_factory
        self.repository_factory = repository_factory

    def get_all(self) -> Sequence[Application]:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        with db_session:
            applications = application_repository.get_all()

        return applications

    def get_one(self, application_id: UUID) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        with db_session:
            application = application_repository.get(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

        return application

    def remove_one(self, application_id: UUID) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        with db_session:
            application = self.get_one(application_id)
            if application is None:
                raise ApplicationNotFoundException()

            application_repository.delete(application)
        return application

    def remove_one_by_name(
        self, application_name: str, vendor_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        with db_session:
            application = application_repository.get(
                name=application_name, vendor_id=vendor_id
            )
            if application is None:
                raise ApplicationNotFoundException()

            application_repository.delete(application)
        return application

    def add_one(
        self,
        vendor: Vendor,
        application_name: str,
        version: str,
        roles: Sequence[Role],
        system_types: Sequence[SystemType],
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository = self.repository_factory.create(
            ApplicationsRepository, db_session
        )
        with db_session:
            application = application_repository.get(
                name=application_name, vendor_id=vendor.id
            )
            if application is not None:
                raise ApplicationAlreadyExistsException()

            new_application = ApplicationFactory.create_instance(
                application_name=application_name,
                application_version=version,
                vendor=db_session.merge(vendor),
                application_roles=[db_session.merge(role) for role in roles],
                application_types=[
                    db_session.merge(system_type) for system_type in system_types
                ],
            )
            application_repository.create(new_application)

        return new_application
