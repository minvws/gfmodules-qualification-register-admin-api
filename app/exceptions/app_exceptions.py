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
        super().__init__("System type already exists")


class SystemTypeExistInApplicationException(ConflictException):
    def __init__(self) -> None:
        super().__init__("System type already exist in application")


class SystemTypeNotUsedByApplicationException(ConflictException):
    def __init__(self) -> None:
        super().__init__("System type does not exist in application")


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


class ProtocolVersionNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Protocol version not found")


class AppVersionExistsInHealthcareProviderException(ConflictException):
    def __init__(self) -> None:
        super().__init__(
            "Application Version already being used by Healthcare provider"
        )


class AppVersionNotUsedByHealthcareProviderException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Application version is not being used by Healthcare provider")


class AppVersionAlreadyQualifiedException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Application version is already qualified for the protocol")


class AppVersionAlreadyArchivedException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Application Version is already archived for protocol")


class AppVersionNotQualifiedForProtocolException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Application version is not qualified for the protocol")


class HealthcareProviderAlreadyQualifiedException(ConflictException):
    def __init__(self) -> None:
        super().__init__(
            "Healthcare provider already qualified for the protocol version"
        )


class HealthcareProviderQualificationAlreadyArchivedException(ConflictException):
    def __init__(self) -> None:
        super().__init__("Qualification is already archived for healthcare provider")


class HealthcareProviderNotQualifiedForProtocolException(NotFoundException):
    def __init__(self) -> None:
        super().__init__("Healthcare provider is not qualified for the protocol")
