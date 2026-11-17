---
slug: api-doc-generator-partme-ai
displayName: 从代码和 OpenAPI 一键生成 API 文档：接口、参数、鉴权、响应与错误码
version: 1.0.0
summary: 自动扫描 OpenAPI、路由、控制器、模型、校验规则和测试，生成可追溯、可核验、可持续更新的完整 API 文档，告别接口遗漏、字段猜测和文档过期。
license: Apache-2.0
name: api-doc-generator
description: Generate or update evidence-backed API documentation from OpenAPI specifications, framework routes, controllers, request/response models, validation rules, and tests. Use when the user explicitly asks for API or interface documentation, route inventory, endpoint reference, OpenAPI-derived docs, or synchronization between code and API docs. Supports OpenAPI-first projects and framework-specific discovery for Spring, FastAPI, NestJS, Express, and Gin; do not use for generic product documentation.
---

# API Documentation Generator

Document APIs from authoritative artifacts and distinguish confirmed facts from inference.

## Source priority

Use the strongest available source in this order:

1. Checked-in OpenAPI/Swagger contract and generated schema.
2. Framework route definitions and annotations.
3. Request/response models and validation rules.
4. Authentication, middleware, exception handling, and error catalogs.
5. Integration and contract tests.
6. Runtime observations explicitly authorized by the user.

When sources disagree, report the mismatch instead of silently choosing one.

## Framework routing

Read only the relevant reference:

- OpenAPI-first: [`references/openapi-first.md`](references/openapi-first.md)
- Java/Kotlin Spring: [`references/spring.md`](references/spring.md)
- Python FastAPI: [`references/fastapi.md`](references/fastapi.md)
- TypeScript NestJS: [`references/nestjs.md`](references/nestjs.md)
- JavaScript/TypeScript Express: [`references/express.md`](references/express.md)
- Go Gin: [`references/gin.md`](references/gin.md)

Use [`references/scan-and-generate-example.md`](references/scan-and-generate-example.md) only when a complete worked example is useful.

For a checked-in OpenAPI document, generate a deterministic inventory before drafting prose:

```bash
python3 scripts/inventory_openapi.py path/to/openapi.yaml --output docs/api-inventory.md
```

The script refuses to overwrite an existing output unless `--force` is explicitly provided.

## Workflow

### 1. Inspect

1. Detect the project framework, modules, existing API contracts, and documentation convention.
2. Determine the requested scope from the user's wording; infer the whole API only when no narrower scope exists.
3. Locate route registration, base paths, version prefixes, security middleware, models, validators, error handling, and tests.
4. Identify generated files so they are not mistaken for the source of truth.

### 2. Build an endpoint inventory

For each endpoint capture:

| Field | Requirement |
|---|---|
| Method and path | Resolve all prefixes and route groups |
| Operation identity | Handler/controller and stable operation name |
| Purpose | Derive from code/comments; mark inference |
| Authentication | Scheme, scopes/roles, and public exceptions |
| Request | Path/query/header/cookie/body fields and validation |
| Response | Status codes, content types, schema, and wrappers |
| Errors | Only errors supported by handlers, middleware, tests, or catalogs |
| Evidence | Contract or source location used |

Do not fabricate example values, undocumented error codes, required flags, or response fields.

### 3. Resolve schemas

- Follow nested model references and generic response wrappers.
- Preserve nullable, optional, enum, format, range, and length constraints.
- Detect pagination and list-envelope conventions.
- Show recursive or polymorphic schemas explicitly.
- Redact secrets and personal data from examples.

### 4. Generate the document

Use the repository's existing convention. If none exists, copy one template from `assets/templates/` and write to a proposed path under `docs/`. Before writing, report the target and whether it already exists.

For every endpoint include:

1. Summary and evidence status
2. Method and full path
3. Authentication/authorization
4. Parameters and request body
5. Responses and supported errors
6. Minimal valid examples
7. Source location

### 5. Validate

- Compare documented routes with the discovered inventory.
- Verify path variables and request fields against validators/models.
- Verify response and error status codes against code or contract.
- Check internal links and anchors.
- Mark unresolved conflicts and inferred fields.
- Never claim runtime verification unless the API was actually run.

## Evidence labels

Use these labels when certainty matters:

- `已确认：契约` — present in the checked-in API contract.
- `已确认：源码` — present in route/model/handler source.
- `已确认：测试` — exercised by a test.
- `推断` — reasonable but not explicitly specified.
- `待确认` — conflicting or missing evidence.

## Completion contract

Report the generated/updated file, documented endpoint count, authoritative sources used, contract/source mismatches, inferred fields, and endpoints skipped because evidence was insufficient.
