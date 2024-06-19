from app.db.entities.application import Application
from app.db.entities.application_role import ApplicationRole
from app.db.entities.role import Role


class ApplicationRolesFactory:

    @staticmethod
    def create_instance(application: Application, role: Role) -> ApplicationRole:
        """
        Creates a new instance of Application Role with parent Application and child Role
        assigned
        """
        new_instance = ApplicationRole()
        new_instance.application = application
        new_instance.role = role
        return new_instance
