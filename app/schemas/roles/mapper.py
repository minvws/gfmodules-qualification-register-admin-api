from app.db.entities.role import Role
from app.schemas.roles.schema import RoleDto


def map_role_model_to_dto(role: Role) -> RoleDto:
    return RoleDto(id=role.id, name=role.name, description=role.description)
