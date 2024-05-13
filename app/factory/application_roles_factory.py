
from app.db.entities.models import ApplicationRole


class ApplicationRolesFactory:

    @staticmethod
    def create_instance() -> ApplicationRole:
        return ApplicationRole()
