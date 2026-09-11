---
name: aip
description: "Design Google AIP resource APIs. Use for protobuf or REST resources, standard methods, HTTP bindings, fields, pagination, filtering, LROs, errors, compatibility, or batch APIs."
paths:
  - "**/*.proto"
  - "**/*openapi*.{yaml,yml,json}"
---

Approved General AIPs are normative. draft AIP-162 and reviewing AIP-182 are advisory; label them as such.

## Workflow

1. Read the proposed surface and nearby APIs; classify management versus data plane.
2. Walk all 72 `Use when` entries in [REFERENCE.md](REFERENCE.md). Record each AIP as selected or excluded; never apply every AIP blindly.
3. Open the official `https://google.aip.dev/{number}` page for every applicable AIP. Never cite the local index as evidence. Compare applicable-row URLs with the research trace and fetch every gap.
4. Resolve conflicts by approved AIP, documented compatibility need, then precedent exception. Mark necessary exceptions `aip.dev/not-precedent` with rationale.
5. Derive a change-specific checklist for proto/HTTP shape, behavior, errors, lifecycle, compatibility, docs, and client ergonomics.
6. Preserve intended capability and wire compatibility unless version policy permits a break.
7. Run the repository's `api-linter`; it is a floor, not proof of conformance.
8. Report `AIP | state | applicability | result | evidence/exception` for each applicable AIP. List every exclusion separately and account for all 72 published numbers exactly once. Separate normative failures from advisory suggestions.

## Baseline

- Model management APIs as named resources with standard methods.
- Use a canonical relative resource `name` and `(google.api.resource)`; reserve display text for `display_name`.
- Annotate request `name` with `resource_reference.type`. For List/Create, annotate `parent` with `resource_reference.child_type` when its type is undeclared or variable, otherwise the parent's `type`; never the child's `type`.
- Align HTTP paths, request fields, signatures, references, field behaviors, pagination, filtering, masks, errors, and LRO metadata.
- Import every introduced annotation or message.
- Preserve relative expiration: `oneof expiration` contains input-capable `Timestamp expire_time` and `Duration ttl [(google.api.field_behavior) = INPUT_ONLY]`; `expire_time` must not be `OUTPUT_ONLY`.
- Review compatibility beyond field numbers: names, types, formats, semantics, bindings, patterns, requiredness, and client behavior.
- Document visible semantics, validation, defaults, ordering, limits, side effects, errors, retention, and exceptions.

## Guardrails

- The catalog has 72 published General AIPs; never invent guidance for unassigned numbers.
- Apply conditional AIPs only when their trigger holds. Do not turn examples into requirements.
- Preserve approved **must**/**must not** language; distinguish **should** and exceptions.
- Recheck AIP-122 relative names and parent direction; AIP-127 and AIP-130 for HTTP-transcoded resource methods; AIP-134 optional update masks; AIP-154 etags; AIP-161 output-only input; AIP-192 public comments; AIP-203 `IDENTIFIER`; `client.proto` signatures; and AIP-214 expiration.
- Prefer an explicit compatibility adapter for legacy non-conformance.
