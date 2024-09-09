# k6 Tests

We are using [k6](https://k6.io/) to run functional and performance tests on our APIs.

## Running the tests

To run the tests, you need to have k6 installed. You can download it from [here](https://grafana.com/docs/k6/latest/set-up/install-k6/).

After installing k6, you can run the tests using the following command:

```bash
k6 run tests/k6/script.js
```

### Different environments

If you want to run the tests on a different environment, you can set the `ENDPOINT_URL` environment variable:

```bash
ENDPOINT_URL=https://api.example.com k6 run tests/k6/script.js
```

Or using the `-e` flag:

```bash
k6 run -e ENDPOINT_URL=https://api.example.com tests/k6/script.js
```  