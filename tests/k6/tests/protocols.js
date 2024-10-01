import http from "k6/http";
import { fail, group } from "k6";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";
import { faker } from "https://cdn.skypack.dev/pin/@faker-js/faker@v9.0.0-1CwM7QbrQ59k92yAdP88/mode=imports/optimized/@faker-js/faker.js";

import { expectToMatch204NoContentResponse, expectToMatchResponseSchema } from "../utils/expects.js";
import { pageResponseSchema } from "../api_contracts/page_schema.js";
import { notFoundResponseSchema, validationErrorResponseSchema } from "../api_contracts/default_response_schemas.js";
import { protocolSchema } from "../api_contracts/protocol_schema.js";
import { protocolVersionSchema } from "../api_contracts/protocol_version_schema.js";
import { defaultParams } from "../utils/defaults.js";

export function protocolsTests(baseUrl) {
    group("/v1/protocols", () => {
        let protocolId = undefined;
        let protocolVersionId = undefined;

        describe('POST /v1/protocols', () => {
            let body = {
                "protocolType": `InformationStandard`,
                "name": faker.company.name(),
                "description": faker.company.name()
            };
            let response = http.post(`${baseUrl}/v1/protocols`, JSON.stringify(body), defaultParams);

            const data = response.json();
            protocolId = data.id;

            expectToMatchResponseSchema(response, 201, protocolSchema)
        });

        describe('GET /v1/protocols', () => {
            const response = http.get(`${baseUrl}/v1/protocols`);

            expectToMatchResponseSchema(response, 200, pageResponseSchema(protocolSchema));
        });

        describe('GET /v1/protocols/:id', () => {
            if (!protocolId) {
                fail('No protocol found to test GET /v1/protocols/:id');
                return;
            }

            const response = http.get(`${baseUrl}/v1/protocols/${protocolId}`);

            expectToMatchResponseSchema(response, 200, protocolSchema);
        });

        describe('POST /v1/protocols/:id/versions', () => {
            if (!protocolId) {
                fail('No protocol found to test POST /v1/protocols/:id/versions');
                return;
            }
            let body = {
                "version": `v1.0.0`,
                "description": faker.company.name()
            };
            let response = http.post(`${baseUrl}/v1/protocols/${protocolId}/versions`, JSON.stringify(body), defaultParams);

            const data = response.json();
            protocolVersionId = data.id;

            expectToMatchResponseSchema(response, 201, protocolVersionSchema)
        });

        describe('DEL /v1/protocols/:id/versions/:version_id', () => {
            if (!protocolId || !protocolVersionId) {
                fail('No protocol or protocolVersion found to test DEL /v1/protocols/:id/versions/:version_id');
                return;
            }

            const response = http.del(`${baseUrl}/v1/protocols/${protocolId}/versions/${protocolVersionId}`);

            expectToMatch204NoContentResponse(response);
        });

        describe('DEL /v1/protocols/:id', () => {
            if (!protocolId) {
                fail('No protocol found to test DEL /v1/protocols/:id');
                return;
            }

            const response = http.del(`${baseUrl}/v1/protocols/${protocolId}`);

            expectToMatch204NoContentResponse(response);
        });

        describe('GET 422 /v1/protocols/:id', () => {
            const response = http.get(`${baseUrl}/v1/protocols/incorrect-id`);

            expectToMatchResponseSchema(response, 422, validationErrorResponseSchema);
        });

        describe('GET 404 /v1/protocols/:id', () => {
            const response = http.get(`${baseUrl}/v1/protocols/ef0b6a18-b294-424e-979c-3dea57c33948`);

            expectToMatchResponseSchema(response, 404, notFoundResponseSchema);
        });
    });
}