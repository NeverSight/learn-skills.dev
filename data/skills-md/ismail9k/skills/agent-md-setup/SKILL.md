---
name: agent-md-setup
description: >
  Use when a repository needs one canonical instruction file shared by coding
  agents, when AGENTS.md or CLAUDE.md is missing, or when their guidance has
  diverged.
---

# Setup Agent Instructions

Make root-level `AGENTS.md` the canonical repository instruction file and keep
root-level `CLAUDE.md` as its import pointer. This skill owns those two files
only; it does not configure issue trackers or other agent-specific files.

## Inspect before changing anything

1. Find the repository root and read any existing root-level `AGENTS.md` and
   `CLAUDE.md` in full.
2. Check `git status` so existing work is not mistaken for generated setup.
3. Summarize what exists and what would change before writing.

Treat hand-written content as intentional. A request to proceed quickly is not
permission to discard or silently relocate it.

## Choose the safe action

| Existing state | Action |
| --- | --- |
| Neither file exists | Copy both assets to the repository root verbatim. |
| `AGENTS.md` exists; `CLAUDE.md` does not | Preserve `AGENTS.md`; copy the `CLAUDE.md` asset. |
| `CLAUDE.md` is already the import pointer | Preserve it. Create `AGENTS.md` from its asset only if missing. |
| `CLAUDE.md` contains real guidance | Show the content, separate shared guidance from genuinely Claude-specific guidance, and ask whether to migrate the shared part or leave both files unchanged. |
| Both files contain real guidance | Show the overlap and propose an explicit merge of shared guidance into `AGENTS.md`; make no change until the user approves it. |

When a merge is approved, preserve the user's wording and repository-specific
structure. Add only missing material; do not replace an established
`AGENTS.md` with the generic template.

If `AGENTS.md` is missing during an approved migration, use its asset as the
starting structure, then place the approved shared guidance under `Project
knowledge`. Remove only empty placeholder headings that the migrated material
supersedes. If any guidance must remain Claude-specific, make no changes until
the user has preserved it somewhere outside these two files or reclassified it
as shared. Never create a partially migrated `AGENTS.md` that duplicates
guidance left in `CLAUDE.md`.

## Assets

- `assets/AGENTS.md` is the complete template for a missing `AGENTS.md`.
- `assets/CLAUDE.md` is the complete import-pointer file.

Read the relevant asset and copy it verbatim. Do not reconstruct either file
from memory when creating it without a migration. An approved migration may
add preserved user content to the `AGENTS.md` template as described above. The
template deliberately contains no issue-tracker, planning, or delivery
workflow; another skill may add those later.

## Finish

Read back the final `AGENTS.md` and `CLAUDE.md` and inspect their diff. Confirm
that approved guidance was neither omitted nor duplicated. Then report which
files were created, merged, left unchanged, or deliberately left for the user
to decide. Stop after instruction-file setup rather than invoking another setup
or workflow skill.

## What NOT to do

- Don't overwrite or delete hand-written instructions without showing them and
  receiving explicit confirmation.
- Don't copy the same guidance into multiple agent-specific files.
- Don't edit `.cursor/`, `.cursorrules`, or other tool-specific files; they are
  outside this skill's contract.
- Don't create `docs/agents/issue-tracker.md` or add an intent-to-PR workflow.
- Don't invent commands, conventions, architecture notes, or project facts for
  the template's empty sections.
- Don't silently replace an existing `CLAUDE.md`, even when the import-pointer
  pattern would be cleaner.
