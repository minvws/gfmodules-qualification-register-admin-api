from typing import Sequence
from uuid import UUID

from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
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
    ) -> None:
        self.role_service = role_service
        self.system_type_service = system_type_service
        self.db_session_factory = db_session_factory

    def get_all_applications(self) -> Sequence[Application]:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        session = db_session.session
        with session:
            applications = application_repository.find_many()

        return applications

    def get_one_application_by_id(self, application_id: UUID) -> Application:
        db_session = self.db_session_factory.create()
        repository: ApplicationsRepository = db_session.get_repository(Application)
        session = db_session.session
        with session:
            application = repository.find_one(id=application_id)
            if application is None:
                raise ApplicationNotFoundException()

        return application

    def delete_one_application_by_id(self, application_id: UUID) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        session = db_session.session
        with session:
            application = self.get_one_application_by_id(application_id)
            if application is None:
                raise ApplicationNotFoundException()

            application_repository.delete(application)
        return application

    def delete_one_application_by_name(
        self, application_name: str, vendor_id: UUID
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        session = db_session.session
        with session:
            application = application_repository.find_one(
                name=application_name, vendor_id=vendor_id
            )
            if application is None:
                raise ApplicationNotFoundException()

            application_repository.delete(application)
        return application

    def add_one_application(
        self,
        vendor: Vendor,
        application_name: str,
        version: str,
        roles: Sequence[Role],
        system_types: Sequence[SystemType],
    ) -> Application:
        db_session = self.db_session_factory.create()
        application_repository: ApplicationsRepository = db_session.get_repository(
            Application
        )
        session = db_session.session
        with session:
            application = application_repository.find_one(
                name=application_name, vendor_id=vendor.id
            )
            if application is not None:
                raise ApplicationAlreadyExistsException()

            new_application = ApplicationFactory.create_rich_instance(
                application_name=application_name,
                application_version=version,
                vendor=vendor,
                application_roles=roles,
                application_types=system_types,
            )
            application_repository.create(new_application)

        return new_application
