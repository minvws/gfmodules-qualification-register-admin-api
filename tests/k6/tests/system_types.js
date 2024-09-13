import http from "k6/http";
import { fail, group } from "k6";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";
import { faker } from "https://cdn.skypack.dev/pin/@faker-js/faker@v9.0.0-1CwM7QbrQ59k92yAdP88/mode=imports/optimized/@faker-js/faker.js";

import { pageResponseSchema } from "../api_contracts/page_schema.js";
import { systemTypeSchema } from "../api_contracts/system_type_schema.js";
import { notFoundResponseSchema, validationErrorResponseSchema } from "../api_contracts/default_response_schemas.js";
import { expectToMatch204NoContentResponse, expectToMatchResponseSchema } from "../utils/expects.js";
import { defaultParams } from "../utils/defaults.js";

export function systemTypesTests(baseUrl) {
    group("/v1/system-types", () => {
        let systemTypeId = undefined;

        describe('POST /v1/system-types', () => {
            let body = {
                "name": faker.string.alpha(150),
                "description": faker.lorem.paragraph(),
            };
            let response = http.post(`${baseUrl}/v1/system-types`, JSON.stringify(body), defaultParams);

            const data = response.json();
            systemTypeId = data.id;

            expectToMatchResponseSchema(response, 201, systemTypeSchema)
        });

        describe("GET /v1/system-types", () => {
            const response = http.get(`${baseUrl}/v1/system-types`);

            expectToMatchResponseSchema(response, 200, pageResponseSchema(systemTypeSchema));
        });

        describe('GET /v1/system-types/:id', () => {
            if (!systemTypeId) {
                fail('No system type found to test GET /v1/system-types/:id');
                return;
            }

            const response = http.get(`${baseUrl}/v1/system-types/${systemTypeId}`);

            expectToMatchResponseSchema(response, 200, systemTypeSchema);
        });

        describe('DEL /v1/roles/:id', () => {
            if (!systemTypeId) {
                fail('No system type found to test DEL /v1/system-types/:id');
                return;
            }

            const response = http.del(`${baseUrl}/v1/system-types/${systemTypeId}`);

            expectToMatch204NoContentResponse(response);
        });

        describe('GET 422 /v1/system-types/:id', () => {
            const response = http.get(`${baseUrl}/v1/system-types/incorrect-id`);

            expectToMatchResponseSchema(response, 422, validationErrorResponseSchema);
        });

        describe('GET 404 /v1/system-types/:id', () => {
            const response = http.get(`${baseUrl}/v1/system-types/ef0b6a18-b294-424e-979c-3dea57c33948`);

            expectToMatchResponseSchema(response, 404, notFoundResponseSchema);
        });
    });
}