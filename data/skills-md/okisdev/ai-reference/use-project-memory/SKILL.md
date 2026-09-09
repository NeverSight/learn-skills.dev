---
name: use-project-memory
description: Read and write Claude project auto-memory so Claude, Grok, and Codex share one store. Use at the start of repo work, when a durable project fact is learned, or when the user says remember / 记住 / 项目记忆.
argument-hint: "[note]"
---

## Context

Memory: !`python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`

## Instructions

Use Claude auto-memory as the only project store. Read the index first. Write a topic file plus one index line.

### Process

1. Parse `$ARGUMENTS` (a note to store, or empty to load). Resolve the directory with `python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`. If the probe printed `missing`, that path is still the write target.
2. Read `MEMORY.md` in that directory. It is an index (Claude loads the first 200 lines or 25KB). Open a linked topic file when a line is relevant to the current task. `ARCHIVE.md`, when present, indexes closed sagas; grep it before re-diagnosing or re-attempting anything old.
3. On load (no note): apply the matching topic files and continue the original task. A stored claim is a point-in-time observation, not proof; before a load-bearing one gates the current work, confirm it still holds on the live tree. When the index has more than twenty lines and `.clean-memory.json` in that directory is missing or older than thirty days, say so in one line and continue; `clean-memory` is the pass that verifies the store. Do not summarize the whole index unless asked.
4. On write: search the directory for an existing topic that already covers the fact and update it in place. Progress and detail go into the topic file; touch its index line only when the status or the retrieval cue changed. A topic file states current truth, not the journey: delete superseded narrative, keep issue numbers and commit SHAs greppable, and compact any file drifting past about 8KB.
5. On a new fact: create one kebab-case `.md` with YAML frontmatter (`name`, `description`, `metadata.type` of `user`, `feedback`, `project`, or `reference`, and `metadata.verified`, the date a `clean-memory` pass last confirmed the topic against the tree, left unset until then) and the fact in the body, carrying its citation (a SHA, issue number, or `file:line`); a claim without one is labeled inference, not written as fact. A path in another repository is cited on a line that names that repository, and a path that no longer exists is cited on a line that says it moved or was removed, because `clean-memory` checks every other path against this tree. Add exactly one index bullet of the form `- [title](file.md) — hook`. The hook is at most 80 characters: a status token (SHIPPED, CLOSED, OPEN, PARKED, DISPROVEN, SUPERSEDED), the retrieval cue, and any standing prohibition. Everything else belongs in the topic file.
6. Index pressure: when `MEMORY.md` is past 180 lines or 22KB, first move terminal lines (shipped or closed, no live leftover, no standing prohibition, no recurring recipe) verbatim to `ARCHIVE.md`. Move lines, never delete them, and never move or rename topic files. A line whose value is a standing prohibition stays in `MEMORY.md` regardless of age.
7. First write in a missing directory: create the directory and a `MEMORY.md` that contains only the new bullet.

### Rules

- Do not append prose to `MEMORY.md`. Do not rewrite the whole index. Do not use Grok `/remember`, Grok `~/.grok/memory/`, or Codex `~/.codex/memories/` for project facts.
- Never delete someone else's entries; the only sanctioned reductions are topic-file compaction, verbatim line moves to `ARCHIVE.md`, and the evidence-backed dispositions of `clean-memory`.
- A new topic needs a one-sentence reason to exist. If you cannot give one, do not write it.
- Worktrees of the same git repo share the primary worktree's directory. The resolver already picks that path.
