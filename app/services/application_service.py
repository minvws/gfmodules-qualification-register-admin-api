from uuid import UUID

from app.db.db import Database
from app.db.db_session import DbSession
from app.db.entities.models import Application
from app.db.repository.applications_repository import ApplicationsRepository


class ApplicationService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_one_vendor_application(
        self, vendor_id: UUID, application_name: str
    ) -> Application | None:
        repository = self.get_applications_repository()
        application = repository.find_one(name=application_name, vendor_id=vendor_id)

        return application

    def get_applications_repository(self) -> ApplicationsRepository:
        repository_session = DbSession[ApplicationsRepository](
            engine=self.database.engine
        )
        return repository_session.get_repository(Application)
