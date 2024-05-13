import inject


from app.db.db import Database
from app.config import get_config
from app.services.application_roles_service import ApplicationRolesService
from app.services.roles_service import RolesService
from app.services.vendors_service import VendorService

from app.services.application_service import ApplicationService
from app.services.vendor_application_service import VendorApplicationService


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(dsn=config.database.dsn)
    binder.bind(Database, db)

    application_service = ApplicationService(db)
    binder.bind(ApplicationService, application_service)

    vendors_service = VendorService(db)
    binder.bind(VendorService, vendors_service)

    vendor_application_service = VendorApplicationService(
        application_service, vendors_service
    )
    binder.bind(VendorApplicationService, vendor_application_service)

    roles_service = RolesService(db)
    binder.bind(RolesService, roles_service)

    application_roles_service = ApplicationRolesService(
        roles_service, application_service
    )
    binder.bind(ApplicationRolesService, application_roles_service)


def get_vendors_service() -> VendorService:
    return inject.instance(VendorService)


def get_application_service() -> ApplicationService:
    return inject.instance(ApplicationService)


def get_vendor_application_service() -> VendorApplicationService:
    return inject.instance(VendorApplicationService)


def get_roles_service() -> RolesService:
    return inject.instance(RolesService)


def get_application_roles_service() -> ApplicationRolesService:
    return inject.instance(ApplicationRolesService)


def get_database() -> Database:
    return inject.instance(Database)


if not inject.is_configured():
    inject.configure(container_config)
