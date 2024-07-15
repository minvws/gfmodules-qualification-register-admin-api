from typing import Generator, Any

import inject
import pytest

from app.db.db import Database
from app.db.db_session import DbSession
from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.db.repository_factory import RepositoryFactory
from app.db.services.application_service import ApplicationService
from app.db.services.roles_service import RoleService
from app.db.services.system_type_service import SystemTypeService
from app.db.services.vendors_service import VendorService
from app.db.session_factory import DbSessionFactory
from app.factory.system_type_factory import SystemTypeFactory
from app.factory.vendor_factory import VendorFactory


@pytest.fixture()
def session() -> Generator[DbSession, Any, None]:
    db = Database("sqlite:///:memory:")
    db.generate_tables()
    session_factory = DbSessionFactory(db.engine)
    session = session_factory.create()

    repository_factory = RepositoryFactory()

    inject.configure(
        lambda binder: binder.bind(DbSessionFactory, session_factory).bind(  # type: ignore
            RepositoryFactory, repository_factory
        ),
        clear=True,
    )

    yield session


@pytest.fixture()
def vendor_service(session: DbSession) -> VendorService:
    return VendorService()


@pytest.fixture()
def role_service(session: DbSession) -> RoleService:
    return RoleService()


@pytest.fixture()
def system_type_service(session: DbSession) -> SystemTypeService:
    return SystemTypeService()


@pytest.fixture()
def application_service(session: DbSession) -> ApplicationService:
    return ApplicationService()


@pytest.fixture()
def mock_vendor() -> Vendor:
    return VendorFactory.create_instance(
        kvk_number="123456", trade_name="example", statutory_name="example"
    )


@pytest.fixture()
def mock_role() -> Role:
    return Role(
        name="example",
        description="example",
    )


@pytest.fixture()
def mock_system_type() -> SystemType:
    return SystemTypeFactory.create_instance(
        name="example",
        description="example",
    )
