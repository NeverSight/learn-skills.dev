---
name: handoff
description: 'Produces and refreshes `.docs/handoff.md`, a 200-line session-continuity runbook for coding agents. Captures git state, working-tree changes, last validation commands, session decisions, blockers, resume checklist, references, and greenfield scaffolds. Triggers on: "update handoff", "session handoff", "refresh handoff", "/handoff", "/handoff init", "resume checklist", "cold-start primer". Use this skill when ending, pausing, resuming, or transferring in-flight project work across agent sessions.'
metadata:
  version: 0.1.0
  category: development
  tags: [session-continuity, runbook, context]
  difficulty: intermediate
  phase: ship
---

# Handoff

Maintains `.docs/handoff.md` as the project-local cold-start primer for the next coding agent or human developer. The file captures transient session state only: what changed, what was decided, what is blocked, and exactly how to resume.

## Reference Files

| File | Contents | Load When |
| --- | --- | --- |
| `references/schema.md` | Verbatim handoff schema and line-budget rules | Always before writing |
| `references/authority-boundaries.md` | Boundary between handoff, memory, CLAUDE.md, plans, and git | Always before writing |

## When To Use

| Use handoff | Use another surface |
| --- | --- |
| In-flight work, uncommitted edits, current branch, blockers, resume steps | `git log` for committed history |
| Session-scoped decisions and failed approaches | Memory or ADRs for durable project facts |
| Immediate validation state and exact next command | `CLAUDE.md` for stable setup instructions |
| Current roadmap cursor | Plan files for strategic roadmap content |

## Triggers

- Direct commands: `/handoff`, `/handoff init`
- Refresh phrases: "update handoff", "session handoff", "refresh handoff", "save handoff"
- Resume phrases: "cold-start primer", "resume checklist", "handoff to next session"
- Stop hook: refresh silently when `.docs/handoff.md` already exists

## Prerequisites

- `git` available in the project root.
- Project write access for `.docs/handoff.md`.
- Optional project-local marker files:
  - `.docs/handoff.last-validation` containing the last verification command and result.
  - `.docs/handoff.session` containing extra bullets for changes, decisions, blockers, or refs.

## Workflow

1. **Resolve mode.**
   - `/handoff init` or invocation from an initialization workflow writes a greenfield stub when `.docs/handoff.md` is absent.
   - `/handoff`, refresh phrases, and Stop-hook invocation rewrite the full file.
2. **Read source of truth.**
   - Load `references/schema.md` and preserve the schema headings exactly.
   - Load `references/authority-boundaries.md` and include the authority boundary line in every generated handoff.
3. **Detect repository state.**
   - Run `git rev-parse --show-toplevel`, `git branch --show-current`, `git rev-parse --short HEAD`, and `git status --porcelain`.
   - Count modified, untracked, and staged paths from porcelain status.
   - Include the top 3-5 changed paths in the Status section.
4. **Detect validation state.**
   - Prefer recent session context: commands actually run in the current agent session and their result.
   - If available, read `.docs/handoff.last-validation`.
   - If neither exists, write explicit unknowns: "not recorded this session" rather than inventing pass/fail.
5. **Gather session substance.**
   - Summarize logical changes from current conversation, uncommitted paths, and commits since the branch base when relevant.
   - Record decisions with rationale in two sentences or fewer.
   - Record blockers and open questions as actionable unchecked items.
   - Include failed approaches when they would prevent wasted work in the next session.
6. **Write by full rewrite.**
   - Replace `.docs/handoff.md` atomically; do not append.
   - Create `.docs/` if absent.
   - Keep the file lowercase at `.docs/handoff.md`.
7. **Enforce 200 lines.**
   - Count final lines after rendering.
   - If over 200, truncate `## What changed this session` oldest-first.
   - Insert `<!-- WARNING: handoff exceeded 200 lines; oldest session changes were truncated. -->`.
   - If still over 200, compress decisions and blockers to the newest actionable items, preserving all required headings.

## Supported Operations

| Operation | Command | Behavior |
| --- | --- | --- |
| Refresh | `/handoff` | Rewrites `.docs/handoff.md` from current repo and session state |
| Scaffold | `/handoff init` | Creates an empty schema stub when no handoff exists |
| Stop refresh | Stop hook | Refreshes only when `.docs/handoff.md` already exists |
| Dry run | `uv run skills/handoff/scripts/handoff.py --dry-run` | Prints generated content without writing |

## Implementation Notes

The bundled script is the deterministic baseline used by the command and hook:

```bash
uv run skills/handoff/scripts/handoff.py --project-root "$PWD"
uv run skills/handoff/scripts/handoff.py --project-root "$PWD" --init
```

Agents may improve populated bullets from live session context before writing, but must preserve:

- Schema headings and order.
- Authority boundary line.
- Full-file rewrite semantics.
- Hard 200-line cap.
- Explicit unknowns instead of silent fallbacks.

## Greenfield Scaffold

When invoked as `/handoff init` or under a project initialization flow and `.docs/handoff.md` does not exist, write the schema with empty placeholders and real git metadata. This documents the `/init` integration point without modifying any init script.

## Output Format

Write exactly one file: `.docs/handoff.md`.

Required first lines:

```markdown
# Handoff — <project name>

**Last touched:** <ISO 8601 timestamp with timezone> · **branch:** `<branch>` · **HEAD:** `<short-sha>` · **session:** <model id>
```

## Troubleshooting

| Problem | Resolution |
| --- | --- |
| Not in a git repository | Fail clearly for refresh; scaffold may use branch `—` and HEAD `—` only during `/handoff init` |
| `.docs/` missing | Create it before writing |
| Validation state unavailable | Write "not recorded this session"; do not claim tests passed |
| Generated file exceeds 200 lines | Truncate oldest `What changed` bullets and add the warning comment |
| Existing handoff uses old casing or root path | Do not migrate automatically; future refreshes converge only when invoked in that project |

## Verification

- `uv run python scripts/validate_evals.py`
- `uv run scripts/evaluate_package.py skills/handoff`
- `uv run skills/handoff/scripts/handoff.py --project-root <repo> --dry-run`
- `uv run skills/handoff/scripts/handoff.py --project-root <repo> --init --output <tmp-file>`

