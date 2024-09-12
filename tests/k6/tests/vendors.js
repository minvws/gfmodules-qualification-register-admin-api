import http from "k6/http";
import { fail, group } from "k6";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";
import { faker } from "https://cdn.skypack.dev/pin/@faker-js/faker@v9.0.0-1CwM7QbrQ59k92yAdP88/mode=imports/optimized/@faker-js/faker.js";

import { pageResponseSchema } from "../api_contracts/page_schema.js";
import { vendorSchema } from "../api_contracts/vendor_schema.js";
import { notFoundResponseSchema, validationErrorResponseSchema } from "../api_contracts/default_response_schemas.js";
import { expectToMatchResponseSchema } from "../utils/expects.js";
import { defaultParams } from "../utils/defaults.js";

export function vendorsTests(baseUrl) {
    group("/v1/vendors", () => {
        let vendorId = undefined;
        let kvkNumber = undefined;

        describe('POST /v1/vendors', () => {
            kvkNumber = faker.number.int({ min: 10000000, max: 99999999});

            let body = {
                "kvkNumber": `${kvkNumber}`,
                "tradeName": faker.company.name(),
                "statutoryName": faker.company.name()
            };
            let response = http.post(`${baseUrl}/v1/vendors`, JSON.stringify(body), defaultParams);

            const data = response.json();
            vendorId = data.id;

            expectToMatchResponseSchema(response, 201, vendorSchema)
        });

        describe('GET /v1/vendors', () => {
            const response = http.get(`${baseUrl}/v1/vendors`);
            const data = response.json();

            expectToMatchResponseSchema(response, 200, pageResponseSchema(vendorSchema));
        });

        describe('GET /v1/vendors/:id', () => {
            if (!vendorId) {
                fail('No vendor found to test GET /v1/vendors/:id');
                return;
            }

            const response = http.get(`${baseUrl}/v1/vendors/${vendorId}`);

            expectToMatchResponseSchema(response, 200, vendorSchema);
        });

        describe('GET /v1/vendors/kvk_number/:kvk_number', () => {
            if (!kvkNumber) {
                fail('No kvk number to test GET /v1/vendors/kvk_number/:kvk_number');
                return;
            }

            const response = http.get(`${baseUrl}/v1/vendors/kvk_number/${kvkNumber}`);

            expectToMatchResponseSchema(response, 200, vendorSchema);
        });

        describe('DEL /v1/vendors/:id', () => {
            if (!vendorId) {
                fail('No vendor found to test DEL /v1/vendors/:id');
                return;
            }

            const response = http.del(`${baseUrl}/v1/vendors/${vendorId}`);

            expectToMatchResponseSchema(response, 200, vendorSchema);
        });

        describe('GET 422 /v1/vendors/:id', () => {
            const response = http.get(`${baseUrl}/v1/vendors/incorrect-id`);

            expectToMatchResponseSchema(response, 422, validationErrorResponseSchema);
        });

        describe('GET 404 /v1/vendors/:id', () => {
            const response = http.get(`${baseUrl}/v1/vendors/ef0b6a18-b294-424e-979c-3dea57c33948`);

            expectToMatchResponseSchema(response, 404, notFoundResponseSchema);
        });
    });
}