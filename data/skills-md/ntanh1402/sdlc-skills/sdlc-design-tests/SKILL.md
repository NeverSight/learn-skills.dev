---
name: sdlc-design-tests
description: Design traceable TestSuites and TestCases for a designed Feature or ChangeRequest in the project wiki, while its requirements are a draft or once they are agreed - unit, integration, e2e, load or security suites, one case per file with risk, numbered concrete data, steps with request and response payloads and explicit validations, and a generated checklist per suite, covering every requirement, contract and failure branch. Use when QA, developers, security or performance roles need test design or test coverage from a design, or when the spec changed after the tests were designed. Does not write runnable test code; not for requirements, architecture or tasks.
---

# Design the tests

This skill is a lifecycle step after the design. It takes a Feature or
ChangeRequest whose design is merged, whether its Requirements are a draft or
agreed, and writes TestSuites in `wiki/<app>/tests/TS-<name>/`, each with one `TC-<name>.md` file
per case. It never writes runnable test code or touches a code repository.

Its draft prefix is `tests-`: the draft for `FEAT-coupons` is
`wiki/tests-FEAT-coupons`. It may run at the same time as `sdlc-plan-tasks` on
the same design.

## Before you start

Read, in this skill's folder, `references/read-protocol.md`,
`references/flow.md` and `references/write-protocol.md`. `flow.md` gives the
steps of the run and the three gates; this file says what is this skill's own
at each step. Then read `references/test-design-rules.md`, `references/case-format.md` and
`references/security-load-checklists.md`, and the schema pages `schema.md`,
`test-suite.md`, `test-case.md`, `feature.md`, `change-request.md`,
`architecture-decision.md` and the page of each Design type in scope, in the
wiki's `.wiki-llm/schema/`.

| Request | Skill |
|---|---|
| No approved design yet | `sdlc-design-arch` |
| Build tasks | `sdlc-plan-tasks` |
| User stories | `sdlc-write-stories`; TestCases link Requirements, never stories |
| Runnable tests, or running them | Not this skill. `sdlc-build-task` writes a Task's unit tests with its code |
| Which tests exist, or what is uncovered | `sdlc-ask-wiki` |

## 1. Look up: readiness and the inventory

Accept one `FEAT-*` or `CR-*` key. Read it on the default branch:

| State | When | Do |
|---|---|---|
| `READY` | A Feature `Draft`, `ReqApproved`, `Approved` or `InDev`, or a ChangeRequest `Proposed`, `ReqApproved` or `Approved`, whose `# Architecture` or `# Delta` is not `None` | Go on |
| `NEEDS_DESIGN` | `# Architecture` or `# Delta` is `None` | Stop: route to `sdlc-design-arch` |
| `NOT_MERGED` | Not on the default branch, but a `wiki/*-<Key>` draft exists | Stop and name the draft |
| `CLOSED` | A Feature that is `Released` or `Deprecated`, or a ChangeRequest that is `Implemented` or `Rejected` | Stop: say it is closed; a change to a Released Feature goes through a ChangeRequest (`sdlc-write-spec`); route nowhere else |

Every state but `READY` is a refusal, not a question.

Then read the Requirements, the Architecture or Delta, the decisions, every
Endpoint, Channel, Subscription, Table and External contract in scope, the
quality targets and risks, the References they link and those about testing
in `references/index.md` (a test plan the user gave is one), and the existing
TestSuites that verify the target (`grep -rl "<Key>" wiki/<app>/tests/`).
Run `$T outdated --feature <Key>` (or `--change <Key>`): a suite it lists was
designed from an older version of the spec. When the design itself is listed
(`designBasedOn` older than `version`), say in the first round that the
design is behind the spec and recommend `sdlc-design-arch` first; go on only
when the person says so. List:

- every Requirement and acceptance outcome;
- every new, changed or removed contract;
- every frontend route or screen with its access rule and its empty, loading,
  error and offline states, when a frontend is in scope;
- happy, alternate, validation and terminal failure branches;
- authentication, authorization, privacy, audit and abuse boundaries;
- retry, timeout, idempotency, ordering, replay, dead letters and fallback;
- data integrity, migration, compatibility, regression and clean-up;
- the performance and security risks the Requirements and decisions state.

## 2. Questions and the Intent gate

Ask in rounds, as `references/flow.md` section 4 says. The first round names
the target and its state, shows the inventory, and asks the person to choose
the suite types. Recommend the types that apply, each with its evidence:

- `unit`: isolated rules, transformations, validations, error mapping;
- `integration`: service, datastore, external and message boundaries;
- `e2e`: actor outcomes across the deployed flow, through the owning frontend
  when there is one;
- `load`: throughput, latency, saturation, recovery and capacity;
- `security`: authentication, authorization, abuse, secrets, injection,
  privacy and audit.

The same round asks about the seams each suite tests at, the exclusions, and
the wiki question; the usual answer to that one is "nothing: only suites and
cases".

