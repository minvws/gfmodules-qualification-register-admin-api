from typing import Callable, Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class ApiVersionHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, api_version: str):
        super().__init__(app)
        self.api_version = api_version

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Process the request and get the response
        response = await call_next(request)
        # Add the API version header
        response.headers["API-Version"] = self.api_version
        return response
