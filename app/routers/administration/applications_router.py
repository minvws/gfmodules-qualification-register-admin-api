from uuid import UUID

from fastapi import APIRouter, Depends

from app.container import get_application_roles_service
from app.schemas.application.mapper import map_application_entity_to_dto
from app.schemas.application.schema import ApplicationDTO
from app.services.application_roles_service import ApplicationRolesService

router = APIRouter(prefix="/administration/applications", tags=["Applications"])


@router.patch("/{application_id}/role/{role_id}")
def assign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> ApplicationDTO:
    results = service.assign_role_to_application(application_id, role_id)
    return map_application_entity_to_dto(results)


@router.delete("/{application_id}/role/{role_id}")
def unassign_one_application_role(
    application_id: UUID,
    role_id: UUID,
    service: ApplicationRolesService = Depends(get_application_roles_service),
) -> ApplicationDTO:
    results = service.remove_role_from_application(application_id, role_id)
    return map_application_entity_to_dto(results)
