from typing import Sequence
from uuid import UUID

from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.repository.healthcare_provider_repository import (
    HealthcareProviderRepository,
)
from app.db.session_factory import DbSessionFactory
from app.exceptions.app_exceptions import (
    HealthcareProviderNotFoundException,
    URACodeAlreadyExists,
    AGBCodeAlreadyExists,
)
from app.factory.healthcare_provider_factory import HealthcareProviderFactory


class HealthcareProviderService:
    def __init__(self, db_session_factory: DbSessionFactory):
        self.db_session_factory = db_session_factory

    def get_one_by_id(self, provider_id: UUID) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

        return healthcare_provider

    def get_all_healthcare_providers(self) -> Sequence[HealthcareProvider]:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        session = db_session.session
        with session:
            healthcare_providers = healthcare_provider_repository.find_all()

        return healthcare_providers

    def add_one_provider(
        self, ura_code: str, agb_code: str, trade_name: str, statutory_name: str
    ) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        session = db_session.session
        with session:
            ura_code_exists = healthcare_provider_repository.ura_code_exists(
                ura_code=ura_code
            )
            if ura_code_exists:
                raise URACodeAlreadyExists()

            agb_code_exists = healthcare_provider_repository.agb_code_exists(
                agb_code=agb_code
            )
            if agb_code_exists:
                raise AGBCodeAlreadyExists()

            new_healthcare_provider = HealthcareProviderFactory.create_instance(
                ura_code=ura_code,
                agb_code=agb_code,
                trade_name=trade_name,
                statutory_name=statutory_name,
            )
            healthcare_provider_repository.create(new_healthcare_provider)

        return new_healthcare_provider

    def delete_one_healthcare_provider(self, provider_id: UUID) -> HealthcareProvider:
        db_session = self.db_session_factory.create()
        healthcare_provider_repository: HealthcareProviderRepository = (
            db_session.get_repository(HealthcareProvider)
        )
        session = db_session.session
        with session:
            healthcare_provider = healthcare_provider_repository.find_one(
                id=provider_id
            )
            if healthcare_provider is None:
                raise HealthcareProviderNotFoundException()

            healthcare_provider_repository.delete(healthcare_provider)

        return healthcare_provider
