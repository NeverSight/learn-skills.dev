---
name: documentation-api-reference
description: "Author API reference documentation that is accurate, complete, and implementation-aligned for client developers. Use when API docs are primary deliverables or must be updated for contract changes; do not use for implementing new product behavior."
---

# Documentation API Reference

## Overview
Use this skill to produce API references that enable clients to integrate correctly without reverse engineering source code.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Quality gates:
  - `references/api-doc-quality-gates.md`

## Templates And Assets
- API reference template:
  - `assets/api-reference-template.md`
- Error catalog template:
  - `assets/api-error-catalog-template.md`

## Inputs To Gather
- Current API contracts/specs and change diff.
- Authentication/authorization requirements.
- Request/response schemas, status codes, and error semantics.
- Versioning/deprecation policy.

## Deliverables
- Endpoint/operation reference with examples.
- Error code and retryability guidance.
- Version/deprecation notes and migration hints.
- Known limits and behavioral caveats.

## Quick Example Coverage Checklist
- Auth method and required headers.
- Request params/body schema with constraints.
- Success response + failure responses.
- Rate limits/idempotency behavior.
- Example curl/request/response snippets.

## Quality Standard
- Doc content matches actual contract behavior.
- Required fields/constraints are explicit.
- Error behavior is actionable for client developers.
- Examples are realistic and syntactically valid.

## Workflow
1. Diff contract changes and identify impacted sections.
2. Update operation docs with schema and behavior details using `assets/api-reference-template.md`.
3. Add/refresh example requests and responses, including error mapping in `assets/api-error-catalog-template.md`.
4. Validate consistency against source/spec with `references/api-doc-quality-gates.md`.
5. Publish with migration notes where applicable.

## Failure Conditions
- Stop when docs diverge from implemented contract.
- Stop when error semantics are undocumented for critical paths.
- Escalate when breaking changes lack migration guidance.
