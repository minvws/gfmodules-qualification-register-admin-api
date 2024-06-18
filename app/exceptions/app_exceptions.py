from app.exceptions.http_base_exceptions import (
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
    MethodNotAllowedException,
)


class VendorNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Vendor not found")


class VendorAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Vendor already exists")


class VendorCannotBeDeletedException(MethodNotAllowedException):
    def __init__(self) -> None:
        super().__init__("Vendor cannot be deleted")


class RoleNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Role not found")


class ApplicationNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Application not found")


class ApplicationAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Application already exists")


class ApplicationUpdateException(ServiceUnavailableException):
    def __init__(self) -> None:
        super().__init__("Updating application failed, please try again later")


class ApplicationRoleNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Cannot assign a non existent role to an application")


class ApplicationVersionNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Application version not found")


class ApplicationVersionDeleteException(ConflictException):
    def __init__(self) -> None:
        super().__init__(
            "Cannot delete version, application should at least contain one version"
        )


class ApplicationRoleDeleteException(ConflictException):
    def __init__(self) -> None:
        super().__init__(
            "Cannot delete role, application should at least contain one role"
        )


class RoleAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Role already exists")


class RoleExistInApplicationException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Role is already assigned to application")


class SystemTypeNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("System type not found")


class SystemTypeAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__("System type already exists in app")


class HealthcareProviderNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Healthcare provider not found")


class URACodeAlreadyExists(ConflictException):
    def __init__(self) -> None:
        super().__init__("URA code already exists")


class AGBCodeAlreadyExists(ConflictException):
    def __init__(self) -> None:
        super().__init__("AGB code already exists")


class ProtocolNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Protocol not found")
