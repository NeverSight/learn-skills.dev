---
name: http-api-conventions
description: >-
  Design, implement, or review HTTP/JSON APIs. Use for request/response
  contracts, validation, error handling, pagination, authentication, or caching.
  Enforce consistent wire formats, omit absent values instead of encoding null,
  specific error codes, precise status semantics, and safe boundaries.
---

# HTTP API conventions

Use predictable, explicit wire contracts. Keep naming, validation, errors,
pagination, and caching consistent across endpoints. Read the repository's API
specification first; this skill supplies reusable defaults, not permission to
break an established client contract.

## Request and response conventions

- Version application routes under `/v1` by default. Introduce a new version
  deliberately for incompatible contract changes; keep health/readiness probes
  outside the versioned API path when required by platform conventions.
- Use `snake_case` for JSON body keys, including nested objects, and for query
  and path parameters unless the published API contract requires another form.
- Never encode an absent optional field as JSON `null` in API requests or
  responses. Omit the key. If a field is required, supply a valid value or
  return a validation error. At integration boundaries, parse the upstream
  representation and map it to this API's contract rather than relaying
  upstream absence conventions blindly.
- Use stable IDs (UUIDs where appropriate) and UTC ISO-8601 timestamps. Document
  exceptions in the API contract.
- Authenticate with the repository's established mechanism; browser session
  cookies must use appropriate `HttpOnly`, `Secure`, and `SameSite` settings.
- Cursor-paginate collections that can grow without bound. Use a consistent
  collection response with `data`, `next_cursor`, and `has_more`. Small,
  explicitly bounded collections may be returned without pagination.
- Return a single-resource domain object directly unless the API contract
  requires an envelope. Do not add a wrapper solely for symmetry with paginated
  collections.

## Error body

Every API error response uses this shape:

```json
{
  "message": "Mensagem legível para pessoas",
  "error_code": "EMAIL_ALREADY_REGISTERED"
}
```

`extra` is optional. Omit it when the code is already specific enough for the
client to choose its handling. A missing value must not be represented by a
JSON `null`; omit an optional key instead.

- `message` is for people, not client-side branching. Use the API's required
  human language; for the house convention, use PT-BR.
- `error_code` is how the client selects its handling, and it is specific in
  most cases. The code names one situation (`EMAIL_ALREADY_REGISTERED`,
  `<RESOURCE>_NOT_FOUND`); the client branches on it and does not parse
  `message`. A code is non-specific only for an unknown failure
  (`UNEXPECTED_ERROR`) or when `extra` complements it and carries the fact that
  distinguishes the case (`INVALID_PARAMS` with `validation_errors`, an
  integration code with a safe upstream detail). Name a known situation in the
  code. Return `UNEXPECTED_ERROR` for a situation that is not classified yet,
  until a specific code exists. Do not rename a shipped code without a
  compatibility plan with API consumers.
- `extra` complements a non-specific code with the fact the client needs. On a
  code that is already specific, it is optional safe context, such as a
  resource identifier, and is omitted when it adds nothing. Never put secrets,
  stack traces, raw internal errors, or sensitive payloads there.

## Status semantics

| Situation | HTTP | `error_code` | `extra` |
| --- | ---: | --- | --- |
| Missing/invalid authentication | 401 | `UNAUTHORIZED` or a stable auth code | Omit unless safe context is needed |
| Authenticated but not allowed | 403 | `PERMISSION_DENIED` | Omit unless safe context is needed |
| Resource does not exist | 404 | `<RESOURCE>_NOT_FOUND` | Omit unless safe context is needed |
| State conflict (already exists/decided) | 409 | Code that names the conflict, e.g. `EMAIL_ALREADY_REGISTERED` | Omit when the code already names it |
| Business precondition not satisfied | 412 | Code that names the precondition | Current safe state, when useful |
| Syntactically valid payload violates validation/business rules | 422 | `INVALID_PARAMS` | **Required:** `validation_errors` array |
| Malformed request (invalid JSON/encoding/corrupt body) | 400 | `MALFORMED_REQUEST` | Omit unless safe context is needed |
| Upstream dependency rejects/fails an operation | 502 | Our stable integration code | Safe upstream code/context, if useful |
| Unexpected or unmapped server error | 500 | `UNEXPECTED_ERROR` | Never expose stack or internal details |
| Derived resource generation fails | 500 | Code that names the failed operation | Safe limits/context, if useful |
| Request body exceeds configured size limit | 413 | `PAYLOAD_TOO_LARGE` | Omit unless safe context is needed |

Keep the distinctions precise:

- **400** means the request cannot be parsed or is malformed.
- **422** means parsing succeeded but the data violates validation or a business
  rule. Every 422 response includes `extra.validation_errors`, an array of
  `{ "field": "...", "message": "..." }` entries.
- **409** means the current resource state conflicts with the requested action.
  The code names which conflict.
- **412** means a prerequisite for the action has not been satisfied.
- **404** means the addressed resource does not exist.

## Upstream errors

Do not expose an upstream provider's code as this API's `error_code`. Classify
the outcome (for example, retryable vs. definitive), return a stable code owned
by this API, and place a safe upstream code in `extra` only when useful. Keep
internal endpoints, credentials, raw payloads, and sensitive provider details
out of responses.

## Signed webhook requests

Signed webhooks are protocol-defined request exceptions. Verify signatures
against the exact request bytes and canonicalization rules required by the
upstream protocol. Do not parse and reserialize, normalize field names, change
encoding, or otherwise transform the body before signature verification. After
verification succeeds, parse the payload and map it into internal domain types
and naming conventions. Keep secrets and full sensitive payloads out of logs.

## Centralize translation

Domain errors should carry a human message and a specific error code. Translate
them to `{ statusCode, body }` in one shared builder/adapter rather than
scattering HTTP status selection and response-envelope construction across
routes. Map schema-validation failures into the standard validation error
representation. The fallback for an unknown exception is a generic HTTP 500
response; log details through the server's protected logging path, never in the
response body.

## Cache boundary

Keep caching outside domain/business logic. Wrap a repository or query
interface with a cache decorator so callers do not need cache-specific branches.
Every write that changes a cached representation must invalidate or version the
corresponding entry at a centralized boundary; do not rely on TTL alone for
correctness. Use generation keys only when cache-key cardinality makes targeted
invalidation impractical, and store the generation outside an evicting cache.

## Review checklist

- Does every error use the shared body shape and a specific `error_code`?
- Does the status reflect the semantics, especially malformed 400 vs. invalid
  422 and conflict 409 vs. precondition 412?
- Does every 422 include `extra.validation_errors[]`?
- Are absent values omitted, with no JSON `null` in API request/response bodies?
- Can the client select its handling from a specific `error_code`, without
  parsing `message`? A code is non-specific only for `UNEXPECTED_ERROR` or when
  `extra` complements it with the distinguishing fact.
- Are upstream codes kept separate from this API's codes?
- Are application routes versioned, with only required platform probes outside
  the versioned path?
- Are signed webhook bodies verified before parsing or normalization?
- Are stack traces, internal messages, secrets, and sensitive payloads excluded
  from all public responses?
- Does one central translator/builder handle domain and framework errors?
- Are unbounded lists cursor-paginated and cache invalidation tied to writes?
