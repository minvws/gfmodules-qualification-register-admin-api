import http from "k6/http";
import { fail, group } from "k6";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";

import { pageResponseSchema } from "../api_contracts/page_schema.js";
import { notFoundResponseSchema, validationErrorResponseSchema } from "../api_contracts/default_response_schemas.js";
import { expectToMatchResponseSchema } from "../utils/expects.js";
import { applicationSchema } from "../api_contracts/application_schema.js";

export function applicationsTests(baseUrl) {
    group("/v1/applications", () => {
        let applicationId = undefined;

        describe('GET /v1/applications', () => {
            const response = http.get(`${baseUrl}/v1/applications`);
            const data = response.json();

            expectToMatchResponseSchema(response, 200, pageResponseSchema(applicationSchema));

            if (data.items.length > 0) {
                applicationId = data.items[0].id;
            }
        });

        describe('GET /v1/applications/:id', () => {
            if (!applicationId) {
                fail('No application found to test GET /v1/applications/:id');
                return;
            }

            const response = http.get(`${baseUrl}/v1/applications/${applicationId}`);

            expectToMatchResponseSchema(response, 200, applicationSchema);
        });

        describe('GET 422 /v1/applications/:id', () => {
            const response = http.get(`${baseUrl}/v1/applications/incorrect-id`);

            expectToMatchResponseSchema(response, 422, validationErrorResponseSchema);
        });

        describe('GET 404 /v1/applications/:id', () => {
            const response = http.get(`${baseUrl}/v1/applications/ef0b6a18-b294-424e-979c-3dea57c33948`);

            expectToMatchResponseSchema(response, 404, notFoundResponseSchema);
        });
    });
}
