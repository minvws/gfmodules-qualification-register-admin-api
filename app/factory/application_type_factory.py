from app.db.entities.application import Application
from app.db.entities.application_type import ApplicationType
from app.db.entities.system_type import SystemType


class ApplicationTypeFactory:

    @staticmethod
    def create_instance(
        application: Application, system_type: SystemType
    ) -> ApplicationType:
        """
        Creates a new rich instance of ApplicationType with parent Application and child
        System type assigned
        """
        new_instance = ApplicationType()
        new_instance.application = application
        new_instance.system_type = system_type
        return new_instance
