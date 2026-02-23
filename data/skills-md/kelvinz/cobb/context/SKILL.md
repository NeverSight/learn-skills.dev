---
name: context
description: "Maintain durable project context in `tasks/context.md` (state, decisions, milestones, gotchas, optional context links), inline during other workflows or standalone for cleanup/backfill. Triggers: update context.md, decision log, record project context, capture high-value reference links that improve context handoff."
---

# context

Maintain `tasks/context.md` as a living, durable "what matters" record for the project.
Write it for someone taking over the project (or a future session resuming later).
Explain where things are, what was decided, and what to watch before proceeding.
Treat this as shared behaviour embedded in other skills, not a mandatory standalone step in normal workflows.
When invoked inline (from another skill), apply this workflow as part of that skill's execution.
When invoked directly, use for explicit backfill/repair/cleanup requests.

---

## Guardrails

- Do not store secrets (API keys, tokens, credentials).
- Keep entries short and durable; avoid duplicating long PRDs or code.
- Update `tasks/context.md` in place; do not rewrite the whole file.
- Write in plain language so a junior dev (or another AI) can take over without extra context.
- Prefer inline updates during active skills (`prd`, `design`, `implement`, `review`, `commit`).
- Update when worthwhile information emerges.
- Links are optional and high-signal only; see Links Format below.
- When asking users for decisions/clarifications, provide numbered short-reply options (e.g. `1`, `2`, `3`).

### What goes where
- PRD files (`tasks/f-##-*.md`) = what we intend to do (the spec + progress checklist for one feature)
- `tasks/context.md` = project definition, durable decisions, milestones, gotchas, and "where we are now"

---

## What to Record

- Project gist (what it is, who it's for, success measures) → `## Project`
- Current state (what's done, what's next, what's blocked) → `## Current state`
- Key decisions and durable design decisions (what we chose + why + tradeoffs) → `## Key decisions`
- Completed work (feature IDs and notable outcomes) → `## Completed`
- Notes/gotchas (constraints, pitfalls, conventions, sharp edges) → `## Notes / gotchas`
- Optional context links (canonical docs, API specs, repos) → `## Links (optional)`

Avoid:

- raw meeting transcripts
- verbose day-by-day logs
- duplicate content that already lives in PRDs or code

---

## Links Format

- Only add `## Links (optional)` when links materially improve handoff context.
- Format: `[Label](path-or-url) — why this helps future context`
- Prefer durable references (design docs, API specs, runbooks, repos); avoid ephemeral links (temp chats, preview URLs).
- De-duplicate by updating existing entries instead of adding near-identical links.

---

## Workflow

1. Ensure `tasks/` exists; create `tasks/context.md` if missing.
   - Use `references/context-template.md` as the default file template when creating it.
2. Add short entries (1–3 lines) in the most relevant section.
3. Prepend new entries at the top of each section (newest-first order).
4. Prefer referencing stable feature IDs (`f-##`) and avoid file paths (paths can change after archiving/compaction).
5. If a link materially improves context, add or update entries in `## Links (optional)` using the links format.
6. If it's unclear what to record, ask one clarifying question with numbered short-reply options (e.g. `1`, `2`, `3`).

---

## References

- `references/context-template.md`: default structure for creating `tasks/context.md`.

---

## Output

- Create or update `tasks/context.md`.
- **Inline** (from another skill): reply with a short summary of what was added/updated. Let the calling skill's output format take precedence.
- **Standalone** (direct invocation): reply with the file path, summary, and a status block:
  - **Files changed**: list of created/updated files
  - **Key decisions**: any assumptions or choices made (if any)
  - **Next step**: recommended next skill or action
