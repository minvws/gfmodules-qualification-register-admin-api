from app.db.entities.role import Role
from app.schemas.roles.schema import RoleDTO


def map_role_model_to_dto(role: Role) -> RoleDTO:
    return RoleDTO(id=role.id, name=role.name, description=role.description)
