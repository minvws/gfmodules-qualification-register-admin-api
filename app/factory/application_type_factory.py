from app.db.entities.application_type import ApplicationType


class ApplicationTypeFactory:

    @staticmethod
    def create_instance() -> ApplicationType:
        return ApplicationType()
