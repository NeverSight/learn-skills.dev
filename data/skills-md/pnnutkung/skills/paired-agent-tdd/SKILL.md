---
name: paired-agent-tdd
description: Use for a non-trivial, multi-file feature or bugfix that must be built test-first, with independent verification and a written definition of done (DoD) that the tests demonstrably cover; not for a single-file or one-line change.
---

# Paired Agent TDD

TDD (RED, GREEN) as **driver/navigator pairs**, one pipeline per file group, run by a Workflow script ([`workflow.js`](./workflow.js)) from an execution graph ([`graph.mjs`](./graph.mjs)). Plain-code **gates** ([`tdd.mjs`](./tdd.mjs), [`probes.md`](./probes.md)) produce the facts: tests run, new code is mutated, scope is diffed, the DoD is closed against real runs. Agents judge those facts and never grade their own work. The lead coordinates and never edits code. **A stage is a loop, never one shot:** the maker edits, runs the real gate and edits again; an independent navigator re-runs it; defects go back until the check passes, stops making progress or the rounds run out.

**Requires:** Node 18+, git, the Workflow tool, the sibling skill `zero-trust-review` (sandbox runner, mutation probe, `proofcheck.mjs`; `ZT_DIR` if it lives elsewhere), and nothing else: the gates run the test command **directly** (your rights, your network); `plan.sandbox: true` confines it in the zero-trust-review sandbox (macOS `sandbox-exec`, Linux `bwrap`, docker). Agent types `tdd-guide` and `code-reviewer` (the judges have no Edit or Write).

Cost levers ([`runs.md`](./runs.md)): no barrier between groups, gates are code, one whole-diff reviewer, one fixer per group, narrow agent types.

## Progress checklist

```
- [ ] 0 Gate: skill needed? DoD written with source quotes; groups partitioned, one owner per file
- [ ] 1 tdd.mjs plan ok; agent count shown (confirm if > 25)
- [ ] 2 Workflow run; compact return read, saved as return.json
- [ ] 3 tdd.mjs verify: DoD closure, unfixed, overridden, notDone, proofcheck
- [ ] 3b Rename test_ac* to the naming rule; guard passes
- [ ] 4 Full suite and lint on changed files, once; record the run; report
```

## When to use

- A multi-file change with tests expected, whose files split into groups that can be owned independently (**one owner per file**: teammates share one working tree).
- Not for single-file or one-line changes (use `tdd` or a lone subagent), exploration, or work with no tests. One group with no fan-out still gets independent verification.

## Step 0 — Write plan.json (the lead, no agent)

| Field | Rule |
|---|---|
| `dod[]` | One observable behavior each: `{id, text, source, kinds?}`. `id` is alphanumeric (`AC1`: it goes into test names). `source` = a **verbatim quote** from the ticket or request, else `"assumed"`; list the assumed items for the user before spending. `kinds` defaults to `happy, fail, edge`; narrow it only with a reason you state in the report. |
| `groups[]` | `{id, goal, tests[], src[], dod[], after[], mirror?}`: files each group owns, the DoD ids it covers (every id in some group), `after` only when its code imports another group's new code (its GREEN waits; its RED does not), `mirror` = a sibling file whose pattern to copy. |
| `cmd` | The project's one-test-file command with `{file}`, e.g. `pytest -q {file}`. Agents and gates both run it. `link` (venv dir), `env`, and with the sandbox `ro` (interpreter install), as in [`probes.md`](./probes.md). |
| options | `ticket` (path: DoD quotes are checked against it), `cover` + `coverMin` (an lcov-writing command, default minimum 80% of changed lines), `integration {file, goal}` only when the change crosses a process, DB or network boundary, `mutation {max, budget, off}`, `rounds` (repair rounds per stage, 1-4, default 3), `maxRepairs` (repairs for the first run, default 2 per group), `smoke` (1-3 tests that pass at the base, to prove the runner), `sandbox` (true = confined gates). `src` may hold config files; never a test-like path. |

Partition by file ownership, never by chore. Run the `graph-planner` (opus, one agent) only when files import one another and the groups are unclear. If a driver would need a file another group owns, the groups are wrong: merge them.

## Step 1 — Plan

```bash
SK=${SK:-$HOME/.claude/skills/paired-agent-tdd}
node $SK/tdd.mjs plan --plan plan.json > args.json    # validates, snapshots the base tree, creates the run folder RUN, prints the Workflow args
node $SK/graph.mjs --plan <groups> <integration 0|1> <groups expected to get findings>
```

