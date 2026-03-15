---
name: apideck-portman
description: API contract testing with Portman by Apideck. Use when generating Postman collections from OpenAPI specs, writing contract tests, variation tests, integration tests, fuzz testing, or setting up CI/CD API test pipelines. Portman converts OpenAPI 3.x specs into Postman collections with auto-generated test suites.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

# Portman API Testing Skill

## Overview

[Portman](https://github.com/apideck-libraries/portman) converts OpenAPI 3.x specifications into Postman collections with auto-generated contract tests, variation tests, content tests, and integration tests. It runs tests via Newman (Postman's CLI runner) and integrates into CI/CD pipelines.

## Installation

```sh
npm install -g @apideck/portman
```

Or use without installing:

```sh
npx @apideck/portman -l your-openapi-spec.yaml
```

## IMPORTANT RULES

- ALWAYS use a `portman-config.json` (or `.yaml`) for test configuration. Do not rely solely on defaults for production use.
- ALWAYS target operations using `openApiOperationId` or `openApiOperation` (method::path) syntax.
- USE `--baseUrl` to override the spec's server URL when testing against local/staging environments.
- USE `--envFile` to inject environment variables. Variables prefixed with `PORTMAN_` auto-map to Postman collection variables.
- USE `assignVariables` to chain request/response values across operations (e.g., capture `id` from create, use in get/update/delete).
- DO NOT hardcode secrets in portman-config. Use environment variables and `.env` files.

## Quick Start

```sh
# Generate collection from local spec
portman -l ./openapi.yaml

# Generate and run tests against live API
portman -l ./openapi.yaml -b https://api.example.com -n true

# With custom config
portman -l ./openapi.yaml -c ./portman-config.json -b https://api.example.com -n true
```

## Configuration File

Create `portman-config.json` (or `.yaml`):

```json
{
  "version": 1.0,
  "tests": {
    "contractTests": [],
    "contentTests": [],
    "variationTests": [],
    "integrationTests": [],
    "extendTests": []
  },
  "assignVariables": [],
  "overwrites": [],
  "globals": {}
}
```

JSON Schema: `https://raw.githubusercontent.com/apideck-libraries/portman/main/src/utils/portman-config-schema.json`

## Targeting Operations

All test and overwrite sections use the same targeting system:

```json
// By operationId
{ "openApiOperationId": "leadsAdd" }

// By multiple operationIds
{ "openApiOperationIds": ["leadsAdd", "leadsAll"] }

// By method::path (supports wildcards)
{ "openApiOperation": "GET::/crm/leads" }
{ "openApiOperation": "*::/crm/*" }
{ "openApiOperation": "POST::/*" }

// Exclude specific operations
{ "openApiOperation": "*::/crm/*", "excludeForOperations": ["leadsDelete"] }
```

## Contract Tests

Validate API responses conform to the OpenAPI spec:

```json
{
  "tests": {
    "contractTests": [
      {
        "openApiOperation": "*::/*",
        "statusSuccess": { "enabled": true },
        "contentType": { "enabled": true },
        "jsonBody": { "enabled": true },
        "schemaValidation": { "enabled": true },
        "headersPresent": { "enabled": true }
      },
      {
        "openApiOperation": "*::/*",
        "responseTime": { "enabled": true, "maxMs": 300 }
      }
    ]
  }
}
```

| Test | Description |
|------|-------------|
| `statusSuccess` | Response returns 2xx |
| `statusCode` | Response returns specific HTTP code |
| `contentType` | Content-Type matches spec |
| `jsonBody` | Body is valid JSON matching spec |
| `schemaValidation` | Body validates against JSON schema |
| `headersPresent` | Required headers are present |
| `responseTime` | Response within `maxMs` milliseconds |

## Content Tests

Validate specific response values:

```json
{
  "tests": {
    "contentTests": [
      {
        "openApiOperationId": "leadsAll",
        "responseBodyTests": [
          { "key": "status_code", "value": 200 },
          { "key": "data[0].id", "assert": "not.to.be.null" },
          { "key": "data", "minLength": 1 },
          { "key": "resource", "oneOf": ["leads", "contacts"] }
        ],
        "responseHeaderTests": [
          { "key": "content-type", "contains": "application/json" }
        ]
      }
    ]
  }
}
```

Content test assertions: `value` (exact), `contains` (substring), `oneOf`, `length`, `minLength`, `maxLength`, `notExist`, `assert` (Postman assertion string).

## Variation Tests

Test alternative scenarios (errors, edge cases, unauthorized access):

```json
{
  "tests": {
    "variationTests": [
      {
        "openApiOperation": "*::/crm/*",
        "openApiResponse": "401",
        "variations": [
          {
            "name": "Unauthorized",
            "overwrites": [
              { "overwriteRequestSecurity": { "bearer": { "token": "invalid" } } }
            ],
            "tests": {
              "contractTests": [{ "statusCode": { "enabled": true } }]
            }
          }
        ]
      },
      {
        "openApiOperationId": "leadsAdd",
        "openApiResponse": "400",
        "variations": [
          {
            "name": "MissingRequiredFields",
            "overwrites": [
              { "overwriteRequestBody": [{ "key": "name", "value": "", "overwrite": true }] }
            ],
            "tests": {
              "contractTests": [
                { "statusCode": { "enabled": true } },
                { "schemaValidation": { "enabled": true } }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

## Fuzz Testing

Auto-generate invalid values based on schema constraints:

```json
{
  "tests": {
    "variationTests": [
      {
        "openApiOperation": "*::/crm/*",
        "openApiResponse": "422",
        "variations": [
          {
            "name": "FuzzTest",
            "fuzzing": [
              {
                "requestBody": [
                  {
                    "requiredFields": { "enabled": true },
                    "minimumNumberFields": { "enabled": true },
                    "maximumNumberFields": { "enabled": true },
                    "minLengthFields": { "enabled": true },
                    "maxLengthFields": { "enabled": true }
                  }
                ]
              }
            ],
            "tests": {
              "contractTests": [{ "statusCode": { "enabled": true } }]
            }
          }
        ]
      }
    ]
  }
}
```

Fuzzing targets: `requestBody`, `requestQueryParams`, `requestHeaders`.

## Integration Tests

Group operations into end-to-end workflows:

```json
{
  "tests": {
    "integrationTests": [
      {
        "name": "Lead Lifecycle",
        "operations": [
          { "openApiOperationId": "leadsAdd" },
          { "openApiOperationId": "leadsOne" },
          { "openApiOperationId": "leadsUpdate" },
          { "openApiOperationId": "leadsDelete" }
        ]
      }
    ]
  }
}
```

## Variable Chaining

Capture values from responses to use in subsequent requests:

```json
{
  "assignVariables": [
    {
      "openApiOperationId": "leadsAdd",
      "collectionVariables": [
        { "responseBodyProp": "data.id", "name": "leadId" },
        { "responseHeaderProp": "x-request-id", "name": "requestId" }
      ]
    }
  ]
}
```

Use captured variables in overwrites: `{{leadId}}`, `{{requestId}}`.

## Request Overwrites

Modify generated requests:

```json
{
  "overwrites": [
    {
      "openApiOperationId": "leadsAdd",
      "overwriteRequestBody": [
        { "key": "name", "value": "Test Lead {{$randomInt}}", "overwrite": true }
      ],
      "overwriteRequestHeaders": [
        { "key": "x-apideck-consumer-id", "value": "{{consumerId}}", "overwrite": true }
      ]
    },
    {
      "openApiOperation": "DELETE::/crm/leads/{id}",
      "overwriteRequestPathVariables": [
        { "key": "id", "value": "{{leadId}}", "overwrite": true }
      ]
    }
  ]
}
```

Security overwrites: `overwriteRequestSecurity` supports `bearer`, `apiKey`, `basic`, `oauth2`, and `remove`.

## Globals

```json
{
  "globals": {
    "collectionPreRequestScripts": ["pm.collectionVariables.set('timestamp', Date.now());"],
    "securityOverwrites": {
      "bearer": { "token": "{{bearerToken}}" }
    },
    "keyValueReplacements": { "x-apideck-app-id": "{{applicationId}}" },
    "valueReplacements": { "<Bearer Token>": "{{bearerToken}}" },
    "orderOfOperations": ["leadsAdd", "leadsAll", "leadsOne", "leadsUpdate", "leadsDelete"],
    "stripResponseExamples": true,
    "variableCasing": "camelCase"
  }
}
```

## Environment Variables

Variables prefixed with `PORTMAN_` in `.env` are auto-injected as camelCase Postman variables:

```
PORTMAN_CONSUMER_ID=test_user    → {{consumerId}}
PORTMAN_API_TOKEN=abc123         → {{apiToken}}
```

## CI/CD Integration

Store all options in a CLI options file:

```json
{
  "local": "./specs/crm.yml",
  "baseUrl": "https://staging-api.example.com",
  "output": "./output/crm.postman.json",
  "portmanConfigFile": "./config/portman-config.json",
  "envFile": "./.env",
  "includeTests": true,
  "runNewman": true
}
```

```sh
portman --cliOptionsFile ./portman-cli-options.json
```

## Testing Apideck APIs

```sh
# Test CRM API
portman -u https://specs.apideck.com/crm.yml -c ./portman-config.json -b https://unify.apideck.com -n true

# Test Accounting API
portman -u https://specs.apideck.com/accounting.yml -c ./portman-config.json -b https://unify.apideck.com -n true
```

## CLI Reference

| Flag | Description |
|------|-------------|
| `-l, --local` | Path to local OpenAPI spec |
| `-u, --url` | URL of remote OpenAPI spec |
| `-b, --baseUrl` | Override base URL |
| `-o, --output` | Output file path |
| `-c, --portmanConfigFile` | Path to portman-config |
| `-n, --runNewman` | Run Newman after generation |
| `-t, --includeTests` | Include test suite (default: true) |
| `-d, --newmanIterationData` | Path to iteration data |
| `--envFile` | Path to .env file |
| `--syncPostman` | Upload to Postman app |
| `--bundleContractTests` | Separate folder for contract tests |
| `--cliOptionsFile` | Path to CLI options file |
| `--init` | Interactive config wizard |
