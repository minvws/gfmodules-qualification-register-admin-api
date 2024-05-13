from app.db.entities.models import ApplicationVersion, Application


class ApplicationFactory:

    @staticmethod
    def create_instance(application_name: str, application_version: str) -> Application:
        new_application_version = ApplicationVersion(version=application_version)
        new_application = Application(name=application_name)
        new_application.versions.append(new_application_version)

        return new_application
