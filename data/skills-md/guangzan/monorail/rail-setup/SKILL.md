---
name: rail-setup
description: Configure a repo for rail skills — all docs under docs/monorail/ (work tracker + domain). Run once per repo before other rail engineering skills.
disable-model-invocation: true
---

# Rail Setup

Scaffold per-repo configuration that rail engineering skills assume:

- **Everything under `docs/monorail/`** — work tracker, glossary, ADRs, and convention files (no remote tracker; no scatter to repo root / `docs/agents/` / `docs/adr/`)
- **Domain docs** — `docs/monorail/CONTEXT.md` + `docs/monorail/adr/`

This is prompt-driven, not a deterministic script. Explore, present, then write — never pause to ask the user to confirm the plan.

## Process

### 1. Explore

Read what exists; do not assume:

- `AGENTS.md` / `CLAUDE.md` — either present? Already has `## Agent skills`?
- `docs/monorail/` — already in use? Check with the shell (`ls -R docs/monorail`, or `ls` / `test -f` per file): `work-tracker.md` / `domain.md` / `CONTEXT.md` / `adr/`. Search tools skip gitignored paths — an empty Glob/Grep result is **not** evidence the directory is unused
- Legacy scatter (migrate hint only, do not auto-move): repo-root `CONTEXT.md` / `CONTEXT-MAP.md`, `docs/adr/`, `docs/agents/`
- Monorepo signals (`pnpm-workspace.yaml`, package `workspaces`, populated `packages/*`)

### 2. Present

Summarise present vs missing. Then:

**Doc root** — state that rail keeps **all** docs under `docs/monorail/` only. Show templates at `templates/work-tracker.md` and `templates/domain.md` (relative to this skill). Use the default root (`docs/monorail/`); adjust path wording only if the user explicitly asks for a non-default root. If they insist on a remote tracker, refuse for rail skills and stop — rail v1 is local-only. If legacy paths exist, tell the user to move them under `docs/monorail/` manually (do not rewrite their content in this skill).

**Domain docs** — default single-context (`docs/monorail/CONTEXT.md` + `docs/monorail/adr/`). Offer multi-context only when exploration found monorepo signals (`docs/monorail/CONTEXT-MAP.md`; per-context paths still under `docs/monorail/`).

### 3. Write

Write immediately after presenting — no confirmation, no waiting for edits. Show each draft as you go, then report what was written. The pieces to write:

- `## Agent skills` block for `CLAUDE.md` or `AGENTS.md`
- `docs/monorail/work-tracker.md` (from template, path adjusted if needed)
- `docs/monorail/domain.md` (from template)

**Skip what already exists:** if `docs/monorail/work-tracker.md` / `docs/monorail/domain.md` — or the `## Agent skills` block — is already there (confirmed with the shell), leave it untouched, report it as already present, and write only the missing pieces. Never overwrite an existing tracker or domain doc.

**Pick file for Agent skills block:**

- If `CLAUDE.md` exists, edit it
- Else if `AGENTS.md` exists, edit it
- If neither exists, ask which to create — do not pick for them
- Never create both

**Agent skills block** (adapt if work root changed) — include these bullets verbatim in the target file:

- Heading: `## Agent skills`
- Line: This repo uses **rail** skills. All rail docs live under `docs/monorail/`.
- Bullet: Work tracker: `docs/monorail/work-tracker.md`
- Bullet: Domain docs: `docs/monorail/domain.md`
- Line: Run `/rail-setup` again only if these conventions change. Prefer `/rail` to see the main flow.

Write `docs/monorail/work-tracker.md` and `docs/monorail/domain.md` from the templates in this skill folder. Create `docs/monorail/` if needed. Do **not** create `CONTEXT.md` / `adr/` until `/rail-align` needs them.

### Completion

Done when both convention files exist under `docs/monorail/`, the Agent skills block is present, and you told the user they can start with `/rail-align` or `/rail`.
