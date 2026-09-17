---
name: tenets-audit
description: |
  Produces a severity-ranked compliance report for an entire repository, a package, or a named
  subtree, measured against the tenets engineering ruleset and the project guide, with every finding
  cited to a rule anchor and a file location.

  Use only when the user explicitly asks to audit or assess a codebase against the rules — "audit
  this repo", "check compliance", "how aligned is this package". Not for ordinary code work,
  single-file edits, reviewing a diff, or answering a rules question: those load the tenets skill.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(git ls-files:*) Bash(git diff:*) Bash(wc:*)
metadata:
  version: '1.0.0'
  requires: 'tenets >= 2.0.0'
---

# Tenets audit

Read-only. This skill never edits code, never commits, and writes a report file only when the user
asks for one or names a path.

## Locate the ruleset

`<ruleset>` below is the `tenets` skill directory installed beside this one — **not** a path
relative to the working directory. Resolve it once, in this order, and use it for every path after:
`.claude/skills/tenets/`, `.agents/skills/tenets/`, then a glob for `**/skills/tenets/SKILL.md`
outside `node_modules`. Nothing found → stop: `State: BLOCKED — install the tenets ruleset skill
(skills add BarakChamo/tenets --all)`.

## Arguments

Scope: `$ARGUMENTS`. If that is empty or still contains a literal `$ARGUMENTS` or `{{args}}`, audit
the repository root and say so in the first output line. The scope may be one or more paths, a
workspace name, or a rule anchor to audit for specifically (`Rule 02.1`). `--report [path]` writes
the report to disk in addition to reporting inline.

## Phase 1 — Load the shared contracts

Read `<ruleset>/workflow/scope.md` and `<ruleset>/workflow/findings.md`. If that path does not
resolve, stop: `State: BLOCKED — install the tenets ruleset skill (skills add BarakChamo/tenets
--all)`. Check `<ruleset>/SKILL.md`'s `metadata.version` satisfies this skill's
`metadata.requires`; on a mismatch say which side is stale before continuing, since anchors cited
against an older ruleset may not exist.

## Phase 2 — Stop conditions, before reading any source

- The named scope does not exist → `State: BLOCKED`, naming the path.
- No source files under scope → `Audit: n/a — no source files under <scope>.` Stop.
- Over the audit ceiling in `scope.md` with no scope argument → `State: NEEDS_CONTEXT`, naming the
  three largest candidate subtrees. Do not audit a huge repository unscoped.

## Phase 3 — Load context

Discover and read the project guide per `scope.md`, but only the slots the audit column lists. Read
the language profile the guide names. **Do not read all 15 rule files** — the dimension table says
which rules each unit needs, and per-task loading is the point of the ruleset.

With no project guide, open with the degradation line from `scope.md` and suggest `/tenets-init`
once.

## Phase 4 — Measure and select

Measure the scope with the commands in `scope.md`, then pick dimensions by their trigger column.
Emit one status line before working:

```text
Rules: 09 (+ per dimension) · scope apps/api 42 files / 3,100 lines · dimensions 1,2,3,4 · mode parallel(4)
```

## Phase 5 — Run the units

Follow `scope.md`'s parallel-or-sequential rule. Each unit gets its checklist file's text, the rule
and profile paths it needs, its file list, and the return schema from `findings.md`. A unit reads
the files in its list and answers its checklist against them — it never guesses from filenames.

Above the adversarial threshold, run one more pass over the findings already produced: challenge
each anchor, verify the cited line says what the finding claims, and check severity is not inflated.

## Phase 6 — Consolidate

Merge per `findings.md`: dedup by fingerprint, drop low confidence, collapse repeated anchors, sort
by severity then path. Report a unit that failed or returned nothing as `dimension <n>: no result`.

## Phase 7 — Reconcile recorded deviations

Findings whose anchor appears in the guide's recorded-deviations section are **dropped**, and
reported once as a single MINOR line naming the guide and the number suppressed. The guide is
authoritative over the rules for that project (Rule 9.4). A deviation that looks wrong is worth
mentioning in prose; it is not a finding.

## Phase 8 — Report

Findings first, grouped by severity with empty groups omitted, then a one-line verdict per dimension,
then the summary line from `findings.md`. Close with the top three by risk when there are more than
ten findings.

Write a file only when asked or given a path; default name
`<the guide's plan or decisions location>/tenets-audit-<yyyy-mm-dd>.md`, same body plus a header
naming the scope, mode, and thresholds used.

## Phase 9 — Hand off

With a BLOCK, or three or more REQUIRED CHANGES, add one line: `/tenets-realign <scope>` produces an
ordered slice plan for these findings. Never start realigning from inside this skill.

## Standing rules

- Every finding cites a rule anchor and a path and line actually read. No anchor, no finding above
  SUGGESTION.
- Clearing a concern needs the same evidence as raising one (`findings.md`).
- Flag only what affects correctness, safety, or a stated requirement — a reviewer told to find gaps
  will invent them.
- Counts in the summary come from commands actually run, never estimated, and the summary names
  every check that was skipped.
- Three failed attempts at any step escalates per `findings.md`'s state protocol rather than looping.
