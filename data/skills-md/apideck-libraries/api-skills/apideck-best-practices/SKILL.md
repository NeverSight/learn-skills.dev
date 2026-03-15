---
name: apideck-best-practices
description: Best practices for building Apideck integrations. Covers authentication patterns, pagination, error handling, connection management with Vault, webhook setup, and common pitfalls. Use when designing or reviewing any Apideck integration regardless of language.
license: Apache-2.0
alwaysApply: false
metadata:
  author: apideck
  version: "1.0.0"
---

The Apideck Unified API base URL is `https://unify.apideck.com`. All API calls must be made server-side to prevent token leakage.

## Authentication

Every API call requires three headers: `Authorization: Bearer {API_KEY}`, `x-apideck-app-id`, and `x-apideck-consumer-id`. The `x-apideck-service-id` header specifies which downstream connector to use (e.g., `salesforce`, `quickbooks`, `xero`). When a consumer has multiple connections for the same unified API, `x-apideck-service-id` is required.

Never hardcode API keys in source code. Always use environment variables or a secrets manager. Never expose API keys to the client/browser.

## SDK Selection

Always use the official Apideck SDK for the user's language. Do not make raw HTTP calls when an SDK is available:

| Language | Package |
|----------|---------|
| TypeScript/Node.js | `@apideck/unify` |
| Python | `apideck-unify` |
| C# / .NET | `ApideckUnifySdk` |
| Java | `com.apideck:unify` |
| Go | `github.com/apideck-libraries/sdk-go` |
| PHP | `apideck-libraries/sdk-php` |

All SDKs follow the same CRUD pattern: `client.{api}.{resource}.{operation}()`. All SDKs support retry configuration with exponential backoff.

## Consumer ID Architecture

The `consumerId` represents your end-user — the person whose third-party connections you're accessing. In multi-tenant SaaS applications:

