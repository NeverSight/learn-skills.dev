---
name: documenting-contracts
description: Use when documenting an HTTP API, message payloads, queue contracts, DTOs, file formats, or webhooks - or when writing the api-reference of a legacy campaign, or when callers keep asking what a field means or which errors an endpoint returns. Encodes the four detail levels, the DTO-first catalog, wire types with source anchors, the generated-spec one-home rule, and omitted-versus-null semantics. Use whenever a machine interface needs documenting for its callers, even if nobody says "API docs".
---

# Documenting contracts

**REQUIRED BACKGROUND:** the `technical-writing` skill (hard rules, truth rules, style).

## Overview

A contract document is read by a stranger who cannot see the code and is about to depend on it. Core principle: **document the wire, exhaustively, with each detail at its own level; the caller's language is the wire format and domain terms, never the implementation's types.** Contract surfaces are reference kind, so the core Reference rule applies: every endpoint, every field, every error.

## When to invoke, and not

Invoke when documenting anything machines call or parse: REST and RPC endpoints, message queues and topics, webhooks, CLI commands, file formats. The `api-reference.md` of a legacy campaign (`documenting-legacy-codebases`) is this skill's document. Do NOT invoke for internal code interfaces, which the code documents itself, or for configuration references, which belong in `config-reference.md` under the core Reference rule. Judging whether the contract is well designed is out of scope: this skill documents the contract that exists.

## One home versus generated specs

When an OpenAPI or AsyncAPI spec exists, or the code generates one, that spec owns the field tables. The markdown then documents only what the spec cannot say (semantics, side effects, ordering, omitted-versus-null) and links the spec; never hand-maintain field tables beside a generated one; a second home drifts. The catalog below is for the case where no machine spec exists; writing one is not this document's job.

## The four detail levels

Each level has its own home; the writer moves detail found at the wrong level into the level that owns it:

| Level | The caller asks | Home |
|---|---|---|
| Index | What exists here | The endpoint, message, and command tables |
| Semantics | What invoking it does | Per-endpoint, per-message, and per-command prose: side effects, events published, idempotency, redelivery, exit behavior, quirks |
| Shape | What crosses the wire | The DTO catalog: one field table per DTO |
| Example | What it looks like | At most one illustrative example per DTO |

Repetition across levels is the defect to hunt: an endpoint section restating its DTO's fields, an example smuggling in a field the table lacks.

## The DTO catalog

A DTO is defined once and referenced everywhere:

- **Wire types, not language types.** `string (date, ISO 8601)`, `number (64-bit integer)`, `string (decimal)`: the column says what crosses the wire, complete enough that no reader needs the implementation's type as a proxy. A 64-bit integer that exceeds the range or precision of a consumer's native number type is wire information; the type name that produced it is not.
- **One Source line per DTO**, naming the owning class or schema file. Reference kind sanctions this evidence anchor, as a config reference carries binding evidence.
- **Required is a tri-state**: `yes`, `no`, or `if <condition>` with the condition stated.
- **Omitted versus null is stated wherever it matters**, and always on a DTO used in a replace-style write, where an omitted field is absent from the result. Where the server assumes a value on omission instead, that value goes in the Default column.
- **Enums get their own table**, values with meanings; nested objects link to their own catalog entry, never a second inline copy.
- **Constraints in domain terms**: "past date", "1..100 chars", "must reference an existing budget policy", read from validation the code enforces.

## The template

```markdown
# API reference: <service>

## Conventions
[Once, never per endpoint: base path, auth, content type, the error
envelope, global (de)serialization behavior, idempotency defaults.]

## Endpoints
| Method | Path | Purpose | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | `/thing` | Create a thing | [ThingRequest](#thingrequest) | 200 [Thing](#thing) | 422, 404 |

### POST /thing
[Semantics only: side effects, events published, idempotency, quirks.
No field lists; the index and catalog are not repeated.]

## Messages
| Direction | Destination | Payload | Reply | On error |
|---|---|---|---|---|
| in | `thing.create` | [ThingRequest](#thingrequest) | `thing.created` | `thing.create.error` |

### thing.create
[Semantics only: redelivery, ordering, events published, quirks;
what differs from the sibling transport is called out here.]

## Commands
| Command | Purpose | Arguments | Output |
|---|---|---|---|

### <command>
[Semantics only: side effects, idempotency, exit behavior, quirks.]

## DTOs
### ThingRequest
Source: `api/ThingRequest`

| Field | Type | Required | Default | Constraints | Meaning |
|---|---|---|---|---|---|

[Omitted versus null, where it matters. At most one illustrative example.]

### Thing
[Response shapes are catalog entries like any other.]

## Errors
| Status | When | Body |
|---|---|---|
```

## Rules

- **Verify against the serializer, not the class.** The wire is what the configured serializer emits and accepts: a global trimmer, a null-omitting mapper, or a custom date format changes the contract without touching any DTO. Read the serialization configuration before writing a single field row.
- **Asymmetries are semantics.** The mutation that publishes an event on one transport and nothing on the other, or the endpoint that skips a step its siblings perform, is documented at the semantics level.
- **Examples are illustrative, never normative.** One per DTO at most, labeled so, and containing no field the table lacks; the table is the contract.
- **Errors are cataloged once**, as envelope plus a status table; an endpoint lists only which entries apply to it. Command failures are cataloged the same way, by exit code.
- **The exhaustiveness is checkable.** The endpoint count and the DTO count are denominators like any other (core truth rules): a legacy campaign records them in its coverage ledger with the commands behind them and the date.
