---
name: polish-new
description: Pre-release code review that converges - parallel review agents sized to the diff, findings validated against evidence in a run ledger, fixes on approval, then re-reviews its own fixes until a round warrants no edits. Run on /polish-new.
metadata:
  version: "0.1.3"
  categories: "development"
  topics: "code-review, linting, refactoring, pre-release, diff-review"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/polish-new
    emoji: "✨"
argument-hint: "[base-ref]"
---

# Pre-Release Polish

A review is finished when a review of its own fixes warrants no further edits -
not when the fixes are written, not when checks pass. Evidence beats judgment: a
finding that cannot be reproduced from its own citations does not survive. The
fix pass is where the next round's defects come from, so it gets reviewed like
any other code. Findings live in files, not in this conversation - context can
be compacted away mid-run; if you are resuming after a compaction or
interruption, re-read `ledger.md` and the saved agent reports before continuing.
They are the source of truth, not the summary.

A base ref may be passed as an argument; Phase 2 uses it for scope.

## Phase 0: Orient

Work in the repository under review - it may be a worktree, not the current
directory. Establish state there:

```
git rev-parse --abbrev-ref HEAD
git status --short
git diff --stat
```

Create the run directory `.agents/polish/<YYMM-DD-HHMM>-<slug>/` with an
`agents/` subdirectory, and start `ledger.md` recording the reviewed sha
(`git rev-parse HEAD`) and, as they launch, one row per agent (lens, shard,
output file, launch time, plus any run identifier the harness exposes).
Base ref and diff stat are backfilled at the end of Phase 2. Findings get ledger
rows as reports arrive, not later.

If `.agents/` is not already ignored, add `.agents/polish/` to the project's
ignore file - run artifacts are working state, never committed.

The reviewed sha makes this review a certificate about one snapshot. Anything
committed after it is unreviewed; a later run scopes to `<reviewed-sha>..HEAD`.

## Phase 1: Automated Checks

Run the project's lint + type-check command. Check CLAUDE.md (or the equivalent
project instructions) for the correct validation command - commonly `pnpm check`,
`just check`, `cargo clippy`, `uv run ruff check`. If none is documented, ask.

If checks fail: fix all errors, re-run until clean, then continue. Do not start
the review against a failing gate. When a failure predates the diff (it
reproduces on the base ref), still fix it - but record it in the ledger as
`pre-existing gate failure, fixed` and surface it in the report.

## Phase 2: Map

Resolve the base ref: the argument if one was passed; else the repository's
default branch (`git symbolic-ref refs/remotes/origin/HEAD`, falling back to
whichever of `main`/`master` exists); if neither resolves or there is no merge
base (shallow clone, detached HEAD), say so and ask the user for a base.

Scope is a **union**: `<base>...HEAD`, plus staged and unstaged changes, plus
untracked (`??`) source files. The reviewed-sha certificate must be true of the
whole union. If the work under review was committed this session, the branch side
narrows to those commits. A staged change that references an untracked file is
itself a finding: without the file, fresh checkouts and CI break. If nothing
changed at all, report "nothing to review" and stop.

Write the diff to a file in the run directory. `git diff` does not emit
untracked files - append each one via `git diff --no-index /dev/null <path>`,
and include untracked paths in the changed-file list handed to agents. Exclude
lockfiles and generated outputs (`Cargo.lock`, `pnpm-lock.yaml`, `*.snap`,
generated bindings) - but never a plan or spec document the branch implements:
that is review input. For moved or rewritten code, note the prior version
(`git show <ref>:<path>`) for agents to compare behavior against. Backfill the
ledger header: base ref, diff stat.

Read the diff's **structure**, not every line: which subsystems it touches and
which control flows it changes. Then produce the shard plan and arm the
conditional lenses.

**The shard plan.** If the diff is tiny (under ~50 changed lines), skip the
finder agents and review all lenses yourself, reading every changed line - the
fast path skips ONLY the finder fan-out; the run directory, ledger, evidence
standard for your own findings, skeptics on your confirmed correctness findings,
report, approval gate, fix pass, and fix review all still apply. Otherwise one
agent per lens. When a lens's share would exceed roughly 1500 lines of diff,
split that lens across shards - enumerate the lens's natural units and assign
each agent a few, drawing boundaries so control flows stay intact:

