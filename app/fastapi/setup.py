from typing import List, Dict, Any

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.config import Config
from app.middleware.api_version import ApiVersionHeaderMiddleware


def setup_fastapi(
        config: Config,
        routers: List[APIRouter],
        description: str = "",
        openapi_tags: List[Dict[str, Any]] | None = None,
) -> FastAPI:
    docs_url = config.uvicorn.docs_url if config.uvicorn.swagger_enabled else None
    redoc_url = config.uvicorn.redoc_url if config.uvicorn.swagger_enabled else None

    fastapi = FastAPI(
        title="Qualification Register Admin API",
        docs_url=docs_url,
        redoc_url=redoc_url,
        description=description,
        openapi_tags=openapi_tags
    )

    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        fastapi.include_router(router)

    return fastapi


def setup_fastapi_for_api(
        config: Config,
        routers: List[APIRouter],
        api_version: str,
        description: str = "",
        openapi_tags: List[Dict[str, Any]] | None = None,
) -> FastAPI:
    fastapi = setup_fastapi(config, routers, description, openapi_tags)

    fastapi.add_middleware(ApiVersionHeaderMiddleware, api_version=api_version)

    return fastapi


def fastapi_mount_api(root_fastapi: FastAPI, mount_path: str, api: FastAPI) -> None:
    root_fastapi.mount(mount_path, api)

    @root_fastapi.get(mount_path, include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url=mount_path + '/docs')