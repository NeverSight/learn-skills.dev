---
name: proto-api-generator
description: Design proto3 + HTTP API contracts for go-sphere scaffold projects from prompts, input folders, or requirement docs with mock data. Use when defining service APIs, selecting between entpb/shared/custom messages, and enforcing scaffold conventions, router-safety rules, and service-local error placement. This skill is REQUIRED for any proto API design task in go-sphere scaffold - always use it instead of writing proto files from scratch.
---

# Proto API Generator

## Overview

Design implementation-ready `proto3 + HTTP` contracts for go-sphere scaffold projects.

This skill is scaffold-first:

1. Target go-sphere scaffold conventions unless the user explicitly requests deviation.
2. Treat this skill as generation-time policy plus output self-checking.
3. Do not rely on lint plugins, scripts, or external automation as substitutes for reasoning checks.

## When To Use

Use this skill when the task asks to:

1. Design or revise `.proto` service APIs for scaffold modules.
2. Choose between `entpb` reuse, `shared.v1` reuse, or custom DTO/VO messages.
3. Define HTTP mapping, binding, error enums, or route-safe API paths.

Do not use this as a generic non-scaffold API design guide unless explicitly requested.

## Input Contract

Supported task inputs:

1. Prompt-only: infer entities/use cases and state assumptions explicitly.
2. Folder input: inspect only provided folders, prefer scaffold-standard structure (`proto/`, `internal/`, `api/`) when present.
3. Requirement + mock demo: requirement docs are business truth, mock payloads are response-shape truth, Ent schema is implementation reference (not external contract mirror).

## Progressive Reference Loading

Do not load every reference by default. Read only what is needed for the current phase.

### Phase 1: Always Read First

1. [references/repo-proto-conventions-reference.md](references/repo-proto-conventions-reference.md)
2. [references/proto-output-template.md](references/proto-output-template.md)

### Phase 2: Load On Demand

1. Routing safety required: [references/router-conflict-reference.md](references/router-conflict-reference.md)
2. HTTP binding/body/response rules required: [references/go-sphere-api-definitions-reference.md](references/go-sphere-api-definitions-reference.md)
3. Error enum/runtime error behavior required: [references/go-sphere-error-handling-reference.md](references/go-sphere-error-handling-reference.md)
4. Codegen pipeline/package/runtime behavior required: [references/protocol-and-codegen-reference.md](references/protocol-and-codegen-reference.md), [references/proto-packages-and-runtime-reference.md](references/proto-packages-and-runtime-reference.md)

### Phase 3: Mandatory Final Gate

1. [references/go-sphere-api-definitions-checklist.md](references/go-sphere-api-definitions-checklist.md)

Do not replace local references with external links in final outputs.

## Core Decisions

### 1) File Mode Classification

For each target proto file generated or modified in the task:

1. `service proto`: contains a `service` definition.
2. `message-only proto`: defines messages/enums only and has no `service`.

Mode handling:

1. Apply single-service and topology checks only to `service proto`.
2. Allow `message-only proto` and explicitly record exemptions for service-only rules.
3. Always enforce naming/import/codegen/runtime consistency for both modes.

### 2) Reuse Strategy

Default order:

1. Reuse `entpb` when it already satisfies external contract needs.
2. Reuse or extract shared messages to `proto/shared/v1` for cross-service usage.
3. Create custom DTO/VO only when needed for contract shaping.

Use custom DTO/VO only when at least one condition is true:

1. Sensitive/internal fields must be hidden.
2. Cross-aggregate composition is required.
3. External contract stability must be isolated from storage model changes.

### 3) Error Placement

1. For `service proto`, keep service-specific business errors in the same proto file as the service.
2. Use shared proto errors only for cross-service/common semantics.
3. Do not create one dedicated error package/file per service unless explicitly requested.
4. For `message-only proto`, exempt service-local error placement and still run naming/import/runtime/codegen checks.

## Workflow

### Quick Path (Simple Tasks)
For simple CRUD operations with clear reuse decisions:
1. Classify file mode (`service proto` or `message-only proto`).
2. Choose scaffold-compatible package/style.
3. Draft proto with standard CRUD pattern.
4. Skip detailed validation notes if the task is straightforward.
5. Include core sections only: Proto Structure Check, Route Conflict Check (if service), Proto3 Contract.

