from typing import Any


def api_version_header() -> dict[str, dict[str, Any]]:
    return {
        "API-Version": {
            "description": "API version in SemVer format",
            "schema": {
                "type": "string"
            }
        }
    }


def api_version_header_responses(response_codes: list[int]) -> dict[int | str, dict[str, Any]]:
    responses: dict[int | str, dict[str, Any]] = {}

    for code in response_codes:
        responses[code] = {
            "headers": {
                **api_version_header()
            }
        }

    return responses


def api_validation_error_response() -> dict[int | str, dict[str, Any]]:
    return {
        422: {
            "description": "Validation error",
            "headers": {
                **api_version_header()
            },
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }


def api_not_found_response() -> dict[int | str, dict[str, Any]]:
    return {
        404: {
            "description": "Not found error",
            "headers": {
                **api_version_header()
            },
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string"
                            }
                        },
                        "required": ["detail"]
                    },
                    "example": {
                        "detail": "Not found"
                    }
                }
            }
        }
    }


def api_conflict_response() -> dict[int | str, dict[str, Any]]:
    return {
        409: {
            "description": "Conflict error",
            "headers": {
                **api_version_header()
            },
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string"
                            }
                        },
                        "required": ["detail"]
                    },
                    "example": {
                        "detail": "Conflict"
                    }
                }
            }
        }
    }
