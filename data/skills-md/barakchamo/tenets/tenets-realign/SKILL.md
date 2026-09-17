---
name: tenets-realign
description: |
  Brings existing code back into line with the tenets ruleset: audits the named scope, clusters the
  findings into an ordered slice plan, waits for approval, then applies the approved slices one at a
  time with the project's acceptance gate green and one commit per slice.

  Use only when the user explicitly asks to realign, refactor, or fix a codebase against the rules —
  "realign this package to the tenets", "fix the rule violations in apps/api". Not for ordinary code
  work, a single edit, or a read-only assessment: those load the tenets skill or tenets-audit.
disable-model-invocation: true
allowed-tools: Read Glob Grep Edit Write Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git branch:*) Bash(git rev-parse:*) Bash(git add:*) Bash(git commit:*) Bash(git checkout --:*)
metadata:
  version: '1.0.0'
  requires: 'tenets >= 2.0.0'
---

# Tenets realign

This skill writes code. Its safety comes from the stop conditions and the approval gate below, not
from tool configuration.

**Never**: push, force-push, amend an existing commit, `git reset --hard`, touch a file outside the
approved slice, edit the rule files or the project guide, or commit with the gate red. One commit
per slice, and nothing is edited before the user approves.

## Locate the ruleset

`<ruleset>` below is the `tenets` skill directory installed beside this one — **not** a path
relative to the working directory. Resolve it once, in this order, and use it for every path after:
`.claude/skills/tenets/`, `.agents/skills/tenets/`, then a glob for `**/skills/tenets/SKILL.md`
outside `node_modules`. Nothing found → stop: `State: BLOCKED — install the tenets ruleset skill
(skills add BarakChamo/tenets --all)`.

## Arguments

Scope: `$ARGUMENTS`. If that is empty or still contains a literal `$ARGUMENTS` or `{{args}}`, stop:
`State: NEEDS_CONTEXT — name a scope (a path, package, or rule anchor); an unbounded whole-repo
realign is not a slice.` A trailing `-- "<command>"` overrides the acceptance gate command.

## Phase 1 — Shared contracts and preconditions

Read `<ruleset>/workflow/scope.md` and `<ruleset>/workflow/findings.md`; read
`<ruleset>/rules/10-decision-framework.md` and `<ruleset>/rules/11-change-delivery.md`. Missing
path → `State: BLOCKED — install the tenets ruleset skill`.

Then check the working state, in this order:

- Dirty tree → `State: BLOCKED — commit or stash first; realign needs a clean baseline so each slice
  reverts cleanly (Rule 11.2).`
- Detached HEAD, or on the default branch when the guide's branching model protects it → require a
  branch, propose a name, and **do not create it** unasked.
- No acceptance gate command (no guide, or the guide names none, and no `--` override) →
  `State: BLOCKED — a commit without the gate violates Rule 11.2. Run /tenets-init, or pass the gate:
  /tenets-realign <scope> -- "<command>".`

## Phase 2 — Audit the scope

Run the audit procedure over the scope: the phases in `tenets-audit`'s skill from context load
through deviation reconciliation, using the same checklists, thresholds, dedup, and guide slots. Do
not restate that logic here and do not invent a second set of checks.

## Phase 3 — Cluster into slices

One slice is **one anchor family in one ownership boundary**. Merge same-anchor findings inside a
workspace; give any public-contract change its own slice. Findings that need a product decision are
not sliced at all — they go to a `needs decision` list in Rule 10.6's pushback shape. SUGGESTION and
MINOR findings stay out of the plan unless the user asks for them.

Order is fixed:

1. safety, security, and data-loss BLOCKs;
2. missing tests before the behavior they pin — a characterization-test slice precedes any
   behavior-touching slice in the same module (Rule 4.2);
3. primitives and boundaries before their callers (schema or typed error at the boundary, then call
   sites), which minimizes re-touching;
4. structural moves — workspace-boundary fixes, export narrowing — once their tests exist;
5. documentation and preambles last, batched into one slice.

## Phase 4 — Approval gate

Print the numbered slices, each with its name, anchors closed, file list, gate command, and expected
diff size; then the verdict line; then exactly this and **stop**:

```text
Approve: "all", a slice list (e.g. 1,3), or "no". Nothing is edited until you answer.
```

Silence or an ambiguous answer means no. Approval covers only the listed slices and only their
listed files; a slice that turns out to need a file outside its list stops and re-asks. Under a
read-only or planning mode, print the plan and stop regardless of the answer.

## Phase 5 — Execute, one slice at a time

For each approved slice, in order:

1. edit only the files that slice listed;
2. run the gate command;
3. green → one commit, message imperative, carrying the why and the anchors closed
   (`Parse api request bodies with the owning schema (Rule 02.1)`), never a file list;
4. red → do not commit. Fix and retry, at most **three attempts** (Rule 6.2), then
   `git checkout --` **only that slice's files**, mark the slice BLOCKED, and continue with the next
   independent slice. Slices that depended on it become `SKIPPED(dep on N)`.

Never re-audit and re-slice mid-run — findings shift underfoot and the approved plan stops meaning
anything. A violation noticed while editing outside the current slice is recorded as a finding for
the next run, never fixed opportunistically.

## Phase 6 — Report

One line per slice, then the summary:

```text
slice 2 — Result at the api boundary: COMMITTED a1b2c3d (gate green, 3 files)
slice 3 — narrow greetings exports: BLOCKED after 3 attempts — <last failing gate line>
Realign: 3 committed, 1 blocked, 1 skipped; 6 findings remain (0 BLOCK, 2 REQUIRED, 4 SUGGESTION); branch realign-api; not pushed.
```

Any BLOCKED slice makes the state `DONE_WITH_CONCERNS` and earns an offer — never an unasked write —
of a three-line learning entry for the guide's inbox (Rule 6.2).
