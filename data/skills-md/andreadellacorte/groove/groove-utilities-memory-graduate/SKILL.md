---
name: groove-utilities-memory-graduate
description: "Graduate a workflow insight from learned/<topic>.md into AGENTS.md as a permanent constraint. Use when a lesson is stable enough to apply to every future session."
license: MIT
allowed-tools: Read Write Edit Glob AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-graduate

Promote a stable workflow insight from `.groove/memory/learned/` into `AGENTS.md` as a permanent constraint — visible to every agent session without needing to run prime.

Use $ARGUMENTS as the topic or insight text if provided.

## Outcome

The lesson is appended to a `<!-- groove:learned:start -->` / `<!-- groove:learned:end -->` section in `AGENTS.md`, making it permanently visible to all future sessions.

## Acceptance Criteria

- Insight is appended to the `## Graduated Learnings` section in `AGENTS.md`
- Section is created if it does not exist
- User confirms the exact text before writing
- Source `learned/<topic>.md` entry is marked as graduated (not deleted)

## Steps

1. Memory path is always `.groove/memory/`
2. If $ARGUMENTS names a topic, read `.groove/memory/learned/<topic>.md` and show its entries. Otherwise, list all `*.md` files in `.groove/memory/learned/` and ask which topic to graduate from.
3. Show the file contents; ask: "Which entry should be graduated? (paste or describe it)"
4. Show the exact text that will be written to AGENTS.md; ask: "Confirm? (yes / edit / skip)"
5. If confirmed: write to AGENTS.md (see section management below)
6. Mark the entry in the learned file by appending `[graduated YYYY-MM-DD]` inline after the bullet
7. Report: "Lesson graduated to AGENTS.md → ## Graduated Learnings"

## Section management in AGENTS.md

Look for a `<!-- groove:learned:start -->` / `<!-- groove:learned:end -->` block:

- If the block exists: append the new insight as a bullet under `## Graduated Learnings` inside the block
- If the block does not exist: append the following to the end of `AGENTS.md`:

```
<!-- groove:learned:start -->
## Graduated Learnings

Stable workflow insights promoted from `.groove/memory/learned/`. These apply to every session.

- <insight text>
<!-- groove:learned:end -->
```

Each entry is a single bullet: `- <insight text> *(from learned/<topic>.md, graduated YYYY-MM-DD)*`

## Constraints

- Never graduate without explicit user confirmation of the exact text
- Never delete the source entry from `learned/<topic>.md` — mark it as graduated with `[graduated YYYY-MM-DD]` inline; the full context stays in the file
- The `<!-- groove:learned:* -->` section is user-owned — groove update will not overwrite it
- Keep graduated lessons concise — one actionable sentence per bullet; ask user to trim if longer
- If AGENTS.md does not exist: create it with just the graduated learnings section
- If the same insight is already present in the block (exact match): skip and report "Already graduated."
