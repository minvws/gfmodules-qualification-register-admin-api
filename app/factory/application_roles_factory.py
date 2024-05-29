from app.db.entities.application_role import ApplicationRole


class ApplicationRolesFactory:

    @staticmethod
    def create_instance() -> ApplicationRole:
        return ApplicationRole()