`plan` refuses an invalid plan with every error at once (unknown DoD id, a file with two owners, a cycle, a quote not in the ticket) and a runner that cannot run the repo's tests (**preflight**, [`probes.md`](./probes.md): a wrong `cmd`, a missing venv or no sandbox stops here, never as a fake RED; `--skip-preflight` goes on unproven). The base is HEAD, or a snapshot of the dirty working tree; your repo's index, refs and files are never touched. Show the user the groups, the DoD (assumed items marked), the agent count and the ceiling `--plan` prints. **If the total exceeds 25, confirm before spending.**

## Step 2 — Run

```
Workflow({ scriptPath: "$SK/workflow.js", args: <the JSON in args.json> })
```

`mode: "plan"` is a dry run (counts, ceiling, prompt sizes). Read the **compact return** only: `{groups{state, reason, red, green, matrix, files}, clusters, fixes, verified, notDone, stats, boardMd, postmortemMd}`. Save it as `return.json`; write `boardMd` and `postmortemMd` into `$RUN`.

**Continue after a failure** (a group `failed`, `blocked` or `paused`, or the run died): `node $SK/tdd.mjs resume --run $RUN [--ret return.json] [--max-repairs N]` reads the gate files (no agent, no tokens), prints the next run's budget and agent ceiling, and writes `$RUN/continue.json`. Run the Workflow again with `args: {...args, resume: <that file>}`: the file sets the budget (default 2 per group still working), done groups cost nothing, the others restart where they stopped with the defects the gates and navigators found. A group on `env` (a gate said `unverifiable`: fix the runner, re-run that gate) or `hold` (the same defects stalled; options in [`probes.md`](./probes.md) "resume") spends nothing until you decide.

## Step 3 — Verify, then report

```bash
node $SK/tdd.mjs verify --run $RUN --ret return.json
```

It prints `{dod{covered,total,gaps}, final, overridden, unfixed, notDone, proofcheck}` and writes `$RUN/dod-matrix.md`. **Not done while** any DoD gap, `final: false`, an `overridden` entry (a navigator said PASS against its own gate), an `unfixed` finding or a `notDone` group (a failed integration test included) remains; say so with the numbers. Then rename tests to the repo's naming rule, if any (probes.md, "Naming rule"), run the project's full suite once (background) and lint on the changed files only. Report: DoD matrix, blocked groups with their reason, findings by proof status, assumed DoD items.

**Record every real run** (one line, no baseline): `node $SK/record.mjs --run $RUN --ret return.json --transcript <the transcript dir the Workflow result prints> --note "<job>" --append $SK/runs.md`. Run `verify` first; cost and time come from the transcript.

## The graph

<!-- GENERATED:graph -->

```mermaid
graph TD
  graph-planner["graph-planner<br/>opus/high · gated"]
  plan["plan<br/>code"]
  red-driver["red-driver<br/>sonnet/medium · per group"]
  red-gate["red-gate<br/>code · per group"]
  red-navigator["red-navigator<br/>sonnet/high · per group"]
  green-driver["green-driver<br/>sonnet/medium · per group"]
  green-gate["green-gate<br/>code · per group"]
  green-navigator["green-navigator<br/>sonnet/high · per group"]
  integration-tester["integration-tester<br/>sonnet/high · gated"]
  final-gate["final-gate<br/>code"]
  reviewer["reviewer<br/>opus/high"]
  fixer["fixer<br/>sonnet/medium · per group · gated"]
  final-verifier["final-verifier<br/>haiku/low · gated"]
  verify["verify<br/>code"]
  graph-planner --> plan
  plan --> red-driver
  red-driver --> red-gate
  red-gate --> red-navigator
  red-navigator --> green-driver
  green-driver --> green-gate
  green-gate --> green-navigator
  green-navigator --> integration-tester
  green-navigator --> final-gate
  integration-tester --> final-gate
  final-gate --> reviewer
  reviewer --> fixer
  fixer --> final-verifier
  final-verifier --> verify
```

<!-- /GENERATED:graph -->

`node graph.mjs --check` fails on drift (`--write` regenerates the generated blocks here and in `workflow.js`). Protect: every group starts RED at once; `after` delays only GREEN; the reviewer reads the whole diff **once**.

## What the gates check (T0, [`probes.md`](./probes.md))

| Gate | Run by | Facts |
|---|---|---|
| `red` | red-driver (its loop), red-navigator | each new test file **fails now**, and how: assertion, load error, passes already, missing |
| `green` | green-driver (its loop), green-navigator | tests pass and **fail once the group's code is reverted**, no flake, **tests unchanged since RED**, **mutants of the new lines** (a survivor is a test gap), coverage |
| `dod` | makers and navigators | the group's DoD pairs: each test **named in its file**, its file failed at RED and passes at GREEN, the gate file **not stale**; instant, runs nothing |
| `final` | reviewer, final courier | all group tests together, existing tests that mention the changed modules, stray files, the whole-diff patch; `--again` = the re-run after fixes |
| `verify` | lead | DoD closure from the gate files, fixes still present, reviewer proofs re-checked |

