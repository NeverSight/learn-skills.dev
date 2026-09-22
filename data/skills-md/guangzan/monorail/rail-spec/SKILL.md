---
name: rail-spec
description: Synthesize durable align/map sources (and current conversation) into docs/monorail/<feature>/spec.md, then stop and ask before continuing to rail-slice. Refuse empty context — do not invent a thin spec.
disable-model-invocation: true
---

# Rail Spec

Turn **durable alignment** into a spec. Prefer synthesis over interview — but **never** invent a spec from thin air.

Confirm with the shell before concluding it is missing (`ls docs/monorail/work-tracker.md`, or read the path directly) — search tools skip gitignored paths, so an empty Glob/Grep result is **not** evidence of absence. If it is missing on disk, tell the user to run `/rail-setup` and stop.

## Process

### 1. Confirm the feature slug

Before reading or writing work files:

- If the user named one, use it
- Else list them with the shell (`ls docs/monorail/`, then each effort directory for `align.md` / `map.md` / `spec.md`) — search tools skip gitignored paths, so never build this list from Glob/Grep results (skip reserved names: `adr`, `work-tracker.md`, `domain.md`, `CONTEXT.md`, `CONTEXT-MAP.md`); match by **content name** (strip the `YYYY-MM-DD-NN-` prefix from agent-invented slugs); if several match, use the latest (date + sequence sorts chronologically)
- If `docs/monorail/<slug>/align.md` or `map.md` already exists for this effort, **do not** invent a different slug for the spec

### 2. Adequacy gate (fail closed)

Collect sources for this `<slug>`:

| Source | Counts as adequate? |
|---|---|
| `docs/monorail/<slug>/align.md` | Yes |
| `docs/monorail/<slug>/map.md` with at least one resolved decision linked under Decisions so far (or map clear: no open tickets, Not yet specified empty / only out-of-scope) | Yes |
| Substantial align discussion **in this same session** that has not yet been written to `align.md` | Yes — but write `align.md` first (same template as `/rail-align` light), then continue |
| `docs/monorail/<slug>/pass-*.md` or a pass path the user passed | Enrichment only — **not** sufficient alone |
| `docs/monorail/CONTEXT.md` / ADRs alone | **No** |
| Empty / unrelated conversation | **No** |

If **no** adequate source: **stop**. Tell the user to run `/rail-align` for this slug (or keep grilling in this session, then persist `align.md`). Do **not** write `spec.md`.

If the map still has open decision tickets or non-empty fog under Not yet specified: **stop**. Suggest finishing `/rail-align` map mode first — do not spec over unresolved fog.

### 3. Fold durable sources

- If `align.md` exists, read it fully — fold Intent / Decisions settled / Out of scope into the spec; do not leave consensus only in `align.md`
- If `map.md` exists, read Decisions so far and linked decision answers (and `notes/` when cited) — fold them in; do not leave decisions only on the map
- Use conversation only to enrich, never as the sole source after a fresh session

### 4. Code-ground the seams (mandatory)

Before writing, run a **read-only grounding pass** so the spec's seams are anchored in the actual code — this is **not optional**: the spec's `## Testing Decisions` is the single seam decision for the effort, and `/rail-build` verifies it rather than re-confirming.

- Explore the codebase. Use `docs/monorail/CONTEXT.md` vocabulary; respect ADRs under `docs/monorail/adr/`.
- Run a read-only grounding sweep **inline in the main session by default** — usually a few reads (`grep` + `read`): **code map** (paths/types/call chains named or implied), **test / seam precedents** (existing tests and public boundaries near those paths), **domain docs** (CONTEXT, ADRs, coding standards). Offload to read-only sub-agents — up to three in parallel, or sequentially — only when the territory is genuinely unfamiliar or wide enough to justify the spawn; skip a scope whose inputs clearly do not exist. Always run code map + test precedents when any code exists.
- Write the validated outcome into `## Testing Decisions`: external behaviour, then seams — prefer existing seams, highest seam, few seams — each with a pointer to the file/test that anchors it. Do not leave seams as a sketch.
- **Confirm seams with the user once, here** — this is the single seam decision; downstream build only re-raises a seam on a real contradiction.

### 5. Gap-closing only (not a full grill)

If durable sources exist but a **few** gaps block a coherent spec, ask only those questions — one at a time. If gaps are large or re-open the decision tree, stop and suggest `/rail-align` instead of pushing a hollow spec.

### 6. Write, then stop for the slice go/no-go

Write `docs/monorail/<feature-slug>/spec.md` using the template below.

**Stop and ask once before slicing.** After writing, present a short digest of the spec (Problem / Solution / Stories overview, the single seam decision from `## Testing Decisions`, Out of scope, and the `spec.md` path), then ask whether to continue into `/rail-slice` in this same session. Wait for the answer.

- **Continue** → read and follow `/rail-slice` for this same `<slug>` in this same session (writes `docs/monorail/<slug>/tasks/NN-*.md`)
- **Revise the spec** → stay on the spec; iterate `spec.md` in place from the feedback (if a change contradicts a settled `align.md` / map decision, update that durable source too), then return to this go/no-go
- **Pause** → stop here. `spec.md` is durable; a later `/rail-slice` (or the next session) resumes from it

Do **not** substitute foreign-pack skills — e.g. `/to-tickets`, `/to-issues`, `/to-prd`, `/to-spec` — even if those are installed. Do **not** open GitHub/GitLab Issues for rail work. Do **not** auto-continue into `/rail-build`.

**Stop instead when:** context is near limits → `/rail-pass` (do not write a degraded spec, and do not continue to slice).

## Spec template

Use these exact headings in `spec.md`:

- `## Problem Statement`
- `## Solution`
- `## User Stories` (numbered: As a \<actor\>, I want \<feature\>, so that \<benefit\>)
- `## Implementation Decisions` (modules/interfaces/architecture/schema/API — no fragile file paths unless quoting a prototype snippet that encodes a decision)
- `## Testing Decisions` (external behaviour; seams; prior art)
- `## Out of Scope`
- `## Further Notes`
