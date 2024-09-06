import { expect } from "https://jslib.k6.io/k6chaijs/4.3.4.1/index.js";

export function expectToMatchResponseSchema(response, expectedStatusCode, expectedSchema) {
    expect(response.status, 'response status').to.equal(expectedStatusCode);

    expect(response).to.have.validJsonBody();
    expect(response.json()).to.matchSchema(expectedSchema);
}