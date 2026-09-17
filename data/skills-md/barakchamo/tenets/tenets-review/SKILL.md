---
name: tenets-review
description: |
  Produces a severity-ranked review of a pull request, a branch, or the uncommitted working tree
  against the tenets engineering ruleset, plus an intent audit comparing what the active plan said
  against what the diff actually does.

  Use only when the user explicitly asks to review changes against the rules — "review this PR",
  "review my diff against the tenets", "did I build what the plan said". Not for ordinary code work,
  writing code, or auditing a whole codebase: those load the tenets skill or tenets-audit.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git merge-base:*) Bash(git symbolic-ref:*) Bash(git rev-parse:*) Bash(git branch:*) Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh repo view:*)
metadata:
  version: '1.0.0'
  requires: 'tenets >= 2.0.0'
---

# Tenets review

Read-only. Never commit, push, amend, post a PR comment, or apply a fix. Fixing is
`/tenets-realign`'s job, and shipping is not this skill's business at all.

## Locate the ruleset

`<ruleset>` below is the `tenets` skill directory installed beside this one — **not** a path
relative to the working directory. Resolve it once, in this order, and use it for every path after:
`.claude/skills/tenets/`, `.agents/skills/tenets/`, then a glob for `**/skills/tenets/SKILL.md`
outside `node_modules`. Nothing found → stop: `State: BLOCKED — install the tenets ruleset skill
(skills add BarakChamo/tenets --all)`.

## Arguments

Target: `$ARGUMENTS`. If that is empty or still contains a literal `$ARGUMENTS` or `{{args}}`,
resolve the target from git state per the chain below. A target may be a PR number or URL, a branch,
a ref range (`main...feature`), or a path.

## Phase 1 — Load the shared contracts

Read `<ruleset>/workflow/scope.md` and `<ruleset>/workflow/findings.md`; read `<ruleset>/rules/09-code-review.md`,
which owns the severity vocabulary and the review checklist. If those paths do not resolve, stop:
`State: BLOCKED — install the tenets ruleset skill`. Check `metadata.requires` against the ruleset's
`metadata.version` and say which side is stale on a mismatch.

## Phase 2 — Resolve scope, before anything expensive

Walk `scope.md`'s git scope modes in order and **name the rung used** in your first output line. A
repository with no remote and no upstream is normal — fall through rather than erroring.

Hard stops: clean tree with `HEAD` at base → `Review: nothing to review — clean tree on <base>.`;
`gh` missing or unauthenticated for a PR target → `State: BLOCKED — gh auth login`; over the review
ceiling in `scope.md` → `State: NEEDS_CONTEXT`, or proceed on the largest files and record the
omission in the summary.

## Phase 3 — Find the stated intent, before reading the diff

Order matters: intent read after the diff is intent rationalized from the code.

1. the plan in this conversation, if the session has one;
2. the guide's plan or decisions location in the repository — the only plan location that exists in
   every harness;
3. the host's own plan directory when it has one, as an opportunistic extra;
4. the PR body, when the target is a PR;
5. commit messages on the branch.

Name the winning source in one line. With nothing found, state the requirement you infer from the
diff in one sentence and cap every intent finding at confidence 3 (`findings.md`).

## Phase 4 — Intent audit

Always inline, never delegated. One flat line per plan item:

```text
plan: "slice 2 — typed error for provider timeout" → partial: err type added (packages/greetings/src/greet.ts:31); no test asserts it.
```

Classify each as `done`, `partial`, `missing`, or `undeclared`. Then judge work the plan never
mentioned: beyond trivial (more than ~10 lines, or any new export, dependency, or config change) it
becomes a finding — scope creep is `[REQUIRED CHANGES] Rule 11.1`; an unplanned root-config or
dependency change is `[BLOCK] Rule 7.8`. Drift that is merely unlisted, small, and coherent with the
requirement is reported as informational and never blocks.

## Phase 5 — Review the diff

Read the changed files, not only the hunks — a diff hides the context a contract lives in. Work
Rule 9.2's checklist, then the dimension checklists in `<ruleset>/workflow/checklists/` that the
diff's signals select, per `scope.md`. Fan out only above the threshold; above the adversarial
threshold, run a second pass over the findings asking what the first pass missed.

Pre-existing issues are out of scope unless the change worsens them or they are safety, correctness,
or data-loss risks (Rule 9.4). Count what you suppressed.

## Phase 6 — Report

Findings by severity per `findings.md`, empty groups omitted, then the intent-audit lines, then the
summary line with the Rule 9.4 decision:

```text
Review: REQUEST CHANGES — 1 BLOCK, 2 REQUIRED, 4 SUGGESTION, 0 MINOR; intent 3 done / 1 partial / 1 undeclared; plan docs/work/decisions/slug.md; scope dirty-tree 12 files / 340 lines; gate not run; suppressed 2 pre-existing, 3 low-confidence.
```

The acceptance gate is **reported, not run**: name it and offer to run it in one line. Clean review
still names residual risk and any check not run.

## Standing rules

- Findings cite an anchor and a path and line actually read; a "this is fine" claim names the test
  or line that proves it.
- Flag only what affects correctness, safety, or the stated requirement. Chasing every conceivable
  gap produces defensive code and abstraction nobody asked for.
- Never weaken or delete a test to make the diff pass review; a failing assertion is evidence
  (Rule 10.2).
- Three failed attempts at any step escalates per the state protocol rather than looping.
