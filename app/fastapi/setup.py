from typing import List

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.middleware.api_version import ApiVersionHeaderMiddleware


def setup_default_middleware_and_routers(
        fastapi: FastAPI,
        routers: List[APIRouter],
        api_version: str | None = None,
) -> FastAPI:
    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        fastapi.include_router(router)

    if api_version is not None:
        fastapi.add_middleware(ApiVersionHeaderMiddleware, api_version=api_version)

    return fastapi


def fastapi_mount_api(root_fastapi: FastAPI, mount_path: str, api: FastAPI) -> None:
    root_fastapi.mount(mount_path, api)

    @root_fastapi.get(mount_path, include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url=mount_path + '/docs')
