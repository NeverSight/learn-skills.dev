---
name: openapi
description: 'OpenAPI 3.1 specification, schema design, and code generation. Use when designing REST APIs, generating TypeScript clients, or creating API documentation. Use for openapi, swagger, api-spec, schema, code-generation, api-docs, openapi-typescript, zod-openapi.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://spec.openapis.org/oas/v3.1.0'
user-invocable: false
---

# OpenAPI

## Overview

OpenAPI Specification (OAS) 3.1 is the industry standard for describing HTTP APIs. It defines a machine-readable contract covering endpoints, request/response schemas, authentication, and error formats. OpenAPI 3.1 is a strict superset of JSON Schema Draft 2020-12, enabling full JSON Schema compatibility for data validation and type generation.

**When to use:** Designing REST APIs, generating typed clients (TypeScript, Python, Go), producing interactive documentation, validating request/response payloads, contract-first API development, API gateway configuration.

**When NOT to use:** GraphQL APIs (use the GraphQL schema), gRPC services (use Protocol Buffers), WebSocket-only protocols, internal function calls that never cross a network boundary.

## Quick Reference

| Pattern         | Element                                                 | Key Points                                         |
| --------------- | ------------------------------------------------------- | -------------------------------------------------- |
| Document root   | `openapi`, `info`, `paths`                              | `openapi: '3.1.0'` required at top level           |
| Path item       | `/resources/{id}`                                       | Curly braces for path parameters                   |
| Operation       | `get`, `post`, `put`, `delete`, `patch`                 | Each operation needs `operationId` and `responses` |
| Parameters      | `in: path\|query\|header\|cookie`                       | Path params are always `required: true`            |
| Request body    | `requestBody.content`                                   | Keyed by media type (`application/json`)           |
| Response        | `responses.200.content`                                 | At least one response required per operation       |
| Component ref   | `$ref: '#/components/schemas/Name'`                     | Reuse schemas, parameters, responses               |
| Schema types    | `type: string\|number\|integer\|boolean\|array\|object` | Arrays support `type: ["string", "null"]` in 3.1   |
| Composition     | `oneOf`, `anyOf`, `allOf`                               | Model polymorphism and intersection types          |
| Discriminator   | `discriminator.propertyName`                            | Hint for code generators with `oneOf`/`anyOf`      |
| Security        | `securitySchemes` + top-level `security`                | Bearer, API key, OAuth2, OpenID Connect            |
| Tags            | `tags` on operations                                    | Group operations for documentation                 |
| Type generation | `openapi-typescript`                                    | Zero-runtime TypeScript types from spec            |
| Typed fetch     | `openapi-fetch`                                         | Type-safe HTTP client using generated types        |
| React Query     | `openapi-react-query`                                   | Type-safe React Query hooks from spec              |
| Schema-first    | `zod-openapi`                                           | Generate OpenAPI documents from Zod schemas        |

## Common Mistakes

| Mistake                                    | Correct Pattern                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| Using `nullable: true` in 3.1              | Use `type: ["string", "null"]` (3.0 syntax removed)                            |
| Missing `operationId` on operations        | Always set unique `operationId` for code generation                            |
| Path parameter not in `required`           | Path parameters are always required (`required: true`)                         |
| Inline schemas everywhere                  | Extract to `components/schemas` and use `$ref`                                 |
| `allOf` with conflicting `required` fields | Merge `required` arrays; `allOf` unions them                                   |
| Discriminator without shared property      | All schemas in `oneOf`/`anyOf` must include the discriminator property         |
| Empty `description` on responses           | Every response needs a meaningful `description`                                |
| Using `type: object` without `properties`  | Always define `properties` or use `additionalProperties`                       |
| Circular `$ref` chains                     | Break cycles with lazy resolution or restructure schemas                       |
| Mixing 3.0 and 3.1 syntax                  | Choose one version; 3.1 drops `nullable`, changes `exclusiveMinimum` to number |

## Delegation

- **API design review**: Use `Task` agent to audit spec completeness and consistency
- **Type generation**: Use `Explore` agent to find project-specific OpenAPI tooling config
- **Code review**: Delegate to `code-reviewer` agent for generated client usage patterns

> If the `typescript-patterns` skill is available, delegate advanced TypeScript typing questions to it.

## References

- [Schema design: paths, operations, parameters, components, and $ref](references/schema-design.md)
- [Data types: formats, composition, discriminators, and nullable](references/data-types.md)
- [Code generation: openapi-typescript, openapi-fetch, openapi-react-query, and Zod OpenAPI](references/code-generation.md)
- [Documentation: Swagger UI, Redoc, and API docs best practices](references/documentation.md)
