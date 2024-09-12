import { chai } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";
import { initContractPlugin } from "https://jslib.k6.io/k6chaijs-contracts/4.3.4.1/index.js";
import { healthTests } from "./tests/health.js";
import { vendorsTests } from "./tests/vendors.js";
import { rolesTests } from "./tests/roles.js";
import { systemTypesTests } from "./tests/system_types.js";

const baseUrl = __ENV.ENDPOINT_URL ?? "http://localhost:8506";
// Sleep duration between successive requests.
// You might want to edit the value of this variable or remove calls to the sleep function on the script.
const SLEEP_DURATION = 0.1;
// Global variables should be initialized.

export const options = {
  thresholds: {
    // all checks should pass
    checks: [{ threshold: 'rate == 1.00', abortOnFail: true }],
    // 99% of requests should be below 1s
    http_req_duration: ['p(99)<1000'],
  },
};

initContractPlugin(chai)

export default function testSuite() {
    healthTests(baseUrl);
    vendorsTests(baseUrl);
    rolesTests(baseUrl);
    systemTypesTests(baseUrl);
}
