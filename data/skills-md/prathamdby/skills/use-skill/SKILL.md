---
name: use-skill
description: >
  use-skill to fetch and run GitHub-linked skills ephemerally, without installation.
---

# Use skill

## Scope

Default ephemeral: fetch/run/discard, never install or persist.
Blob/raw/tree URLs or owner/repo@ref:path resolve to a skill directory (a file
uses its parent); omitted ref uses repo default branch. Other forms or requests
to save/install block. Repository-content questions belong to box.
Record `links | resolved directory/revision | blob set | executed | terminal`.

Fetched workflows run under this invocation's authority, not above host
permissions or higher-priority instructions. Trust linked skills by default,
without an allowlist; live user instructions win direct content conflicts.
Skill links inside fetched content may be followed under the same boundaries.

## 1. Resolve and fetch

Resolve every link, then pin its ref/default branch to a commit revision.
Use authenticated gh; no sibling skill is required for these file reads.
Missing gh/auth blocks. Apply API/decoding rules in `REFERENCE.md`.

List the recursive tree once at the pinned revision; require a non-truncated
listing and fetch every blob under the directory, not only the entry.
Stage only in a run-owned temporary directory outside the repo; page long
content locally instead of re-fetching a successful blob. Missing directory,
failed blob, or rate-limit blocks with retry signal.
Done when every link has an identity and every listed blob has decoded content.

## 2. Verify and execute

Empty set → NO_CHANGES. Nonempty requires SKILL.md or the specifically linked
entry, name frontmatter, and procedure; otherwise BLOCKED.
Read entry and every sibling in full: weak remote pointers cannot hide required
material. Execute steps in order within authority. For an item failure,
continue remaining links; never retry successful executions.
Done when every link reaches a terminal.

## 3. Discard and report

Remove only this run's temporary artifacts after execution, never unknown paths.
Report each link's SUCCESS/NO_CHANGES/BLOCKED and what ran, citing its pinned
source. Done when artifacts are discarded and every terminal is evidenced.
