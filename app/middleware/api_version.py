from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class ApiVersionHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_version: str):
        super().__init__(app)
        self.api_version = api_version

    async def dispatch(self, request: Request, call_next):
        # Process the request and get the response
        response: Response = await call_next(request)
        # Add the API version header
        response.headers["API-Version"] = self.api_version
        return response