| Lens | Shard unit - enumerate these to shard |
|---|---|
| Cleanliness | files - the only genuinely local lens |
| Efficiency | hot paths (per-frame/per-request/per-render/per-log-line/per-CI-run work) and shared resources (memory limits, locks, caches, stores, pools, declared timeouts), each traced end to end |
| Design & Reuse | subsystems, with whole-diff visibility |
| Side-Effect Gating | side-effect flows - each costly or irreversible action the diff introduces or relocates (charges, writes, deletes, mutating external calls, notifications), traced entry point to effect |

A shard assigns **accountability, not visibility**: every agent gets the full
diff and may read anything in the repository; it is answerable for complete
coverage of its shard.

**The conditional lenses.** Arm Control Verification if the diff touches a
security control (credentials, auth, permissions, payments, sandboxing, input
validation at a trust boundary). Arm Plan Conformance if a plan or spec document
for this branch exists.

## Phase 3: Find

Launch all agents concurrently. Every agent this skill spawns - finder, skeptic,
dive, fix-review - receives the Agent Contract verbatim; finders also receive
their lens section verbatim, plus:

- The diff file path, the changed-file list, and their shard assignment
- Project constraints from CLAUDE.md (performance assumptions, logging conventions, platform quirks) so findings are domain-correct
- Known-intentional patterns, marked as *prior decisions to re-verify*, not as suppressions. A decision recorded as settled can still be the bug

Save each agent's report **verbatim** to `agents/<lens>[-<shard>].md` as it
lands. Do not summarize into the conversation and discard the original.

### Agent Contract

- Read every changed file in your shard fully before judging it - never assess code you have not opened
- Only flag real issues, not style preferences already handled by the formatter
- The diff is the hunting scope - review the changed code, don't audit the whole repo. But anything real you surface along the way (a pre-existing flaw the diff touches, a stale sibling path, an adjacent issue) is a finding, tagged `(pre-existing)` or `(out of diff)`
- Every finding carries reproducible evidence: the code site as `file:line`, the check performed as an exact command with its observed output (for a purely code-local finding, the quoted code itself is the check), and the source of any external fact as a path or URL. A finding whose evidence cannot be reproduced from its citations is a claim, and claims do not survive validation
- Chase every thread to resolution inside your own context; do not defer work you can finish
- Never report a category clean without saying what was traced
- End with an **Unresolved suspicions** section: what you smelled but could not run to ground, and what would settle it. It is mandatory and may not be empty on the grounds that everything was checked - if nothing is unresolved, say what you would look at with more time

### Lens 1: Cleanliness

Fast, mechanical, high-confidence. Junk that should be removed.

- **Debug leftovers**: `console.log`, `console.debug`, `console.warn` added during development; temporary debug variables, hardcoded test values. NOT structured logger calls
- **AI slop**: comments explaining obvious code - flag each individually; JSDoc on internal functions that aren't public API; verbose docstrings on simple helpers; `TODO`/`FIXME`/`HACK` markers left by the agent; unnecessary type annotations where the language infers; emoji in code (unless the project uses them); references to plan phases or section numbers meaningless to a reader of the code
- **Non-ASCII punctuation**: em-dashes, smart quotes, other unicode punctuation in changed lines (unless the project uses them). Scan byte-aware, e.g. `rg -n '[\x{2010}-\x{2015}\x{2018}-\x{201F}]'` - a plain-text grep over a diff misses multi-byte characters
- **Dead code**: unreferenced functions, variables, types; fields written but never read; commented-out blocks; unused parameters (unless required by an interface). Verify with a repo-wide search before flagging
- **Unused imports**: added but never referenced, or left behind after refactoring
- **Hardcoded values**: magic numbers or strings that should be constants; a literal where the same package already names that exact value; URLs, prices, limits belonging in config. NOT `0`, `1`, `true`, HTTP status codes
- **Stale doc comments**: a comment describing behavior the diff changed, a doc block split or orphaned by a move, a comment promising something the code no longer does

### Lens 2: Design & Reuse

Requires exploring beyond the diff. Structural and design issues.