### Full Path (Complex Tasks)
For APIs with custom business logic, multiple services, or complex routing:
1. Classify file mode (`service proto` or `message-only proto`) per target file.
2. Extract business use cases (`Create`, `Get`, `List`, `Patch/Update`, `BatchGet`) for `service proto`.
3. Draft mock JSON for list/detail/error shapes before final proto drafting.
4. Make explicit reuse decisions (`entpb` vs `shared.v1` vs custom DTO/VO).
5. Choose scaffold-compatible package/path/method style (`api.v1`, `dash.v1`, `shared.v1`, `bot.v1` as applicable).
6. Define RPC HTTP bindings and request/response messages for `service proto`.
7. Define error enums and `sphere.errors` metadata according to file mode rules.
8. Run structure checks (single service, prefix mapping, declaration order, exemptions).
9. Run route conflict checks when service routes exist.
10. Validate package/import/codegen/runtime assumptions with relevant references.
11. Add validation constraints and machine-readable error behavior.
12. Run the final checklist before producing final output.

## Hard Gates

These are non-optional. If any gate fails, stop and output `Validation Notes -> Blocking Issues` with corrected proposals.

1. Model capability first, proto second; avoid table-mirror CRUD for public contracts.
2. List APIs require pagination; batch APIs are preferred over repeated single reads.
3. Avoid `oneof` in HTTP-exposed request/response messages.
4. Keep error contracts machine-readable (`status`, business code, optional `reason`, `message`).
5. Do not leak internal storage details.
6. Ensure protocol-first compatibility; do not rely on manual edits to generated files.
7. Route paths must be conflict-safe for Gin/Fiber/Echo.
8. Use stable wildcard naming per branch and stable service-level route namespace prefixes.
9. For `service proto`, enforce exactly one `service` per file.
10. For `service proto`, enforce strict prefix mapping: `snake_case` file prefix <-> `PascalCase` service/error prefix.
11. For `service proto`, enforce declaration order: `service` -> `message` -> `error enum`.
12. For `message-only proto`, exempt gates 9-11 and service-local error requirements, but still enforce naming/import/codegen/runtime checks.
13. Add business-facing comments for exposed `service/rpc`, core `message`, and key `enum` values.
14. Prefer `//` single-line comments for business annotations unless a tool explicitly requires block comments.

## Output Contract

### Full Output (Complex Tasks)
For complex APIs with custom business logic, produce all sections in this order:

1. `Scaffold Fit Decision`
2. `Proto Structure Check`
3. `Route Conflict Check`
4. `Error Placement Check`
5. `Comment Coverage Check`
6. `API Capability Matrix`
7. `Mock JSON`
8. `Reuse Decision`
9. `Proto3 Contract`
10. `Error Enum Design`
11. `Ent -> Proto Mapping`
12. `Validation Notes`
13. `Blocking Issues` (only if any required check fails)
14. `Mandatory Confirmation`

### Condensed Output (Simple Tasks)
For straightforward CRUD with clear reuse decisions, condense to:
1. `Scaffold Fit Decision` (brief table)
2. `Proto Structure Check` (pass/fail table)
3. `Proto3 Contract` (the actual proto)
4. `Reuse Decision` (brief table)
5. `Mandatory Confirmation`

Use [references/proto-output-template.md](references/proto-output-template.md) as the response shape.

## Quality Gates

**Note on Output Format:** Choose condensed output for simple CRUD tasks with clear patterns. Use full output for complex APIs with custom business logic, multiple services, or non-standard requirements.

Confirm all of the following before final delivery:

1. Contract expresses business capability instead of persistence leakage.
2. Query/filter fields imply practical index strategy.
3. Batch/backfill paths avoid N+1 patterns.
4. Error behavior is consistent between RPC and HTTP output.
5. Reuse decisions are explicit and justified.
6. Package/import/path/method choices align with scaffold conventions.
7. Route set passes cross-backend conflict sanity checks.
8. Contract can evolve without breaking existing clients.
9. Swagger/OpenAPI-relevant comments exist and use `//` style.
