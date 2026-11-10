---
name: kb
description: Use when a KB hook message or check issue needs resolving, a source file is too large for one read, evidence or a table export arrives, the user asks whether the knowledge base already has a page or term for something, a stable technique may become a recipe, or the workspace needs an upgrade. Runs the integrity tool.
---

# KB

The workspace ships a deterministic integrity tool in `tools/kb/`. It
checks links, indexes, evidence tracking, required page sections,
duplicates, recipes, and encoding; it applies fixes that have exactly
one correct answer and hands everything else to you as numbered issues.
Use this skill to act on what it reports and to do knowledge-base work
through it instead of by hand.

## How to call it

Run from the workspace root (the folder holding `AGENTS.md` and
`modules.md`):

```
python tools/kb/kb.py <command> ...
```

Use `python3` or `py -3` where `python` is
missing or older than 3.9. Every command prints a one-line
summary first. Exit 0 means clean or done; 1 means issues were found;
2 means a usage or workspace error; 3 means a table export needs a new
layout; 4 means an upgrade has open questions.

## Route by situation

| Situation | Read |
|---|---|
| A source file is larger than about 50 KB, or you only need its shape | `references/outline.md` |
| New evidence arrived (documents, exports, library sources, examples) | `references/ingest.md` |
| A table export must become table pages | `references/tables.md` |
| You are about to write a page and need to know whether one exists | `references/dedupe.md` |
| An unknown term, abbreviation, or transliteration | `references/terms.md` |
| A platform technique has stabilized and may be reused | `references/recipes.md` |
| A hook message, a check result, or `docs/checks/OPEN.md` lists issues | `references/issues.md` |
| The session-start line says the workspace version is old | `references/upgrade.md` |

Read only the reference you need.

## Fix policy

- Safe fixes (exactly one correct answer) are applied automatically by
  the hooks and by `kb fix --safe`; each one is journaled and can be
  reverted with `kb undo <run-id>`.
- Ambiguous cases become issues with their candidates. You decide when
  the evidence settles it; otherwise ask the user.
- Never hand-edit what `kb fix --safe` would do. Run the command.
- When the user confirms that two pages are an intended duplicate,
  record it with `kb config accept-duplicate <path> <path>` so the issue
  does not come back.

## What the hooks do

After you edit a knowledge-base page or evidence file, the post-write
hook applies safe fixes and reports remaining issues for that file. At
the end of a turn, the stop hook blocks once if your changes introduced
a blocking issue. At session start, one line reports open issues or an
old workspace version. When nothing is wrong, the hooks print nothing.
Without hooks, run `kb check --changed <files>` yourself before closing
a session.
