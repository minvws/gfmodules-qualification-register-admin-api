import logging
from typing import Any

from fastapi import APIRouter
from gfmodules_python_shared.session.healthy import is_healthy_database

logger = logging.getLogger(__name__)
router = APIRouter()


def ok_or_error(value: bool) -> str:
    return "ok" if value else "error"


@router.get("/health")
def health() -> dict[str, Any]:
    logger.info("Checking database health")

    components = {
        "database": ok_or_error(is_healthy_database()),
    }

    return {
        "status": ok_or_error(all(value == "ok" for value in components.values())),
        "components": components,
    }
