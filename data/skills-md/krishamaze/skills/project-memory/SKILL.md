---
name: project-memory
description: >
  Maintains three living project docs: DECISIONS.md (what + why), CONTEXT.md (where we
  are + what's next), STACK.md (locked versions + do-not patterns + failure root causes).
  Invoke every 5-7 conversation turns, after any architectural decision, after any failure
  or error is resolved, or when stack constraints change. Updates are surgical — only what
  changed. Never rewrites what's still true. Never adds bloat. If invoked and nothing
  changed, say so and stop.
---

# project-memory

## Purpose
Three files. Each has one job. Together they let any agent — or future-you — resume
work cold without losing context or repeating dead ends.

| File | Job |
|------|-----|
| `DECISIONS.md` | What was chosen + why. Immutable once written. |
| `CONTEXT.md` | Live state: current layer, blockers, next action. Overwrites each run. |
| `STACK.md` | Locked versions + **do-not** patterns + failure root causes. |

---

## Rules Before Writing Anything

1. **Read all three files first.** Never update blind.
2. **Update only what changed.** One new decision? One new entry. Not a rewrite.
3. **CONTEXT.md is the only file that fully overwrites.** The other two append only.
4. **Failures are first-class.** A root cause captured is a dead end avoided.
5. **If nothing changed, say "No updates needed" and stop.**

---

## DECISIONS.md — Format

Each entry is an ADR (Architecture Decision Record). Once written, never edited.
If a decision is reversed, add a new ADR that supersedes it.

```markdown
# Decisions

## ADR-001: [Title]
**Status:** active | superseded by ADR-00X
**Decision:** One sentence — what was chosen.
**Why:** One to three sentences — the actual reason. Not obvious things.
**Do not:** What must never happen as a result of this decision.
**Failure mode:** What goes wrong if this is ignored.
```

**What earns an ADR:**
- Architectural choices (always-on vs on-demand, profile system, gatekeeper)
- Stack choices (uv not pip, Camoufox not Playwright raw)
- Security choices (localhost-only ports, no cookie rotation)
- Anything that, if reversed, would break something silently

**What does NOT earn an ADR:**
- Implementation details
- File naming
- Anything reversible without consequence

---

## CONTEXT.md — Format

Fully overwrites every invocation. Stays under 20 lines.

```markdown
# Context
**Updated:** YYYY-MM-DD

## Current Layer
Layer X — [name]. Status: [building | blocked | verified]

## Last Completed
[One line — what just finished and confirmed working]

## Active Blocker
[One line — what is broken or unclear right now. "None" if clear.]

## Next Action
[Exact next task. Specific enough that an agent can execute it cold.]

## Deferred
- [Thing explicitly set aside + why]
```

---

## STACK.md — Format

Two sections. Append-only except version bumps.

```markdown
# Stack

## Locked Versions
| Package | Version | Replaces |
|---------|---------|----------|
| camoufox | >=0.4.0 | raw Playwright for stealth |
| uv | latest | pip, venv, pyenv |
| ...

## Do-Not Patterns + Root Causes

### [Pattern name]
**Never:** [Exact thing to never do]
**Why:** [Root cause — what actually broke or will break]
**Instead:** [Correct pattern]
```

**What earns a Do-Not entry:**
- Anything that caused a real failure during this project
- Any 2025 pattern that was caught and rejected
- Any anti-pattern from the 2026 skills that applies here

---

## Update Algorithm

```
1. Read DECISIONS.md, CONTEXT.md, STACK.md
2. Read last 5-7 conversation turns
3. Extract:
   a. New decisions made → append to DECISIONS.md
   b. New failures/root causes → append to STACK.md do-nots
   c. Version changes → update STACK.md locked versions
   d. Current state → overwrite CONTEXT.md
4. Write only changed files
5. Report: "Updated X, Y. Z unchanged."
```

---

## Token Budget Rule

Each file has a hard cap:
- `DECISIONS.md` — 60 lines max. If full, archive old ADRs to `references/decisions-archive.md`
- `CONTEXT.md` — 20 lines max. Always.
- `STACK.md` — 80 lines max. If full, archive resolved do-nots.

**Quality check before writing:** Would removing this sentence lose information?
If no → remove it.
