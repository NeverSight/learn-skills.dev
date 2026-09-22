---
name: rail-align
description: Align on a plan or design — light grilling with domain docs by default; map mode for foggy multi-session efforts. Light mode writes docs/monorail/<slug>/align.md then auto-continues the planning chain (spec, which stops for your go/no-go before slice).
disable-model-invocation: true
---

# Rail Align

Sharpen an idea before spec/build. Two modes — light by default when the ask is clear; ask about map only when fog warrants it.

Confirm with the shell before concluding either file is missing (`ls docs/monorail/work-tracker.md docs/monorail/domain.md`, or read the paths directly) — search tools skip gitignored paths, so an empty Glob/Grep result is **not** evidence of absence. If a file is missing on disk, tell the user to run `/rail-setup` first and stop.

## Opening gate

After the user states the idea, **classify silently** — do **not** open with a Light vs Map choice.

- **Clear and small enough for this conversation** → enter **Light mode** immediately and start grilling
- **Foggy / complex / multi-session** → ask whether to enter **Map mode** (read [`map-mode.md`](map-mode.md)); if they decline, stay in light
- If unsure: start light; escalate to map only when fog appears mid-session and the user agrees

If map mode's first breadth pass finds **no fog**, do not create a map — stay in light mode.

## Light mode (default)

1. Interview one question at a time (same discipline as `/rail-grill`), with recommended answers
2. Actively maintain domain docs (paths from `docs/monorail/domain.md`):
   - Challenge terms against `docs/monorail/CONTEXT.md`
   - Sharpen fuzzy language; propose canonical terms
   - When a hard-to-reverse decision crystallises, write an ADR under `docs/monorail/adr/`
   - Create `docs/monorail/CONTEXT.md` / `docs/monorail/adr/` lazily when first needed — check with the shell first (`ls`); search tools skip gitignored paths, and an existing glossary or ADR must never be replaced
3. When the decision tree is resolved and the user confirms shared understanding, **persist before continuing**:
   - **Pick a new feature slug** (`docs/monorail/<slug>/`) — agent chooses; **never ask** the user; **never reuse** an existing `docs/monorail/<slug>/` work directory (related prior efforts stay separate; link them from Domain pointers if useful). If the user already named a free slug, use it as-is (no prefix). Otherwise invent a distinct unused slug: `YYYY-MM-DD-NN-<kebab>` where `NN` is the day's global sequence (`01`, `02`, … — count today's existing date-prefixed effort dirs + 1 with the shell, `ls docs/monorail/`; search tools skip gitignored paths and can miss effort dirs, so never take the sequence or the "unused" check from Glob/Grep). Reserved names: `CONTEXT.md`, `CONTEXT-MAP.md`, `adr`, `work-tracker.md`, `domain.md`
   - **Do not** interview for slug (no A/B/C, no “new vs continue”) — slug is path bookkeeping, not a decision-tree branch
   - Write `docs/monorail/<slug>/align.md` using the template below (create the directory)
   - Domain docs alone are **not** enough — `/rail-spec` requires this file (or a cleared map)
4. **Continue the planning chain** for this same `<slug>`: read and follow `/rail-spec` in this same session (it writes `spec.md`, then stops for your go/no-go before `/rail-slice`). Do **not** stop and ask the user to type `/rail-spec`. Do **not** substitute `/to-spec` or other foreign-pack equivalents.
   - **Exceptions (stop instead):** user asked to stop after align; context near limits → `/rail-pass`
   - **Budget check (before auto-continuing):** the light grilling may have already spent a large share of this session's context. If so, stop here — `align.md` is durable, and `/rail-spec` resumes it fresh next session (its code-grounding pass and single seam confirmation deserve a clean window). When in doubt prefer stopping with `align.md` written. This is a self-determined stop, not a new question for the user.

### `align.md` template

Use these exact headings:

- `## Intent` — what we're building and why (user perspective)
- `## Decisions settled` — bulleted consensus from this align (trade-offs the user owned)
- `## Deferred` — explicitly parked; not blockers for spec (or `None`)
- `## Out of scope`
- `## Domain pointers` — links/paths to `docs/monorail/CONTEXT.md` terms and ADRs touched (or `None`)

Do **not** treat conversation memory as the pass. If context is near limits before step 3, request `/rail-pass` and finish `align.md` in the next session from that pass document — never suggest `/rail-spec` without a durable align or map artifact.

## Map mode

Follow [`map-mode.md`](map-mode.md). Charting opens a **new** effort slug (same rules as light persist — never ask, never reuse); work-through stays on the map's existing slug. Still update `docs/monorail/CONTEXT.md` / ADRs when terms crystallise. Produce **decisions**, not implementation deliverables.

Map mode does **not** require `align.md` — `map.md` + resolved `decisions/` are the durable source for `/rail-spec`.

## Completion

- Light: user confirms alignment; `align.md` written; domain docs updated as needed; then auto-continue into `/rail-spec` (unless an exception above applies)
- Map charting: `map.md` + initial `decisions/` written (each with a `Type`); no tickets resolved in the charting session — **stop** (do not auto-continue; next session works tickets)
- Map work-through: exactly one ticket resolved (any `Type`); map index updated; research tickets also write `notes/` — **stop** unless the map is now clear, in which case auto-continue into `/rail-spec` (see `map-mode.md`)

Near context limits: stop and suggest `/rail-pass` instead of continuing degraded.
