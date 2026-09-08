---
name: maintenance-routine
description: Use when running a scheduled mechanical maintenance pass over a repo — dead code removal, useless-test pruning, layering-violation fixes, duplicate unification, logic bugfixing, logic simplification, or excess-abstraction flattening. Invoked as `/cadence:maintenance-routine <archetype>`, typically from a scheduler (cron, a CI schedule, or an agent workbench's time trigger). One archetype per invocation; opens PRs and never merges. NOT for reviewing a PR (use pr-review), NOT for ad-hoc refactoring the user asked for directly.
---

# Running a Maintenance Routine

## Overview

A **routine** is one mechanical maintenance pass, run on a schedule, that either opens a small reviewable PR or reports that it found nothing. Seven archetypes ship with this skill. Each has its own qualification test; all of them share one contract.

Routines exist because the maintenance nobody has time for — dead code, tests that cannot fail, layering drift, duplicates that drift apart — is exactly the work that survives being done mechanically, *provided* the qualification bar is high enough that a "no findings" result is normal and acceptable.

**This skill supplies the method. The repo supplies the parameters.** Scan scope, forbidden paths, verification commands and the framework traps that defeat static search are all repo-specific and live in `.claude/routines.md` in the target repo. That split is deliberate: the routine's own tuning loop is "a PR gets rejected → adjust the routine" and the adjustable half has to be inside the repo the routine can open PRs against.

**Scope**: one archetype per invocation. Running several is the scheduler's job — stagger them so they do not compete for the same runner.

## Invocation

```
/cadence:maintenance-routine <archetype>
```

`<archetype>` is one of the seven below. From a scheduler, the whole prompt can be that one line.

| Archetype | What it does | Objectivity |
|---|---|---|
| `dead-code-removal` | Deletes code provably unreachable by static search | highest |
| `useless-test-pruner` | Finds tests that cannot fail; fixes them, deletes only as a last resort | high |
| `abstraction-police` | Fixes violations of layering rules the repo has written down | high |
| `dup-unifier` | Converges duplicate implementations that provably change together | medium |
| `logic-bugfixer` | Models one module against its spec and fixes real bugs, test-first | medium |
| `logic-simplifier` | Untangles logic inside a single function | low |
| `abstraction-improver` | Flattens indirection layers that carry no meaning | lowest |

Objectivity predicts first-round merge rate. When adopting routines in a new repo, enable the top of this table first and only add the lower rows once the earlier ones are landing.

**Scheduler hygiene**, whatever fires the run — the specifics belong in the target repo's own operator docs, but three things hold everywhere:

- **Pin the model explicitly** if the scheduler exposes one. Left blank it inherits a default, and the default is usually the expensive one — a poor trade for work this mechanical.
- **Do not carry state between runs.** Each run starts cold and reads the repo. Scheduler-side session memory gets reclaimed on its own schedule, so a routine that depends on remembering last time will silently start over.
- **Stagger the schedules** against whatever concurrency limit the runner enforces. Same-minute triggers queue up and hold their workspaces while they wait.

## Preflight — all four gates must pass before any scanning

**1. Load the repo config.** Read `.claude/routines.md` in the target repo.

If it does not exist, **stop**. Do not infer scope, forbidden paths or verification commands from the codebase — guessing them is how a routine ends up editing migrations. Print the template from [Repo Config Schema](#repo-config-schema), say it needs to be filled in and committed first, and end the run.

**2. Load the archetype.** Read `routines/<archetype>.md` next to this file. It defines the qualification test, the workflow, the PR body sections and the per-run PR cap. Its rules are additive to this file, never a relaxation of it — where the two differ, the stricter one wins.

**3. Detect the forge.** `gh` for GitHub, `glab` for GitLab. Check which is installed and authenticated:

```bash
gh auth status 2>/dev/null || glab auth status 2>/dev/null
```

Neither → stop, report it. This skill's examples use `gh`; the `glab` equivalents are in [Forge Commands](#forge-commands). "PR" below means MR on GitLab.

**4. Establish a green baseline.** Run the config's verification commands at HEAD *before changing anything*.

If the baseline is red, **stop and report which command failed**. Do not attempt to fix it — a routine that arrives to delete dead code and leaves having repaired an unrelated broken test is out of scope, and worse, a red baseline makes every later "my change is safe" claim unfalsifiable. A broken HEAD is a human's problem.

Record the baseline output. You will diff against it later.

## The Routine Contract

Every archetype obeys all of this. Archetype files restate the parts they most often get wrong; that repetition is intentional.

**Open PRs. Never merge.** Not with `--auto`, not when CI is green, not when the change is trivial. Merge is a human decision. This is the single invariant that makes the whole mechanism safe to run unattended.

**No findings → no PR.** An empty or padded PR is worse than silence: it costs review attention and it corrupts the merge-rate signal that tells you whether the routine is worth running. Ending with "scanned X, considered Y and Z, neither cleared condition 3, opened nothing" is a **successful** run. Say so plainly rather than reaching for something marginal.

**Respect the per-run PR cap.** Each archetype file states its own (1–3). The cap is about reviewer throughput, not about how much you found. Surplus candidates go in `## Observations`.

**Name branches for accounting.**

```
claude/<archetype>/<YYYY-MM-DD>-<n>
```

`<n>` starts at 1 within a run. This is what makes merge rate computable without instrumenting anything — see [Merge-Rate Accounting](#merge-rate-accounting). Do not improvise a different scheme.

**Stay out of the forbidden paths.** The config's list, plus these, which hold in every repo:

- **Spec and decision records** — architecture docs, ADRs, domain glossaries, feature specs, archived change records. For several archetypes these files are the *oracle* the work is judged against. Editing your own oracle is not maintenance. If you believe a rule is wrong, that goes in `## Observations` for a human to turn into a decision.
- **CI workflow definitions** — a routine must not be able to weaken the checks that gate its own PRs.

Nothing enforces this at the platform level. Branch protection and human review are the real defense; the list lowers the odds of getting there.

**Do not fix what you notice in passing.** A routine that wandered off its archetype produces a diff nobody can review against a stated intent. Real bugs spotted while pruning tests, schema problems found while chasing a logic bug, "while I was here" cleanups — all of it goes in `## Observations`.

**Every PR body carries `## Verification` and `## Observations`.** Archetype files add their own required sections. `## Verification` pastes the actual command output, not a claim that it passed. `## Observations` is never omitted — write `none` when there is nothing.

**Keep PRs single-topic and small.** Archetype files set line ceilings. Over the ceiling means split, not "just this once".

## Workflow

1. Preflight (all four gates).
2. Pick this run's target — subdirectory, module, or whatever unit the archetype rotates over. Prefer areas untouched recently; `git log --since='60 days ago' --name-only` shows which parts of the tree are cold. State the choice and the reason in the PR body.
3. Enumerate candidates.
4. Apply the archetype's qualification test to each. This is where most candidates die, and that is the design working.
5. Make the change for the survivors, up to the PR cap.
6. Run the full verification suite. Compare against the baseline.
7. Open the PR(s), or report that nothing qualified.

## Verification

Run the config's commands verbatim. A candidate whose change does not come back green is abandoned, not debugged into submission — write it up in `## Observations` and move on.

Paste real output in `## Verification`. When an archetype requires a red-then-green demonstration (`logic-bugfixer`'s failing test, `abstraction-police`'s new lint rule), both halves are required.

**Leave the tree clean.** Archetypes that temporarily mutate source to test something (`useless-test-pruner`, `logic-simplifier`) must restore it and confirm with `git status` before continuing. A mutation that leaks into a PR discredits every routine PR that follows it.

## Merge-Rate Accounting

The branch naming convention is the entire instrumentation. After a couple of weeks:

```bash
# GitHub
gh pr list --search "head:claude/<archetype>" --state all \
  --json number,state,mergedAt,title

# GitLab
glab mr list --source-branch "claude/<archetype>" --all
```

A routine landing well below the others is a routine whose qualification test is too loose or whose repo config is missing a trap. Tighten the archetype's conditions or add to `.claude/routines.md` — then let the next tick pick up the change.

## When Nothing Qualifies

Report, in the run output rather than a PR:

- Which target was scanned and why it was chosen
- Which candidates were considered
- Which condition each one failed

This is the most common outcome for the lower-objectivity archetypes and it is not a failure. Padding it into a PR is.

## Forge Commands

| Purpose | GitHub | GitLab |
|---|---|---|
| Create PR | `gh pr create --head <branch> --title T --body-file -` | `glab mr create --source-branch <branch> --title T --description "$(cat -)"` |
| Auth check | `gh auth status` | `glab auth status` |
| List by branch | `gh pr list --search "head:<prefix>"` | `glab mr list --source-branch <prefix>` |

Pass PR bodies via `--body-file -` / stdin. Multi-line bodies through shell arguments get mangled.

On GitLab, never pass `--merge-when-pipeline-succeeds` (or `--auto-merge`). It violates the never-merge invariant.

## Repo Config Schema

`.claude/routines.md` in the target repo. Everything here is repo-specific by definition — this skill has no defaults for any of it.

````markdown
# Maintenance routine config

## Verification

Commands every routine runs, in order, before opening a PR. Include whatever
build step the tests depend on — a missing one produces failures that look
like the routine's fault.

```bash
<install command>
<build command, if the test run needs built artifacts>
<lint command>
<test command>
```

## Forbidden paths

| Path | Why |
|---|---|
| `<glob>` | `<reason a human can check>` |

## Spec sources

Where the written rules live. `abstraction-police` and `logic-bugfixer` use
these as their oracle; every archetype treats them as read-only.

| What | Where |
|---|---|
| Architecture constraints | `<path>` |
| Decision records | `<path>` |
| Domain glossary / state-machine invariants | `<path>` |

## Commit conventions

Anything a commit lint will reject: title format, body line length, allowed
scopes.

## Dynamic-reference traps

Constructs that look unreferenced to static search but are live: framework
convention files, glob-loaded test files, string-keyed dispatch tables,
cross-package boundaries, config that names symbols as strings, and any
deliberately-retained transitional code. Each entry: what it is, how to
recognise it, and that the routine must skip it.

## Per-routine

### <archetype>

Scan scope, rotation order, or archetype-specific exclusions. Omit an
archetype to accept the defaults in its file.
````

Sections may be empty but should not be absent — an empty **Dynamic-reference traps** is a claim that the repo has none, and it should be a deliberate claim.

## Design Notes

- **The qualification test is the product.** Each archetype's value comes from what it *refuses* to do. A routine that opens a PR on every run has a broken test, not a productive one.
- **Method here, parameters in the repo.** Rules that generalise live in this skill; anything naming a path, a package manager or an internal symbol belongs in `.claude/routines.md`. A generalisable rule that has drifted into a repo config is a bug in this skill — pull it back.
- **Routines feed the rest of cadence.** A routine's output is a PR, which is `pr-review`'s input, which is `pr-babysit`'s input. Routines are the leftmost stage of the lifecycle, and the only one with no human at the start.
