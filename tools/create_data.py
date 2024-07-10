import random
import time
import uuid
from random import randint
from typing import Sequence, List

from sqlalchemy import TIMESTAMP, select
from sqlalchemy.orm import Session

from app.config import get_config
from app.db.db import Database
from app.db.entities.application import Application
from app.db.entities.application_role import ApplicationRole
from app.db.entities.application_type import ApplicationType
from app.db.entities.application_version import ApplicationVersion
from app.db.entities.application_version_qualification import (
    ProtocolApplicationQualification,
)
from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.entities.healthcare_provider_application_version import (
    HealthcareProviderApplicationVersion,
)
from app.db.entities.healthcare_provider_qualification import (
    HealthcareProviderQualification,
)
from app.db.entities.protocol import Protocol, ProtocolTypes
from app.db.entities.protocol_version import ProtocolVersion
from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from app.db.repository.application_repository import ApplicationRepository
from app.db.repository.role_repository import RoleRepository
from app.db.repository.vendor_repository import VendorRepository
from app.db.session_factory import DbSessionFactory
from faker import Faker

import argparse

parser = argparse.ArgumentParser("Data generation")
parser.add_argument(
    "-c",
    "--count",
    metavar="c",
    required=True,
    dest="count",
    help="A global number to give a indication of how many entities you want.",
    type=int,
)
args = parser.parse_args()

count = args.count

config = get_config()

db = Database(dsn=config.database.dsn)

session_factory = DbSessionFactory(db.engine)

fake = Faker("nl_nl")


def create_versions(count: int) -> List[str]:
    _versions = []
    for i in range(count):
        for j in range(count):
            for k in range(count):
                _versions.append(f"{i}.{j}.{k}")
    return _versions


versions = create_versions(9)


def create_roles(session: Session):
    role_names = ["role a", "role b", "role c", "role d", "role e", "role f"]
    return [create_role(session, name) for name in role_names]


def create_system_types(session: Session):
    system_types = [
        "system type a",
        "system type b",
        "system type c",
        "system type d",
        "system type e",
    ]
    return [create_system_type(session, name) for name in system_types]


def create_role(session: Session, name: str) -> Role:
    existing_role = session.scalars(select(Role).filter_by(name=name)).first()
    return existing_role if existing_role is not None else Role(name=name)


def create_system_type(session: Session, name: str) -> SystemType:
    existing_system_type = session.scalars(
        select(SystemType).filter_by(name=name)
    ).first()
    return (
        existing_system_type
        if existing_system_type is not None
        else SystemType(name=name)
    )


def create_applications(
    count: int,
    roles: List[Role],
    system_types: List[SystemType],
    protocols: List[Protocol],
    healthcare_providers: List[HealthcareProvider],
) -> Sequence[Application]:
    return [
        create_application(roles, system_types, protocols, healthcare_providers)
        for _ in range(count)
    ]


def create_application(
    roles: List[Role],
    system_types: List[SystemType],
    protocols: List[Protocol],
    healthcare_providers: List[HealthcareProvider],
) -> Application:
    _versions = random.sample(versions, min(random.randint(1, 3), len(versions)))

    return Application(
        id=uuid.uuid4(),
        name=fake.catch_phrase(),
        created_at=fake.date_time(),
        modified_at=fake.date_time(),
        roles=[ApplicationRole(role=role) for role in random.sample(roles, 2)],
        system_types=[
            ApplicationType(system_type=system_type)
            for system_type in random.sample(system_types, 2)
        ],
        versions=[
            ApplicationVersion(
                version=version,
                qualified_protocol_versions=[
                    ProtocolApplicationQualification(
                        protocol_version=random.choice(
                            random.choice(protocols).versions
                        ),
                        qualification_date=fake.date_time(),
                    )
                ],
                healthcare_providers=[
                    HealthcareProviderApplicationVersion(
                        healthcare_provider=hpav,
                        created_at=fake.date_time(),
                        modified_at=fake.date_time(),
                    )
                    for hpav in random.sample(
                        healthcare_providers,
                        min(random.randint(1, 3), len(healthcare_providers)),
                    )
                ],
            )
            for version in _versions
        ],
    )


def create_application_version(version) -> ApplicationVersion:
    return ApplicationVersion(
        id=uuid.uuid4(),
        created_at=fake.date_time(),
        modified_at=fake.date_time(),
        version=version,
    )


def create_vendors(
    count: int, roles: List[Role], system_types: List[SystemType]
) -> Sequence[Vendor]:
    return [create_vendor(roles, system_types) for _ in range(count)]


def create_vendor(
    roles: List[Role],
    system_types: List[SystemType],
    protocols: List[Protocol],
    healthcare_providers: List[HealthcareProvider],
) -> Vendor:
    company_name = fake.company()
    return Vendor(
        id=uuid.uuid4(),
        kvk_number=str(randint(1_000_000, 9_999_999)),
        trade_name=company_name,
        statutory_name=company_name + " B.V.",
        created_at=fake.date_time(),
        modified_at=fake.date_time(),
        applications=list(
            create_applications(
                randint(2, 5), roles, system_types, protocols, healthcare_providers
            )
        ),
    )


def create_protocols(count: int) -> List[Protocol]:
    _versions = random.sample(versions, 3)
    return [
        Protocol(
            id=uuid.uuid4(),
            name=fake.name(),
            protocol_type=random.choice(list(["InformationStandard", "Directive"])),
            created_at=fake.date_time(),
            modified_at=fake.date_time(),
            description=fake.catch_phrase(),
            versions=[
                ProtocolVersion(
                    id=uuid.uuid4(),
                    version=version,
                    created_at=fake.date_time(),
                    modified_at=fake.date_time(),
                    description=fake.catch_phrase(),
                )
                for version in _versions
            ],
        )
        for _ in range(count)
    ]


def random_protocols(protocols: List[Protocol]) -> List[ProtocolVersion]:
    pvs = []
    for protocol in random.sample(protocols, randint(1, min(5, len(protocols)))):
        for pv in random.sample(
            protocol.versions, randint(1, min(5, len(protocol.versions)))
        ):
            pvs.append(pv)
    return pvs


def create_healthcare_providers(
    count: int, protocols: List[Protocol]
) -> List[HealthcareProvider]:
    company_name = fake.company()

    return [
        HealthcareProvider(
            id=uuid.uuid4(),
            agb_code=f"{randint(1_000_000,9_999_999)}",
            statutory_name=company_name + " B.V.",
            created_at=fake.date_time(),
            modified_at=fake.date_time(),
            trade_name=company_name,
            ura_code=f"{randint(1_000_000,9_999_999)}",
            qualified_protocols=[
                HealthcareProviderQualification(
                    protocol_version=protocol_version,
                    created_at=fake.date_time(),
                    modified_at=fake.date_time(),
                    qualification_date=fake.date_time(),
                )
                for protocol_version in random_protocols(protocols)
            ],
        )
        for _ in range(count)
    ]


def run():
    db_session = session_factory.create()
    with db_session.session as session:
        roles = create_roles(session)
        system_types = create_system_types(session)

        protocols = create_protocols(count)
        for p in protocols:
            session.add(p)

        healthcare_providers = create_healthcare_providers(count, protocols)
        for h in healthcare_providers:
            session.add(h)

        for _ in range(count):
            session.add(
                create_vendor(
                    roles=roles,
                    system_types=system_types,
                    protocols=protocols,
                    healthcare_providers=healthcare_providers,
                )
            )
        session.commit()


if __name__ == "__main__":
    run()
