---
name: contributions-rank
description: >
  Produce a ranked contribution table from a batch of analyzed projects. Read a parent Multica issue
  whose sub-issues (scouts) each analyzed one project and posted a deliverable comment with top picks,
  extract every top-pick contribution, score each against the mmontes11/contributions #contribution-scoring
  rubric, rank descending, and post the table on the parent issue. Use whenever the user wants a
  cross-project ranking of the contributions the scouts surfaced — "rank the contributions", "build the
  contribution scoring table", "which contributions are most likely to be merged first", "produce the
  contribution ranking for the analyzed projects". Read-only against the repos — it never forks, edits
  code, or opens PRs.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires the multica CLI and read access to the parent Multica issue and its scout sub-issues. The scoring rubric is read live from the mmontes11/contributions README #contribution-scoring section — do not restate or hardcode it. Read-only.
allowed-tools: Read, Grep, Bash(multica:*), Bash(gh:*)
---

# Rank the contributions

Take a set of analyzed projects — a parent Multica issue whose **sub-issues** each scouted one project —
and produce a single ranked table of the contributions their scouts surfaced, sorted by **likelihood of
being merged first**.

## Contract

The scoring rubric is the **`#contribution-scoring`** section of the
[mmontes11/contributions](https://github.com/mmontes11/contributions) README — the single source of truth.
Read it live at the start of the run (clone or `gh` fetch the README; never rely on a memorized copy).
This skill is the *workflow* — it does not restate the rubric's points or signals.

**The table is ephemeral.** It changes frequently (scouts land, contributions get claimed, PRs open), so
it is posted **as a Multica comment on the parent issue** and is **never pushed** to
`mmontes11/contributions` or any other repository.

## Inputs

- **The parent Multica issue id** — the batch under analysis; its sub-issues are the scouts.
- **Each scout's deliverable comment** — the comment on the sub-issue containing the investigation
  outcome and its top-pick contribution(s).

## Procedure

1. **Locate the batch.** Read the parent issue (`multica issue get <id> --output json`) and list its
   sub-issues (`multica issue children <id> --output json`). Each sub-issue = one analyzed project.
2. **Gather the top picks.** For every scout sub-issue, read its comment history and extract the
   **deliverable comment** — the one stating the top-pick contribution: its issue/PR reference (with
   URL), the project, and the scout's notes (labels, maintainer intent, size, competing PRs, DCO/CLA,
   star count). Skip sub-issues that have no deliverable comment yet.
3. **Score each contribution.** Apply the README's `#contribution-scoring` rubric (0–10) to every
   top-pick, using only the evidence the scout recorded. Do not re-investigate the repos yourself. Where
   the scout's comment lacks a rubric input (e.g. no star count), record the gap in the "Why" column
   rather than guessing.
4. **Rank descending.** Order by score (desc); break ties by strength of maintainer intent, then by
   smaller effort.
5. **Post the table on the parent issue** (`multica issue comment add <parent-id> --content-file
   <path>`). The comment carries:
   - A one-line framing (what was ranked, across how many scouts).
   - A **rubric recap** — the short signal/point list copied from the README so the reader can audit
     scores without opening the repo.
   - The ranked table: `# | Contribution (linked) | Project | Score | Why`. One row per contribution.
   - A short **read of the field** paragraph: the natural start-first set, anything meaningfully
     blocked, and what is effectively a no.
   - A closing line: **no fork or PR was opened in this pass — this is the ranking only.**

## Rules

- **Read-only.** Never fork a repo, edit code, or open a PR — this step only ranks.
- **One table, one comment.** Consolidate all scouts into a single ranked table; do not post one
  comment per project.
- **Ground every score in the rubric.** Each row's "Why" must name the signals that produced the points,
  so the ranking is auditable against the README.