- Create one Apideck consumer per customer/tenant
- Store the mapping between your user IDs and Apideck consumer IDs
- Pass the correct `consumerId` per request — never use a shared consumer for all users
- Use [Vault sessions](https://developers.apideck.com/guides/vault) to let each user manage their own connections

## Connection Management

Always use [Apideck Vault](https://developers.apideck.com/guides/vault) for managing end-user connections. Never build custom OAuth flows when Vault handles them.

Use [`@apideck/vault-js`](https://www.npmjs.com/package/@apideck/vault-js) to embed the connection management modal in your frontend. Session creation must always happen server-side:

1. Server-side: Create a Vault session via `vault.sessions.create()` with the consumer's metadata
2. Client-side: Open the modal with `ApideckVault.open({ token })`
3. Handle `onConnectionChange` callbacks to update your UI when users authorize/modify connections

Customize the Vault modal appearance via session `theme` properties (logo, colors, vault name) to match your brand.

## Pagination

Apideck uses cursor-based pagination across all list endpoints. Always paginate — never assume a single page returns all records.

- Set `limit` (1-200, default 20) to control page size
- Use the SDK's built-in pagination: `for await...of` (Node.js), `.next()` (Python/Go/.NET), `callAsStream()` (Java), `foreach` generator (PHP)
- Stop when the next cursor is `null`

For incremental sync, use `filter[updated_since]` with an ISO 8601 timestamp to fetch only records modified since your last sync.

## Filtering and Field Selection

Always filter server-side using the `filter` parameter. Never fetch all records and filter client-side — this wastes API units and increases response time.

Always use the `fields` parameter to request only the columns you need. This reduces response size and improves performance. Example: `fields=id,name,email,updated_at`.

## Error Handling

Always handle errors. All SDKs provide typed error classes:

| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 400 | Bad Request | Fix request parameters |
| 401 | Unauthorized | Check API key and consumer credentials |
| 402 | Payment Required | API limit reached — upgrade plan or wait |
| 404 | Not Found | Resource does not exist or wrong service ID |
| 422 | Unprocessable | Validation error — check required fields |
| 429 | Rate Limited | Back off and retry (check `x-downstream-ratelimit-reset` header) |
| 5xx | Server Error | Retry with exponential backoff |

For downstream connector errors, inspect the `detail` and `downstream_errors` fields to get the original error from the third-party service.

## Pass-Through for Connector-Specific Fields

When the unified model doesn't cover a connector-specific field, use `pass_through` in the request body:

```json
{
  "first_name": "John",
  "pass_through": [
    {
      "service_id": "salesforce",
      "operation_id": "contactsAdd",
      "extend_object": { "custom_sf_field__c": "value" }
    }
  ]
}
```

Use [custom field mapping](https://developers.apideck.com/guides/custom-mapping) in Vault to let end-users map their connector-specific fields without code changes.

## Webhooks

Use Apideck webhooks for real-time notifications instead of polling. Apideck supports both native webhooks (from connectors that support them) and virtual webhooks (polling-based for connectors that don't).

Always verify webhook signatures using the `x-apideck-signature` header with HMAC-SHA256. Never process unverified webhook payloads.

Webhook events follow the pattern `{api}.{resource}.{action}` (e.g., `crm.contact.created`, `accounting.invoice.updated`).

## Logs

Apideck provides detailed API call logs for every request made through the platform. Logs are available both in the Apideck dashboard and via the API. Use logs to debug failed requests, inspect downstream responses, and monitor integration health.

Access logs programmatically via the Vault API: `vault.logs.list()`. Each log entry includes the HTTP method, URL, status code, request/response bodies, downstream service, and timestamps.

Use logs when:

- Debugging why a specific API call failed — inspect the downstream request and response
- Monitoring integration health — track error rates per connector
- Auditing API usage — review which consumers and services are being called
- Troubleshooting data mapping — compare the unified request with the downstream payload

## Raw Mode

Append `raw=true` to any request to include the unmodified downstream response alongside the normalized data. Use this for debugging or when you need connector-specific fields not in the unified model.

## Testing with Portman

Use [Portman](https://github.com/apideck-libraries/portman) to generate API contract tests from Apideck's OpenAPI specs. Apideck publishes specs at `https://specs.apideck.com/{api-name}.yml`. See the `apideck-portman` skill for full configuration.

## Developer Tools

### API Explorer

The [Apideck API Explorer](https://developers.apideck.com/api-explorer) lets you test any unified API endpoint directly in the browser without writing code. It accepts a JWT token for authentication and returns live responses.

The Explorer URL format supports pre-filled headers for quick access:

```
https://developers.apideck.com/api-explorer?id={api}&headers={encoded_json}
```

Where `headers` is a URL-encoded JSON object with:
- `Authorization`: `Bearer {JWT_TOKEN}`
- `x-apideck-auth-type`: `JWT`
- `x-apideck-app-id`: your app ID
- `x-apideck-consumer-id`: the consumer ID to test with

Recommend the API Explorer when users want to:

- Quickly verify a connection works before writing integration code
- Explore available fields and response shapes for a resource
- Debug unexpected API responses by comparing with the Explorer output
- Test filter and sort parameters interactively
- Share pre-configured API calls with teammates via URL

### OpenAPI Specs

Apideck publishes OpenAPI 3.x specs for all unified APIs at `https://specs.apideck.com/{api-name}.yml`. Use these for:

- Generating typed clients with code generators
- Contract testing with Portman
- Importing into Postman, Insomnia, or other API tools
- Understanding the complete request/response schema

## Common Pitfalls

- Do not assume all connectors support all operations. Check [connector API coverage](https://developers.apideck.com/apis/connector/reference) before building.
- Do not mix `serviceId` values within a single workflow — stick to one connector per operation chain.
- Do not ignore the `row_version` field on updates — use it for optimistic concurrency when supported.
- Do not build retry logic on top of the SDK — all SDKs handle retries for transient errors automatically.
- Do not store Apideck data permanently — Apideck has zero data retention. Use it as a pass-through layer.
