---
name: openapi-review
description: >-
  Review OpenAPI (Swagger) specification files for compliance with the OpenAPI
  3.1 standard, security scheme design, naming conventions, schema quality, and
  API design best practices. Use when a user asks to review an API spec, check
  an OpenAPI file, audit a Swagger definition, validate an OAS document, or
  improve API design. Accepts YAML or JSON files, file paths, or inline spec
  content.
---

# OpenAPI Specification Review

Review OpenAPI specification files systematically for standards compliance,
security, API design best practices, and documentation quality.

## Input Handling

Determine the input type and gather the specification accordingly:

1. **Direct content** -- Spec provided inline in the conversation. Review as-is.
2. **File path(s)** -- Read the specified `.yaml`, `.yml`, or `.json` files.
3. **Directory path** -- Find all OpenAPI spec files recursively. If multiple
   specs are found, ask the user which to review.
4. **URL** -- If given a URL, ask the user to provide the file content directly.

Before starting the review phases, determine:

- **Format**: YAML or JSON
- **Version**: OpenAPI 2.0 (Swagger), 3.0.x, or 3.1.x
- **Structure**: Single document or multi-file with `$ref` to external files

If the spec uses OpenAPI 2.0 or 3.0.x, note version-specific differences and
recommend migration paths to 3.1.x where beneficial.

## Review Process

Read [references/openapi-checklist.md](references/openapi-checklist.md) before
starting the review.

Execute these phases in order. For each finding, assign a severity.

### Phase 1: Structural Compliance

Verify the spec conforms to the OpenAPI 3.1 specification structure:

- **Required fields** -- `openapi` version string, `info.title`,
  `info.version`, and at least one of `paths`, `components`, or `webhooks`
- **`$ref` resolution** -- All `$ref` pointers resolve to valid targets.
  No circular references that would prevent schema validation
- **Path templating** -- Path parameters match `{paramName}` syntax and have
  corresponding parameter definitions. No duplicate paths after template
  resolution
- **Parameter uniqueness** -- Parameters are unique by the combination of
  `name` and `in` (location) within each operation
- **operationId uniqueness** -- Every `operationId` is unique across the
  entire spec
- **Parameter schema** -- Parameters use `schema` for simple values or
  `content` for complex serialization, never both
- **Media types** -- Request/response `content` keys are valid media types
  (e.g., `application/json`, not invented types)
- **Status codes** -- Response status codes are valid HTTP codes or `default`.
  Range codes (`2XX`, `4XX`) used correctly

### Phase 2: Security Review

Check security definitions and their application:

- **Schemes defined** -- At least one security scheme exists in
  `components/securitySchemes`
- **Global or per-operation security** -- Security is applied globally or on
  every operation. Flag any operation missing security that does not
  explicitly opt out with an empty array `[]`
- **OAuth2 flows** -- OAuth2 schemes have valid flow configurations with
  proper authorization and token URLs. Scopes are defined and used
  consistently
- **API key placement** -- API keys use `header` or `cookie`, not `query`
  (query params appear in logs and browser history)
- **HTTPS enforced** -- All `servers[].url` values use `https://`. Flag any
  `http://` URL that is not `localhost` or `127.0.0.1`
- **Sensitive data exposure** -- Sensitive identifiers (passwords, tokens,
  secrets) are not in path or query parameters. Use headers or request body
  instead
- **CORS considerations** -- If the API is consumed by browsers, note if
  security-relevant headers are missing from response definitions

### Phase 3: API Design Best Practices

Evaluate the API design for RESTful conventions and consistency:

- **Resource naming** -- Paths use plural nouns (`/users`, not `/user`), no
  verbs in paths (`/users`, not `/getUsers`), lowercase with hyphens for
  multi-word segments (`/user-profiles`, not `/userProfiles`)
- **Naming consistency** -- Property names follow a single convention
  throughout (camelCase or snake_case, not mixed). Flag inconsistencies
- **HTTP method usage** -- GET for retrieval (no request body), POST for
  creation, PUT for full replacement, PATCH for partial update, DELETE for
  removal. Flag misuse (e.g., POST for retrieval)
- **Pagination** -- List endpoints (GET returning arrays) include pagination
  parameters (`limit`, `offset` or `cursor`) and response metadata
