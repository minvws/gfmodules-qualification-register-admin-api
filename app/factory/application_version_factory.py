from app.db.entities.application_version import ApplicationVersion


class ApplicationVersionFactory:
    @staticmethod
    def create_instance(version: str) -> ApplicationVersion:
        return ApplicationVersion(version=version)
