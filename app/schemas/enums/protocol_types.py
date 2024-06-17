from enum import Enum


class ProtocolTypes(str, Enum):
    INFORMATION_STANDARD = "InformationStandard"
    DIRECTIVE = "Directive"
