from uuid import UUID

from gfmodules_python_shared.session.session_manager import (
    session_manager,
    get_repository,
)

from app.db.entities.healthcare_provider import HealthcareProvider
from app.db.repository.healthcare_provider_repository import (
    HealthcareProviderRepository,
)
from app.db.repository.protocol_version_repository import ProtocolVersionRepository
from app.exceptions.app_exceptions import (
    HealthcareProviderNotFoundException,
    URACodeAlreadyExists,
    AGBCodeAlreadyExists,
    ProtocolVersionNotFoundException,
)
from app.factory.healthcare_provider_factory import HealthcareProviderFactory
from app.schemas.healthcare_provider.mapper import map_healthcare_provider_entity_to_dto
from app.schemas.healthcare_provider.schema import HealthcareProviderDto
from app.schemas.meta.schema import Page


class HealthcareProviderService:
    @session_manager
    def get_one(
        self,
        provider_id: UUID,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(id=provider_id)
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        return healthcare_provider

    @session_manager
    def get_paginated(
        self,
        limit: int,
        offset: int,
        healthcare_providers_repository: HealthcareProviderRepository = get_repository(),
    ) -> Page[HealthcareProviderDto]:
        healthcare_providers = healthcare_providers_repository.get_many(
            limit=limit, offset=offset
        )
        dto = [
            map_healthcare_provider_entity_to_dto(provider)
            for provider in healthcare_providers
        ]
        total = healthcare_providers_repository.count()

        return Page(items=dto, total=total, limit=limit, offset=offset)

    @session_manager
    def add_one(
        self,
        ura_code: str,
        agb_code: str,
        trade_name: str,
        statutory_name: str,
        protocol_version_id: UUID,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
        protocol_version_repository: ProtocolVersionRepository = get_repository(),
    ) -> HealthcareProvider:
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

        protocol_version = protocol_version_repository.get(id=protocol_version_id)
        if protocol_version is None:
            raise ProtocolVersionNotFoundException()

        new_healthcare_provider = HealthcareProviderFactory.create_instance(
            ura_code=ura_code,
            agb_code=agb_code,
            trade_name=trade_name,
            statutory_name=statutory_name,
            protocol_version=protocol_version,
        )
        healthcare_provider_repository.create(new_healthcare_provider)

        return new_healthcare_provider

    @session_manager
    def remove_one(
        self,
        provider_id: UUID,
        healthcare_provider_repository: HealthcareProviderRepository = get_repository(),
    ) -> HealthcareProvider:
        healthcare_provider = healthcare_provider_repository.get(id=provider_id)
        if healthcare_provider is None:
            raise HealthcareProviderNotFoundException()

        healthcare_provider_repository.delete(healthcare_provider)

        return healthcare_provider