- **Reuse opportunities**: search for existing utilities, helpers, and shared modules that could replace newly written code. Flag hand-rolled logic where a utility exists. Name the exact symbol and path - a reuse suggestion naming something that does not exist is worse than no finding
- **Duplication**: near-identical blocks that should be unified; a helper introduced in this diff while an older twin survives elsewhere; a second implementation of a policy that must not drift from the first
- **Over-engineering**: helpers used exactly once; abstractions wrapping a single call; try/catch adding nothing; validation of data already validated at the boundary; flags or config for what could just be code; backwards-compat shims for code just written; a struct wrapping one field
- **Redundant state**: state duplicating existing state; cached values that could be derived; observers that could be direct calls
- **Parameter sprawl**: new positional parameters instead of restructuring; a function whose signature grew past comfortable use when the codebase already has a flags-struct pattern
- **Constant misuse**: a constant used outside the domain its own definition claims - especially where the definition warns against exactly that
- **Leaky abstractions**: exposing internals that should be encapsulated; breaking existing abstraction boundaries
- **Stringly-typed code**: raw strings where constants, enums, or branded types already exist
- **Structural issues**: functions that grew too long (>50 lines, consider splitting); naming inconsistent with codebase conventions; a file that outgrew its concern while the codebase splits by concern
- **Production-dead code paths**: an entry point or helper that only tests reach, especially when the tests then exercise semantics production does not have
- **Behavior drift in relocated code**: compare against the code it replaced. Dropped validation, removed guards or early-returns, changed error semantics. A refactor that changes *behavior* is a regression even when every line looks clean

### Lens 3: Efficiency

Runtime performance and resource issues. Cost concentrates in two places: **hot
paths** (frequency) and **shared resources** (accumulation). Trace your assigned
paths and resources end to end, across files. Do not flag cold paths, one-time
setup code, or scripts that run once - though a real leak or missing timeout on
a cold path still counts.

- **Budget reconciliation**: for each declared ceiling - a timeout, a memory limit, a size cap, an SLA in a comment - sum the actual worst-case cost against it: along the call path for time budgets, across every consumer at peak for shared resources. A limit the sum can exceed is a finding, and the comment stating the budget is part of the defect
- **Redundant work**: repeated computations, repeated reads, duplicate calls, N+1 patterns, the same data decoded or parsed twice along one path
- **Missed concurrency**: independent operations run sequentially
- **Hot-path bloat**: new blocking work on startup or per-request/per-render/per-frame paths. Quantify - measure or benchmark where you can
- **No-op updates**: updates inside polling loops, intervals, or handlers that fire unconditionally without change detection
- **TOCTOU anti-patterns**: pre-checking existence before operating - operate and handle the error
- **Memory and lifecycle**: unbounded structures, missing cleanup, listener or timer leaks; state whose owner is torn down while the state survives - check every teardown path, not the one the diff shows
- **Lock scope**: expensive work done while holding a lock others need; a lock taken on a path that runs at high frequency; re-entrancy hazards
- **Overly broad operations**: reading whole files when a portion suffices; loading all items to filter for one
- **Unchecked system boundaries**: calls without status checks, unhandled rejections, missing error handling at I/O boundaries

### Lens 4: Side-Effect Gating

Closed-scope correctness. Costly or irreversible side-effects that run before the
checks meant to gate them. Does NOT judge whether business logic is correct - that
is broader code review's job.

For each side-effect flow you own:

- **Enumerate every path to the effect** - not only the ones the inventory or the diff shows you. A gate that holds on the two paths under review and not on a third is ungated. Search for alternative entry points: wrappers, tunnels, nested or aliased dispatch, retry paths, encodings of the same command
- **Inventory the gates**: what must precede the effect - input validation, authentication, authorization, precondition checks, idempotency
- **Cross-check ordering**: flag any effect reachable where a gate runs after it, or not at all. Trace ACROSS boundaries - middleware firing an effect before calling the next layer is the prime suspect; the validation that should gate it often lives downstream. Check the CLI or caller side too: an expensive or one-shot resource acquired before the cheap check that would have rejected the request
- **Verify the gate holds on untrusted input**: a check reading values the untrusted side supplies, a parse that fails open, a filter that a different encoding of the same input evades
- **Missing rollback**: a committed side-effect with no compensation when a later step on the same request can still fail
- **Claimed invariants**: where a comment says a state is impossible, verify it. If the code can reach it, the comment is part of the finding
- **Out of scope**: whether business logic is correct, pricing math, algorithmic correctness, anything without a crisp invariant

