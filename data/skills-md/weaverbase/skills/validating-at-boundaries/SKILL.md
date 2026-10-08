---
name: validating-at-boundaries
description: Use when defining or changing request bodies, query params, form input, environment or config parsing, external API responses, message payloads, or JSON data, or when adding Pydantic models, BaseSettings, Zod schemas, z.infer types, safeParse calls, unknown/any/raw dict inputs, or ad-hoc shape checks in services, handlers, or React components.
---

# Validating at Boundaries

## Overview

A data model is the single source of truth for both the shape and the validation of a concept. External data is checked once, at the boundary where it enters (or leaves) the system. Everything past that point works with validated, typed values and does not re-check them.

**Core principle:** Put structural validation on a schema at the boundary. Keep state-dependent rules in the application operations. Pass typed values inward.

Apply this to new or requested changes. Do not migrate working code unprompted.

## Stack References

Read every applicable stack reference before editing, reviewing, or giving implementation guidance. If unsure whether a reference applies, read it:

- Python and Pydantic v2 (`BaseModel`, `ConfigDict`, `BaseSettings`, `SettingsConfigDict`): [references/pydantic.md](references/pydantic.md)
- TypeScript and Zod 4 (schemas, `z.infer`, React boundaries, env parsing): [references/zod.md](references/zod.md)

## Who Validates What

| Owner | Validates |
| --- | --- |
| Schema at the boundary | Structure: types, required fields, length, format, unknown keys, coercion |
| Application operation | Domain invariants that need business context, persistence, authorization, or current system state |
| Components and presentational code | Nothing about external shape. They receive typed props |

## Rules

1. **Define each concept's shape once.** The schema is the source of the type; do not write a second hand-made type or checker next to it. Use Pydantic v2 in Python and Zod 4 in TypeScript.
2. **Validate at boundaries:** request bodies, query params, environment variables, external API responses, form inputs, message payloads, and JSON columns or tables written by other systems.
3. **Operations accept validated, typed models**, not raw `dict`, JSON, `unknown`, or `any`.
4. **Do not re-assert a constraint the schema already guarantees.** If `name` has a maximum length of 100 on the schema, the operation does not check the length again. Branching on legitimately optional or empty values (a nullable nickname, an empty list of order items) is domain logic and stays in the operation.
5. **Create and update payloads are separate concepts, not duplicates.** Reuse shared models, schemas, or constrained field types: subclass a Pydantic base where appropriate and reuse constrained aliases for nullable updates; derive Zod variants with `.extend()`, `.partial()`, `.pick()`, or `.omit()`. Do not copy constraints into separate definitions.
6. **Reject unknown keys on inbound request bodies.** Default stripping is acceptable for external API responses, where new upstream fields should not break you.
7. **Validate outbound data too.** Return explicit response models so internal fields, such as password hashes or internal IDs, cannot leak.
8. **Surface validation errors at the boundary** as 400 or 422 responses or as form errors. Operations raise domain errors, not validation errors.
9. **Trust data read back from your own database through your own models.** Map ORM rows to typed models in the persistence code that returns them. Do not re-parse them in operations.
10. **Validate configuration.** Read configuration from environment variables through a typed schema (Pydantic settings in Python, a Zod schema for `process.env` in TypeScript). Parse it once at startup or boundary initialization and pass typed values inward. Do not hardcode configuration values.

## Frontend Data

Parse external data where it enters the UI: route loaders, server actions, API-client adapters, form resolvers, or explicitly named boundary/container modules. Reusable and presentational components receive typed props.

Components must not:

- accept `unknown` or `any` for external data;
- call `parse` or `safeParse`;
- run `if (!value?.id)`-style shape guards;
- hide invalid external data by returning `null`.

If external data fails validation, surface the failure deliberately at the boundary (an error state, a form error, or a thrown error that an error boundary handles).

## Example

Good flow: the boundary validates once, the operation receives a typed value and enforces only domain rules.

```text
request body --> boundary: parse with CreateInvite schema (400/422 on failure)
             --> operation: createInvite(invite: CreateInvite)
                    - domain rule: reject a duplicate address (domain error)
             --> boundary: map the domain error to 409; serialize InviteOut
```

Bad flow: the operation takes `dict`/`unknown`, checks `"@" in email` and the name length itself, and returns the internal record. The shape then lives in three places and nothing stops internal fields from leaking.

Full code for both stacks is in the references.

## Red Flags

Stop and move the check onto a schema at the boundary if you think or see:

- "This is urgent, so validate directly where it is easy to see."
- "We can replace the raw `dict`/`any` with a schema later."
- "A quick `if (!value?.id)` check is enough for now."
- "I used `safeParse` and returned `null`, so the component is safe."
- "The old Pydantic `Config` class is shorter and familiar."
- "Hardcode config for speed" or "read the env value ad hoc where it is used."
- "The model is validated, but the service should check the length again to be safe."
- "This component is a boundary because I called it one."

## Rationalizations to Reject

| Rationalization | Response |
| --- | --- |
| "Since you are in a hurry, I will keep this minimal and validate directly where it is easy to see." | Boundary models are the minimal compliant path. Put structural validation on Pydantic/Zod and keep entry points thin. |
| "We can replace the raw `dict` with a Pydantic model later once the endpoint shape settles." | The shape is the contract. Define it once now and derive variants when needed. |
| "No time to add schemas, so I will guard the component locally." | Parse external input at the boundary with Zod/Pydantic; components consume typed data. |
| "I used `safeParse` and returned `null`, so the component is safe." | `safeParse` belongs at the boundary. Presentational components receive typed props and do not decide whether external data is structurally valid. |
| "The old Pydantic `Config` class is shorter and familiar." | Use Pydantic v2 `model_config` with `ConfigDict`, or `SettingsConfigDict` for settings models. |
| "Hardcoding the config is faster for now." | Validate environment configuration with a typed schema; do not hardcode configuration values. |

## Common Mistakes

- Moving validation from the boundary into an operation or a component because the check is small.
- Re-checking a constraint (length, format, required) that the schema already enforces.
- Calling an ordinary component a "boundary" so it can accept `unknown`/`any`, call `safeParse`, and hide invalid data by returning `null`. Validate in a real boundary or container module and surface failures deliberately.
- Using nested Pydantic `Config` classes instead of `model_config` with `ConfigDict` or `SettingsConfigDict` (see [references/pydantic.md](references/pydantic.md)).
- Copying field definitions into separate create and update models instead of deriving them from a shared base.
- Accepting unknown keys on inbound request bodies, or returning a full internal record instead of an explicit response model.
- Letting operations raise validation errors, or letting validation failures reach the client as unhandled server errors.
- Re-parsing rows read from your own database inside operations.
- Using unvalidated environment values or hardcoded configuration.
