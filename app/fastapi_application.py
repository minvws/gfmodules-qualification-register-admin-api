import logging

from typing import Any

from fastapi import FastAPI
import uvicorn

from app.fastapi.custom_fastapi import CustomFastAPI
from app.routers.v1.vendors_router import router as vendors_router
from app.routers.v1.applications_router import router as applications_router
from app.routers.v1.system_types_router import router as system_types_router
from app.routers.v1.healthcare_provider_router import (
    router as healthcare_provider_router,
)
from app.routers.v1.roles_router import router as roles_router
from app.routers.v1.protocol_router import router as protocol_router
from app.routers.v1.qualification_router import (
    router as qualification_router,
)

from app.fastapi.setup import fastapi_mount_api, setup_default_middleware_and_routers
from app.routers.default import router as default_router
from app.routers.health import router as health_router
from app.config import get_config


def get_uvicorn_params() -> dict[str, Any]:
    config = get_config()

    kwargs = {
        "host": config.uvicorn.host,
        "port": config.uvicorn.port,
        "reload": config.uvicorn.reload,
    }
    if (config.uvicorn.use_ssl
        and config.uvicorn.ssl_base_dir
        and config.uvicorn.ssl_cert_file
        and config.uvicorn.ssl_key_file
    ):
        kwargs["ssl_keyfile"] = (
            config.uvicorn.ssl_base_dir + "/" + config.uvicorn.ssl_key_file
        )
        kwargs["ssl_certfile"] = (
            config.uvicorn.ssl_base_dir + "/" + config.uvicorn.ssl_cert_file
        )

    return kwargs


def run() -> None:
    uvicorn.run("app.fastapi_application:create_fastapi_app", **get_uvicorn_params(), reload_delay=1, reload_dirs="app")


def create_fastapi_app() -> FastAPI:
    application_init()

    config = get_config()

    title = "Qualification Register Admin API"
    docs_url = None
    redoc_url = None

    if config.uvicorn.swagger_enabled:
        docs_url = config.uvicorn.docs_url
        redoc_url = config.uvicorn.redoc_url

    fastapi = FastAPI(
        title=title,
        description="This is the documentation of the root endpoints. "
                    "For the rest of the API documentation see the [/v1/docs](/v1/docs).",
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    setup_default_middleware_and_routers(
        fastapi=fastapi,
        routers=[
            default_router,
            health_router,
        ],
    )

    # v1 api

    fastapi_v1 = CustomFastAPI(
        title=title,
        description="This is the documentation of the /v1 endpoints.",
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_tags=[
            {
                "name": "Vendors",
            },
            {
                "name": "Roles",
            },
            {
                "name": "System Types",
            },
            {
                "name": "Applications",
            },
            {
                "name": "Protocols",
            },
            {
                "name": "Healthcare  Provider",
            },
            {
                "name": "Qualification",
            },
        ]
    )
    setup_default_middleware_and_routers(
        fastapi=fastapi_v1,
        routers=[
            vendors_router,
            roles_router,
            system_types_router,
            applications_router,
            protocol_router,
            healthcare_provider_router,
            qualification_router,
        ],
        api_version="1.0.0",
    )
    fastapi_mount_api(root_fastapi=fastapi, mount_path="/v1", api=fastapi_v1)

    return fastapi


def application_init() -> None:
    setup_logging()


def setup_logging() -> None:
    loglevel = logging.getLevelName(get_config().app.loglevel.upper())

    if isinstance(loglevel, str):
        raise ValueError(f"Invalid loglevel {loglevel.upper()}")
    logging.basicConfig(
        level=loglevel,
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
