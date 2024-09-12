import http from "k6/http";
import { fail, group } from "k6";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";
import { faker } from "https://cdn.skypack.dev/pin/@faker-js/faker@v9.0.0-1CwM7QbrQ59k92yAdP88/mode=imports/optimized/@faker-js/faker.js";

import { pageResponseSchema } from "../api_contracts/page_schema.js";
import { roleSchema } from "../api_contracts/role_schema.js";
import { notFoundResponseSchema, validationErrorResponseSchema } from "../api_contracts/default_response_schemas.js";
import { expectToMatchResponseSchema } from "../utils/expects.js";

export function rolesTests(baseUrl) {
    group("/v1/roles", () => {
        let roleId = undefined;

        describe('POST /v1/roles', () => {
            let body = {
                "name": faker.string.alpha(150),
                "description": faker.lorem.paragraph(),
            };
            let params = {headers: {"Content-Type": "application/json", "Accept": "application/json"}};
            let response = http.post(`${baseUrl}/v1/roles`, JSON.stringify(body), params);

            const data = response.json();
            roleId = data.id;

            expectToMatchResponseSchema(response, 201, roleSchema)
        });

        describe('GET /v1/roles', () => {
            const response = http.get(`${baseUrl}/v1/roles`);
            const data = response.json();

            expectToMatchResponseSchema(response, 200, pageResponseSchema(roleSchema));
        });

        describe('GET /v1/roles/:id', () => {
            if (!roleId) {
                fail('No role found to test GET /v1/roles/:id');
                return;
            }

            const response = http.get(`${baseUrl}/v1/roles/${roleId}`);

            expectToMatchResponseSchema(response, 200, roleSchema);
        });

        describe('PUT /v1/roles/:id', () => {
            if (!roleId) {
                fail('No role found to test PUT /v1/roles/:id');
                return;
            }

            let body = {
                "description": faker.lorem.paragraph(),
            };
            let params = {headers: {"Content-Type": "application/json", "Accept": "application/json"}};
            let response = http.put(`${baseUrl}/v1/roles/${roleId}`, JSON.stringify(body), params);

            expectToMatchResponseSchema(response, 201, roleSchema)
        });

        describe('GET 422 /v1/roles/:id', () => {
            const response = http.get(`${baseUrl}/v1/roles/incorrect-id`);

            expectToMatchResponseSchema(response, 422, validationErrorResponseSchema);
        });

        describe('DEL /v1/roles/:id', () => {
            if (!roleId) {
                fail('No role found to test DEL /v1/roles/:id');
                return;
            }

            const response = http.del(`${baseUrl}/v1/roles/${roleId}`);

            expectToMatchResponseSchema(response, 200, roleSchema);
        });


        describe('GET 404 /v1/roles/:id', () => {
            const response = http.get(`${baseUrl}/v1/roles/ef0b6a18-b294-424e-979c-3dea57c33948`);

            expectToMatchResponseSchema(response, 404, notFoundResponseSchema);
        });
    });
}