- **Status codes** -- Appropriate codes per method: 201 for POST creation,
  204 for DELETE with no body, 404 documented for resource endpoints, 409
  for conflict scenarios
- **Versioning** -- Consistent versioning strategy (URL path `/v1/`, header,
  or query param). Flag mixed approaches
- **Component reuse** -- Shared schemas, parameters, and responses defined in
  `components` and referenced via `$ref`. Flag inline duplication of
  identical or near-identical schemas
- **operationId conventions** -- operationIds are descriptive and follow a
  consistent pattern (e.g., `listUsers`, `getUserById`, `createUser`)
- **Descriptions** -- All operations, parameters, and schemas have
  meaningful `description` fields. Flag missing descriptions on public-facing
  endpoints

### Phase 4: Schema and Documentation Quality

Assess schema completeness and documentation:

- **Schema completeness** -- Schemas define `type`, use `format` where
  appropriate (e.g., `date-time`, `email`, `uri`, `uuid`), set `required`
  arrays for mandatory properties, define `enum` for fixed value sets, and
  provide `example` or `examples` values
- **Discriminator usage** -- Polymorphic schemas (`oneOf`, `anyOf`) use
  `discriminator` with a valid `propertyName` and optional `mapping`
- **Request/response examples** -- Operations include `example` or
  `examples` in media type objects. Examples are realistic and consistent
  with schema constraints
- **Error responses** -- 4xx and 5xx responses are defined with consistent
  error schemas (e.g., `title`, `status`, `detail` following RFC 9457
  Problem Details). At minimum, 400, 401, 404, and 500 are documented
- **Deprecated operations** -- Deprecated operations are marked with
  `deprecated: true` and their description states the replacement
  endpoint or migration path
- **External documentation** -- Complex or domain-specific operations link
  to external docs via `externalDocs` where helpful
- **`additionalProperties`** -- Object schemas explicitly set
  `additionalProperties` to `true` or `false` rather than relying on
  default behavior, especially for schemas used in request validation
- **String constraints** -- String properties define `minLength`,
  `maxLength`, or `pattern` where appropriate to communicate validation
  rules to consumers

## Severity Levels

Assign one severity to each finding:

| Severity | Label | Meaning |
|----------|-------|---------|
| S1 | CRITICAL | Spec is invalid, security scheme is missing or broken, or will cause code generation failures. Fix immediately. |
| S2 | HIGH | Likely to cause integration issues, security weakness, or incorrect client behavior. Fix before publishing. |
| S3 | MEDIUM | Design inconsistency, missing documentation, or deviation from best practices. Should be addressed. |
| S4 | LOW | Style suggestion, minor naming improvement, or optional enhancement. Address at discretion. |

## Output Format

Structure the review as follows:

### Summary

Provide a 2-3 sentence overview: what API the spec describes, overall quality
assessment, and the most important finding.

### Findings

List each finding with this structure:

**[S{n}] {Category}: {Brief title}**
- **Location**: JSON Pointer path (e.g., `#/paths/~1users/get/responses`) or
  object name
- **Issue**: What is wrong and why it matters
- **Suggestion**: Concrete fix, with a YAML or JSON snippet when helpful

Order findings by severity (S1 first), then by location within each severity.

### Positive Observations

Note 1-3 things the spec does well. Good component reuse, thorough examples,
or consistent naming deserve acknowledgment.

### Summary Table

End with a count table:

| Severity | Count |
|----------|-------|
| S1 CRITICAL | n |
| S2 HIGH | n |
| S3 MEDIUM | n |
| S4 LOW | n |

## Guidelines

- Be specific. Reference exact paths, property names, and operationIds.
- Provide concrete fix suggestions with YAML or JSON snippets demonstrating
  the improvement.
- When the spec uses OpenAPI 3.0.x, note 3.1.x features that would improve
  it (e.g., `null` type support, JSON Schema alignment) but focus the review
  on the version actually used.
- Do not flag valid style choices that are internally consistent (e.g.,
  camelCase vs snake_case is fine if used consistently throughout).
- For large specs (>100 paths), divide the review into logical sections
  (by tag or resource group) and provide a consolidated summary.
- When uncertain about API domain intent, state the assumption explicitly
  rather than making a silent judgment.
