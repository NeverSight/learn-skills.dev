---
name: oodle-o11y-context
description: Defines the O11y Change Context manifest — the structured PR block that carries a change's observability intent (type, touched services, telemetry added/changed, guarding alerts, watch items, gaps) from authoring through review into production triage. Referenced by oodle-o11y-review and oodle-triage.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,observability,sdlc,pr,change-context
  globs: ""
  alwaysApply: "false"
---

# O11y Change Context — Manifest Spine

This skill defines one thing: the **O11y Change Context** manifest, a small
structured block an authoring agent writes into a pull request description. It is
the connective tissue of the observability loop — the left-side reviewer
([oodle-o11y-review](../oodle-o11y-review/SKILL.md)) enriches it, and the
right-side triage ([oodle-triage](../oodle-triage/SKILL.md)) reads it back when
an alert fires. This skill carries no instrumentation how-to; it is a shared
contract the other two skills reference.

Write the block only when it is warranted (see [Relevance gate](#relevance-gate)).
Its value is that a change's *observability intent* survives from the moment it is
authored to the moment it breaks in production.

## The block

Put this fenced block in the PR description. Keep the `## O11y Change Context`
header and the field keys exactly as written — downstream agents locate and parse
the block by this shape.

```markdown
## O11y Change Context
type: perf, bugfix                 # bugfix | perf | feature | critical-path | refactor | infra
touches: checkout-svc, order-repo  # deploy/service units changed
telemetry:
  + span checkout.place_order {attr: tenant, order_id}   — trace slow orders per tenant
  ~ metric checkout_latency_seconds (histogram)          — widened buckets; guards SLO
  - metric checkout_legacy_timer                          — removed; duplicate of above
guarded-by: SLO checkout-p99, monitor HighCheckoutLatency  # existing alerts over touched code
watch: N+1 on order lookup under load; cache hit-rate regression
gaps: no per-item span in the loop — deferred (cardinality); triage can't attribute per-SKU
```

- `telemetry` lines start with `+` (added), `~` (changed), or `-` (removed),
  followed by the signal and a short **purpose**. A signal whose purpose cannot
  be stated probably should not exist.
- Omit a field only when it genuinely has no content (e.g. no `gaps`). Never
  rename a field.

## Field reference

| Field | Meaning | Filled by | Why it matters downstream |
|-------|---------|-----------|---------------------------|
| `type` | Nature of the change | Author | Sets scrutiny level for review and triage. `critical-path` earns the deepest review. |
| `touches` | Deploy/service units changed | Author | Triage matches a firing alert's service to recent changes here. |
| `telemetry` | Signals added / changed / removed, each with a purpose | Author (drafts), Review (verifies) | Enforces "every signal serves a purpose, no duplicates." |
| `guarded-by` | Existing alerts/SLOs covering the touched code | Review (resolved from backend) | Confirms the alert↔code link at triage; flags high-risk changes. |
| `watch` | Risk hypotheses to watch post-deploy | Author + Review | Triage reads this first — the leading hypotheses are pre-written. |
| `gaps` | Telemetry deliberately not added | Review | Tells triage what the data cannot answer, so it stops chasing it. |

## Lifecycle

1. **Author drafts** `type`, `touches`, `telemetry`, and `watch` when opening the PR.
2. **Review enriches** — [oodle-o11y-review](../oodle-o11y-review/SKILL.md)
   resolves `guarded-by` from the live backend, appends `gaps`, and may upgrade
   `type` to `critical-path` when touched code sits under a critical SLO.
3. **Merge** — the block lives on in the PR history.
4. **Triage reads** — on an alert, [oodle-triage](../oodle-triage/SKILL.md) finds
   recent PRs touching the alerting service and reads their manifests: `watch` and
   `type` focus the investigation, `guarded-by` confirms the alert↔code link, and
   `gaps` explains missing evidence.

## Relevance gate

Write the block when the change **touches instrumented or service code**, or when
its `type` is `perf`, `critical-path`, or `bugfix`. Skip it for docs-only,
config-cosmetic, or otherwise trivial changes — an empty ritual block is noise.
The reviewer skill makes the final call on relevance; when in doubt, include a
short block over none.

## Carrier

In v1 the manifest lives **only in the PR description**, read back at triage time
through the GitHub or Linear MCP — or, when no GitHub MCP is present, the `gh`
CLI (`gh pr list`, `gh pr view`). A durable git commit trailer and a tracked
in-repo manifest file are deliberately **deferred** — revisit only if triage
frequently lacks a discoverable PR for a deployed commit.

## Stability contract

The `## O11y Change Context` header and the field keys
(`type`, `touches`, `telemetry`, `guarded-by`, `watch`, `gaps`) are a parsing
contract. Other skills and future automation match on them — do not rename or
reorder-away fields. Adding a new optional field is safe; renaming an existing one
is a breaking change.