- A type the evidence requires (`references/test-design-rules.md`, "Required
  types") may be declined only when the user explicitly accepts the residual
  risk; record that acceptance in the suite's `log.md`.
- A `load` suite with no numeric threshold from a Requirement, decision or
  SLO is blocked until the user gives one. Ask for it; never invent it.
- A contract or Requirement that cannot be tested as written is another
  skill's change: `sdlc-write-spec`.
- When the Requirements are still a draft (`Draft`, `Proposed`), say so: the
  cases may have to change when the spec does.

**Intent gate.** Restate the target, the inventory, the chosen types, the
seams, the exclusions and the residual risk the person accepted. Ask for
approval.

## 3. What goes into the design

For each chosen type, partition inputs and branches with
`references/test-design-rules.md`. "All cases" means complete coverage of the
requirement, contract and risk partitions, not every combination of inputs.

One suite per target and type: `TS-<target words>-<type>`, for example
`TS-coupons-e2e`. If one exists, add to it; if several match, stop and ask.

**A suite designed from an older version.** Compare the spec at the version
in its `basedOn` with the current one (`git log -p` on the `overview.md`).
Revise the cases the change affects, add the cases it needs, and delete the
cases of removed Requirements as the last rule of `test-case.md` says; leave
the other cases as they are. Show each revised case in full at the Design
gate.
Each case is a file `TC-<behaviour words>.md` in the suite folder, written with
`references/case-format.md`.

## 4. Run plan and the Design gate

Start or resume the draft `tests-<Key>` as `references/write-protocol.md`
section 3 says. The input paths are the Feature's or ChangeRequest's
`overview.md` and, for a ChangeRequest, the target Feature's `overview.md`.

Prepare the test design. Build the matrix from every inventory row to its
cases; rows without their own wiki concept (a failure branch, a risk) are
added by hand. The design is:

- each suite with its type, seams and exclusions;
- each case: key, risk, purpose, what it covers;
- the coverage matrix, with every uncovered row and why;
- the totals by Requirement, Design concept, risk and suite type;
- assumptions and residual risks.

Write the Run plan. Its `## Files` are each new suite's `overview.md`, one
line per case file with what it covers, and the `log.md` of each suite.
When the user gave a test plan that the wiki does not hold yet, add its
Reference folder `references/REF-<name>-test-plan/` (`overview.md`, `log.md`
and the plan as a content file); the Design gate is the person's approval of
it.

**Design gate.** Show the design in full, never only a summary, then the Run
plan. Ask for approval. Approval with an uncovered in-scope row is allowed
only when the user explicitly accepts that gap as residual risk.

## 5. Write

In the draft worktree, under `wiki/<app>/tests/`:

- a new suite folder `TS-<name>/` with `overview.md` (`type: TestSuite`,
  `status: Approved`, `suiteType`, `basedOn`, `# Verifies` linking the
  Feature or ChangeRequest) and `log.md`;
- `basedOn` with one entry per target under `# Verifies`:
  `{ id: <key>, version: <its version>, at: <its versionDate> }`. On an
  existing suite, update the entry of the target you designed for;
- one `TC-<name>.md` per new case;
- `# References` on a suite that links the test plan it was written from,
  and any other Reference a tester needs, with a note on what to take from
  it;
- an entry in each changed suite's `log.md`, for example
  `* **Test design**: Added 9 cases for FEAT-coupons. Written by an AI model with sdlc-design-tests.`

Every step and validation must make sense to a tester who did not design the
system. Do not write `index.md` or `checklist.csv`: `draft finish` writes
both.

## 6. Self review, finish and commit

Follow `references/write-protocol.md` section 4 from step 5. In the self
review, also check that:

- `$T coverage tests --feature <FEAT>` (or `--change <CR>`), run in the
  worktree, reports nothing uncovered except the gaps the user accepted;
- every case has its risk, concrete data, complete steps, a validation for
  each step that needs one, clean-up and links;
- no suite or case is written twice, no existing case was changed except
  those a newer spec version affects, and no runnable code was written;
- each step that calls an API or publishes to a channel has its request and
  expected response, and `# Test data` is numbered from 1;
- each suite's `basedOn` names the current version of each target it was
  designed for;
- each accepted risk or gap is recorded in its suite's `log.md`.

Commit message: `tests(<Key>): design <n> cases`. In the summary, "Not done"
names each gap the user accepted, and "Next" says the suites can be turned
into runnable tests once the pull request is merged, and that each suite's
`checklist.csv` lists its cases.

## Done when

- The user chose the suite types, and any declined required type has an
  accepted residual risk.
- Every in-scope Requirement, contract, branch and risk is covered, or the gap
  was accepted.
- Every case has concrete data, complete steps, validations, clean-up and
  links; no suite or case is duplicated; no runnable code was written.
- The self review found nothing it could not fix, or the person accepted what
  was left at the Change-set gate.
- `draft finish` was `ok`, the change set was approved, and `draft commit`
  reported the branch.
