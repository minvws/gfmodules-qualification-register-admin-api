import random
import uuid
from random import randint
from typing import Sequence, List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_config
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
from app.db.entities.protocol import Protocol
from app.db.entities.protocol_version import ProtocolVersion
from app.db.entities.role import Role
from app.db.entities.system_type import SystemType
from app.db.entities.vendor import Vendor
from faker import Faker

import argparse

parser = argparse.ArgumentParser("Data generation")
parser.add_argument(
    "-c",
    "--count",
    metavar="c",
    dest="count",
    help="A global number to give a indication of how many entities you want.",
    type=int,
    default=1,
)
args = parser.parse_args()

count = args.count

config = get_config()

engine = create_engine(config.database.dsn)

session_factory = sessionmaker(engine)

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
    role_names = [
        "Acute Zorg Proces - (Spoed)melding Sturend [AZP-SPS] Systeem",
        "Acute Zorg Proces - Ambulanceoverdracht Ontvangend [AZP-AOO] Systeem",
        "Acute Zorg Proces - Ambulanceoverdracht Sturend [AZP-AOS] Systeem",
        "Acute Zorg Proces - Ambulanceoverdracht Sturend [AZP-AOS] Systeem (naar SEH)",
        "Acute Zorg Proces - Beschikbaarstellen PS [AZP-PAB]",
        "Acute Zorg Proces - Beschikbaarstellen PS [AZP-PSB]",
        "Acute Zorg Proces - Feedbackbericht Ontvangend [AZP-PAO] Systeem",
        "Acute Zorg Proces - Huisartsverwijzing Sturend [AZP-VES] Systeem",
        "Acute Zorg Proces - Patiëntidentificatie Sturend [AZP-PAS] Systeem",
        "Acute Zorg Proces - Raadplegen Professionele samenvatting SEH [AZP-PSR]",
        "Acute Zorg Proces - Spoedmelding Ontvangend [AZP-SPO] Systeem",
        "Acute Zorg Proces - Verwijzing ontvangend (AZP-VEO) Systeem",
        "Acute Zorg Proces - Verwijzing Sturend [AZP-VES] Systeem",
        "ambulanceoverdracht naar SEH",
        "Beschikbaarstellen",
        "Conditie-vaststeller",
        "Geboortezorg Kernset Sturend Systeem",
        "JGZ-dossierontvanger",
        "JGZ-dossieroverdrager",
        "JGZ-hielprikcoördinator",
        "JGZ-hielprikuitvoerder",
        "JGZ-vaccinatiecoördinator",
        "JGZ-vaccinatieuitvoerder",
        "Ketenzorg HIS",
        "Ketenzorg KIS",
        "Medicatie voorschrift ontvangend systeem (zonder EH)",
        "Medicatiebewaker",
        "Medicatiegegevens beschikbaarstellen MA (MP-MGB-MA)",
        "Medicatiegegevens beschikbaarstellen VV (MP-MGB-VV)",
        "Medicatieraadpleger",
        "Medicatieverstrekker",
        "Medicatievoorschrift ontvangend systeem (zonder EH)",
        "Medicatievoorschrift sturend systeem (MP-VOS)",
        "Medicatievoorschrift sturend systeem (zonder EH)",
        "Opleveren van labgegevens",
        "Overdrachtsbericht ontvangend systeem - overlap BgZ",
        "Overdrachtsbericht sturend systeem - overlap BgZ",
        "Raadplegen",
        "Raadpleger labgegevens",
        "Vaste huisarts",
        "Waarnemend huisarts",
    ]
    return [create_role(session, name) for name in role_names]


def create_system_types(session: Session):
    system_types = [
        "AIS",
        "AMBS",
        "DD JGZ",
        "EVS",
        "HIS",
        "KIS",
        "Viewer",
        "ZAIS",
        "ZBC",
        "ZIC",
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
    with session_factory() as session:
        # define roles in the database
        roles = create_roles(session)
        for role in roles:
            session.add(role)

        # define system types in the database
        system_types = create_system_types(session)
        for system_type in system_types:
            session.add(system_type)

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
