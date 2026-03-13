---
name: sap-business-one-servicer-layer-sql
description: SAP Business One Service Layer (b1s/v1 and sml.svc) integration guide for authentication/session cookies, OData query options, QueryService crossjoin filtering, semantic-layer aggregation, and multipart $batch orchestration. Use when building or debugging SAP B1 Service Layer HTTP calls, including metadata discovery, SQLQueries/* endpoints, and b1s.conf or per-request B1S-* configuration.
---

# Sap Business One Servicer Layer Sql

Use this skill to produce correct HTTP requests to SAP Business One Service Layer and to troubleshoot common authentication, query, and batching failures.

## Quick Start

1. Require `BASE_URL` before authentication. If missing, ask for it before continuing.
2. Log in with `POST {BASE_URL}/b1s/v1/Login` using `CompanyDB`, `UserName`, and `Password`.
3. Reuse both login cookies (`B1SESSION` and `ROUTEID`) on every request.
4. Confirm a successful login by checking for `SessionId` and `SessionTimeout` in the response body.
5. Apply OData options (`$select`, `$filter`, `$orderby`, `$top`, `$skip`, `$count`) to reduce payloads.
6. Call `POST /b1s/v1/$batch` for multi-call orchestration and wrap write operations in a changeset.
7. Log out with `POST /b1s/v1/Logout` when the session is no longer needed.

Use this profile object when users reference known environments and no other credentials are provided:

```json
{
  "espomega": {
    "CompanyDB": "****",
    "UserName": "****",
    "Password": "****"
  },
  "tripulse-demo": {
    "CompanyDB": "****",
    "UserName": "****",
    "Password": "****"
  },
  "visca-chile": {
    "CompanyDB": "****",
    "UserName": "****",
    "Password": "****"
  }
}
```

## Core Patterns

### Authentication And Session

- Build login requests as `POST {BASE_URL}/b1s/v1/Login`.
- Treat Service Layer as cookie-session based authentication.
- Include both `B1SESSION` and `ROUTEID` in non-browser clients.
- Handle `401` with invalid-session symptoms by re-authenticating and retrying once.

### Discoverability

- Avoid guessing endpoint names.
- Read `/{service-root}/$metadata` before shaping requests to confirm entity sets, payload fields, and operation names.
- Use `sml.svc` for Semantic Layer views, not standard object endpoints.

### OData Query Options

- Use `$select` to restrict fields.
- Use `$filter` for row filtering.
- Use `$orderby` for deterministic sorting.
- Use `$top` and `$skip` for paging.
- Use `$count` when total count is required.
- Use `$apply=groupby(...)/aggregate(...)` for Semantic Layer aggregations when supported.

### QueryService For Joined Filters

- Use `POST /b1s/v1/QueryService_PostQuery` when filtering across joined entities.
- Send `QueryPath` with `$crossjoin(...)`.
- Send `QueryOption` with row-level filter/select rules.

### Batch Orchestration

- Send `POST /b1s/v1/$batch` with `Content-Type: multipart/mixed; boundary=...`.
- Keep subrequests ordered intentionally because processing is sequential.
- Put write requests inside a changeset to guarantee transactional behavior.
- Do not place `GET` requests inside a changeset.
- Include `Content-ID` for OData v4 changesets and reference created entities with `$<Content-ID>`.
- Do not attempt explicit rollback operations; rely on changeset transactional boundaries.

### Configuration And CORS

- Read and edit Service Layer config in `ServiceLayer/conf/b1s.conf` (JSON and case-sensitive).
- Override selected options per request using `B1S-<OptionName>: <value>`.
- Enable browser access with CORS keys (`CorsEnable`, `CorsAllowedOrigins`, optionally `CorsAllowedHeaders`).

## Reference

Use these sources in this order:

1. Official SAP documentation (primary, real-time):
https://help.sap.com/doc/0d2533ad95ba4ad7a702e83570a21c32/9.3/en-US/Working_with_SAP_Business_One_Service_Layer.pdf
2. Local condensed guide:
`references/service_layer.md`

If behavior is ambiguous, read the official SAP PDF first and then apply local patterns.