A group is judged on the base plus **only its own files**: another group's half-written edit never fails it.

## Rules

- **Lead-only.** The lead plans, launches, reads, verifies. It never writes test or code (a one-line fix it fully understands is the only exception) and never re-verifies what a gate already proved. Repairs are scheduled by the script, not by teammates.
- **A verifier is always a separate node.** A navigator did not write the work, runs the gate first and judges the output; a claim it did not see in a gate or a file it read is not a fact. The judges cannot edit.
- **DoD closure.** Every DoD id needs a test per required kind, its name carrying the id set apart (`test_ac1_happy`), one test per (id, kind). The script checks the matrix in code before a navigator is paid for; `verify` re-derives coverage from gate files: a pair counts only if its test file failed at RED and passes at GREEN.
- **Repair loop (R4).** No stage is one shot. The maker edits, runs the real gate and `dod`, edits again (3 gate runs at most) and lists what `remaining` when it stops on a failing gate: the next pass starts there. Only a navigator on fresh gate facts ends a stage. Defects go back until PASS, the same defects return (`blocked`, and so is everything that waits) or `rounds` repairs. One run-wide budget pays every repair (a fair share kept per group): spent, the group is `paused` and nothing is reviewed until `resume` finishes it. `unverifiable` is the environment: the group stops with no repair spent. A surviving mutant is a test gap (a strengthening pass, never weakened, then `--retest`); a changed frozen test is restored. After the fixers a courier re-runs `final`; what it names goes back to its owner (two fix passes at most). A defect is fixed or listed under `notDone`.
- **Frozen tests.** GREEN never edits a test; a wrong test is reported (`testDefects`), not patched.
- **Hard scope fence.** Every driver and fixer prompt names the only files it may edit and what to report instead; `final` lists any other changed file.
- **Precedent and research first** (every driver prompt): grep sibling tests for the same flag before asserting a fail or edge behavior; look for an existing helper, then the library docs, before new code.
- **Tool discipline.** Read/Edit/Write/Grep/Glob for files; Bash only for the test command, the gate commands, read-only git and linters; never `sed` or a heredoc to edit.
- **Ponytail** per node (column above): never compress validation at trust boundaries, data-loss handling, security or accessibility.

## Tiering

Aligned to the global subagent routing: T0 code for anything deterministic, T2 sonnet for analysis and implementation, T3 opus only for once-per-run judges (planner, reviewer). Rules R1-R6 and the measured agent-type costs: [`tiering.md`](./tiering.md).

<!-- GENERATED:tiers -->

| node | tier | model | effort | agent type | ponytail | calls | gate/fanout |
|---|---|---|---|---|---|---|---|
| graph-planner | T3 | opus | high | planner | full | - | only when the import structure is unknown |
| red-driver | T2 | sonnet | medium | tdd-guide | ultra | 40 | per group |
| red-navigator | T2 | sonnet | high | code-reviewer | full | 25 | per group |
| green-driver | T2 | sonnet | medium | tdd-guide | ultra | 45 | per group |
| green-navigator | T2 | sonnet | high | code-reviewer | full | 25 | per group |
| integration-tester | T2 | sonnet | high | tdd-guide | lite | 35 | only when the change crosses a process, DB or network boundary |
| reviewer | T3 | opus | high | code-reviewer | off | 40 | - |
| fixer | T2 | sonnet | medium | tdd-guide | full | 35 | per group, only for groups with findings |
| final-verifier | T1 | haiku | low | code-reviewer | off | 6 | only after fixers ran |

<!-- /GENERATED:tiers -->

`graph.mjs --check` also guards tiers, opus placement, navigator >= driver and read-only judges.

## Iterate from measurements

`record.mjs` logs each real run in [`runs.md`](./runs.md); change a node's model, effort or agent type only from those numbers, and shorten the critical path (the wall-clock floor of one group) by removing an edge. Evals: [`evals.json`](./evals.json).

## Links out

`tdd` (RED/GREEN/REFACTOR mechanics), `zero-trust-review` (its probes run here; review the finished diff with it in a fresh session), `ai-code-delivery`, `e2e-runner` (a frontend integration test), `wayfinder` / `grill-with-docs`, `prototype` (unclear RED shape).