Every finding cites the side-effect line, the gate it precedes (or "ungated"), and
the control-flow path between them. No finding without two line references.

### Conditional Lens: Control Verification

Only when the diff touches a security control. A control makes a promise: this
input cannot reach that effect, this caller cannot act without that check.
Establish whether it holds on every path - the only way is to hunt for a
counterexample. For each control the diff introduces or modifies, state its
promise, then look for a path where it fails: another route to the guarded
effect, an encoding of the input the filter does not recognize, a parse that
fails open, a check that reads values the untrusted side supplies, ordering where
the control is armed too late or consumed by the wrong event, resource exhaustion
that disables it. Report each failing path with the exact sequence that reaches
it. Where a promise held, say what you tried.

### Conditional Lens: Plan Conformance

Only when a plan or spec document for this branch exists. Read it in full. For each
requirement, decide: implemented as specified, implemented differently, or missing -
and cite the code for each. Flag requirements silently dropped, behavior beyond what
was specified, and any place the implementation contradicts a guarantee the plan
states. The plan's own caveats and known-trap sections are review input: check
whether this implementation walked into one.

## Phase 4: Validate

Findings arrive as claims. Every raw finding from every report gets a row in
`ledger.md` - including findings buried inside an agent's "clean" section,
parenthetical asides, bundled items, and hedged caveats. Those are where true
findings die.

**Reproduce, do not re-derive.** For each finding, run the command it cites and
compare the output; open the exact file and lines and confirm the code matches;
follow the path or URL behind any external fact. You did not read the whole diff,
so your judgment is not the standard - reproducibility is. Drop a finding when the
line number is wrong, the code does not match the claim, the cited symbol does not
exist, the cited command does not produce the claimed output, or the evidence is
missing and cannot be reconstructed. Record every drop with its reason.

Never drop a side-effect, behavior-drift, or bypass finding as "a design decision"
or "out of scope". If it reproduces, it is the highest-severity finding present.

For findings on rewritten or relocated code, check whether the flaw predates the
change; if so keep it, tagged `(pre-existing)`. Separately flag test coverage
deleted with an old path and not replaced.

**Assign each confirmed finding a disposition** in the ledger:

- `fix` - the default
- `not-worth-fixing (reason)` - real, but the fix trades worse than the defect, or the code is a deliberate backstop
- `separate-change (reason)` - real, but fixing it would bloat this change beyond what belongs in it

Judge on long-term codebase benefit: out-of-diff findings default to `fix`, and a
low-risk fix that just makes maintenance easier is a `fix`, not a deferral.

**Escalate where the evidence says there is more.** In parallel:

- One skeptic agent per confirmed correctness, gating, drift, or bypass finding, tasked to refute it: find the guard that makes it unreachable, the caller that makes it safe. Refuted findings go to Dropped with the refutation recorded
- One dive agent per confirmed *mechanism* - not per finding - with the mandate: this broke this way; enumerate every other path to the same effect, every sibling with the same shape, every other consumer of the same resource. Clustered defects are the norm: one confirmed instance predicts more
- One dive agent per unresolved suspicion worth settling

Dive findings re-enter this phase: ledger row, reproduce, disposition, escalate.
Repeat until a round produces nothing new. A clean diff exits after one pass; a
diff with real defects keeps digging until it stops paying.

## Phase 5: Report

Render the report from `ledger.md`. Merge duplicates - if several agents flagged
the same code, one finding, all citations. The counts must reconcile: every raw
finding is in a category with its disposition, or in Dropped with its reason.
Control-verification failures report under Correctness tagged `(control)`; Plan
Conformance gaps under Correctness tagged `(plan)` when behavior is missing or
wrong, under Design when structural only.

