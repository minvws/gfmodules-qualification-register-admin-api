from app.exceptions.http_base_exceptions import (
    NotFoundException,
    ConflictException,
    ServiceUnavailableException,
)


class VendorNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Vendor not found")


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


class RoleAlreadyExistsException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Role already exists")


class RoleExistInApplicationException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Role is already assigned to application")


class RoleNotInApplicationException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Role is not assigned to application")


class RoleDeleteException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Deleting role failed")


class RoleDBServiceUnavailableException(ServiceUnavailableException):
    def __init__(self) -> None:
        super().__init__("Service is unavailable")
