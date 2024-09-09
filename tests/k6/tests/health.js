import http from "k6/http";
import { describe } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";

import { healthResponseSchema } from "../api_contracts/health_schema.js";
import { expectToMatchResponseSchema } from "../utils/expects.js";

export function healthTests(baseUrl) {
    describe("GET /health", () => {
        const response = http.get(`${baseUrl}/health`);

        expectToMatchResponseSchema(response, 200, healthResponseSchema);
    });
}