```
## Review Findings

Reviewed <sha> against <base>. <N> raw findings: <N> fix, <N> not-worth-fixing,
<N> separate-change, <N> dropped. Ledger: .agents/polish/<run>/ledger.md

### Correctness (N issues)
1. `path/to/file.ts:55` - chargeUser() runs before body validation (handler validates at :78, after next()); a malformed request is charged then 400s - fix
2. `path/to/proxy.ts:258` - every client frame now fully decoded - not-worth-fixing: the prefilter cannot see escaped method names; fail-closed beats microseconds

### Cleanliness (N) / Design (N) / Efficiency (N)
...same shape, one numbered line per finding, disposition last...

### Dropped after validation
1. `path/to/auth.go:88` - claimed bypass; the skeptic showed the parser rejects that encoding at :40 before the filter runs

**Total: X findings - Y to fix now**

**Awaiting approval before proceeding with fixes.**
```

List **Correctness** first, and always - including at `(0 issues)`. A correctness
zero must state what was traced: which side-effect flows were inventoried, which
paths were enumerated, which gates cover them. It must never be batch-approved
alongside cosmetic items. If Phase 1 fixed pre-existing gate failures, say so here.

**Approval semantics**: a bare approval ("go", "proceed", "fix") approves every
finding marked `fix`. The user can override by number ("go, but skip design 2;
also fix efficiency 1") - overridden findings get their disposition updated in
the ledger (`deferred (not approved)` or `fix`), so counts still reconcile. Fix
nothing until the user explicitly approves.

If zero issues survive, report "Clean - no issues found", substantiate the
correctness zero, offer next actions, and stop - a clean report needs no
approval line.

## Phase 6: Fix

All fixes happen in the working tree - create no commits until the very end.
Snapshot the pre-fix state first: `SNAP=$(git stash create); [ -z "$SNAP" ] &&
SNAP=$(git rev-parse HEAD)` - `git stash create` returns nothing on a clean
tree - and record it in the ledger. Then, for each approved finding:

- **Fix the class, not the instance.** Before editing, search for every other site with the same shape - the same ordering, the same missing guard, the same duplicated block, the same teardown path. Fix them together and name the search you ran in the summary. Most repeat findings are a previous fix applied one call site short
- **Read before you write.** Open every function you are about to change, in full, before changing it. Do not edit code you have not read this session
- Make minimal targeted edits - do not refactor surrounding code, and do not add comments, docstrings, or type annotations to code that doesn't have them
- Never pipe the check command through `tail` or `head` and act on its apparent success: the pipeline reports the last command's status, so a failing gate looks green. Capture the exit code and print it
- For every regression test added or strengthened: revert the fix, run the test, confirm it fails, restore. A test that passes without its fix is not a guard - it is a finding

Re-run the project's validation command. Fix anything new. Mark each ledger row
fixed.

## Phase 7: Fix Review

The fixes are unreviewed code written under momentum by someone thinking about a
finding rather than about the code - historically where the next round's defects
come from. Before reviewing, `git add -N` any files the fixes created, or
`git diff` will not show them. Launch a fresh agent over `git diff <SNAP>` (the
working tree against the snapshot), given the ledger, the Agent Contract, and
the lens sections relevant to what changed. It checks:

- Does each fix actually hold - is the claimed invariant true on every path now?
- Is each fix class-complete, or does a sibling site still have the shape?
- Did any fix introduce a new defect, drop a guard, change a return contract, or leave a stale comment, dead symbol, or duplicated policy behind?
- Does each new or strengthened test fail when its fix is reverted?
- Did any fix reverse a decision recorded in the ledger without saying so?

Classify the round's findings and act autonomously - no approval gate here:

- **Defects** - a fix does not hold, is class-incomplete, or introduced a problem: fix them now; the next round reviews only those new edits
- **Residuals** - cosmetic, taste, or not worth an edit: record in the ledger, disclose in the summary, no edit, no new round

**Exit when a round warrants no edits.** Convergence comes from the shrinking
diff: each round reviews only the previous round's edits. Circuit breaker: after
5 rounds stop looping - run the checks and disclose what remains in the summary.

Finish with:

1. Final ledger dispositions - every finding fixed, dropped, deferred, not-worth-fixing, or separate-change, each with its reason. Counts reconcile
2. A summary: what was fixed, what the fix-review rounds found and fixed, residuals disclosed, how many rounds ran, final check status, the run directory path
3. Nothing is committed yet. Ask how to land the fixes: one commit of all of them (default - stage explicit paths, never `git add -A`), fold into existing commits, or leave in the working tree. Push only if asked
