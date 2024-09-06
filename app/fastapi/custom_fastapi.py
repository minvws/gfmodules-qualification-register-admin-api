from typing import Dict, Any

from fastapi import FastAPI

from app.openapi.responses import api_version_header


class CustomFastAPI(FastAPI):

    def openapi(self) -> Dict[str, Any]:
        if self.openapi_schema:
            return self.openapi_schema

        schema = super().openapi()
        paths = schema.get('paths')
        if not isinstance(paths, dict):
            return schema

        for _, method_item in paths.items():
            for _, param in method_item.items():
                responses = param.get('responses')
                for key in responses.keys():
                    if int(key) < 500:
                        headers = responses[key].get('headers', {})
                        responses[key]['headers'] = {**headers, **api_version_header()}

        self.openapi_schema = schema
        return schema
