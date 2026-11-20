---
name: implement
description: >
  Implement one settled task end to end: classify build-up or teardown, build
  and test the slice, simplify, harden, prove the task at its seam, and commit.
  Use when a ready task from spec-and-tasks, a diagnosed bug, or a named
  mechanical change is ready for code. Not for cutting tasks, changing the spec
  or design, an unnamed bug cause, or the final review and handover.
argument-hint: "[task reference | task path]"
---

# implement

One task, end to end. Its behaviour, boundaries, acceptance check, proof, and
seam were settled before this stage. Hold to them, prove the task, commit, and
stop. Do not re-decide the shape behind it.

References: [`build-up.md`](references/build-up.md) and
[`teardown.md`](references/teardown.md) for the two loops;
[`tests.md`](references/tests.md) for test method; [`signals.md`](references/signals.md)
for CRAP, duplication, mutation, and coverage; [`judgment.md`](references/judgment.md)
for drift, causes, structure, and lineage.

## 1. Confirm the work is ready

This stage takes one settled piece of work: a ready task from `spec-and-tasks`
(with an approved spec), a diagnosed bug with a named cause, or a mechanical
change the user has named.

Read the whole input before the first edit. The work needs:

- boundaries: what it includes and what it leaves alone;
- an acceptance check observable from outside the code;
- a proof on the real surface, naming that surface;
- a seam, with what it catches and what it misses.

A `spec-and-tasks` task also has status `ready`, every blocker done, and likely
files as orientation. If it closes a spec, the spec is approved: read it whole,
do not revise it. A mechanical change or a diagnosis may have no spec; then the
task or diagnosis is the contract. If either comes without a seam or proof, name
them before the first edit; if you cannot, stop.

Stop and say what is missing when any of that is absent. A blocked task waits in
the tracker. A published task with a missing field, an ambiguous boundary, or an
open decision goes back to `spec-and-tasks`; a mechanical change or a diagnosis
stops and asks for the missing decision. A task that cannot be built without
choosing a shape goes back to `design`. A bug fix whose cause is not named stops
here: route it to `bug-diagnose`, or stop and ask for the diagnosis; never guess
a cause. If a named stage is not installed, say it is planned and stop.

## 2. Read what binds the task

- Read the code in the task's area and its callers before editing. The source is
  the evidence; names, comments, and likely files are claims.
- Establish the blast radius: callers, public surface, stored data, formats, and
  the tests that will break.
- Read the glossary and any ADR that binds the changed area. Use their names.
- Confirm the task is still valid and is the right one: the behaviour is not
  already true, and no done blocker moved the ground under it.

## 3. Classify: build-up or teardown

- **Build-up**: new behaviour. Make it work, make it right, make it fast.
- **Teardown**: drifted code, right for an intent that has since moved.
  Simplify, harden, clean. Pin the behaviour that must stay, delete one step at
  a time, and prove the same unmodified tests pass.

Failing its current contract is ordinary breakage. Fix it, and call it drift only
when you can point to the intent that moved. Unsure? State what changed: the
requirement, the implementation, or only your understanding.

The loops run opposite: build-up adds structure, teardown deletes first. The beats
below follow the build-up order; a teardown task turns them round and follows
[`teardown.md`](references/teardown.md).

## Beat 1: make it work

**Gate:** the smallest end-to-end path works on real data, and a test at the
task's seam disagrees with the code when the slice is reverted.

- Shape the data before the logic: types, fields, legal states. Make illegal
  states unrepresentable, and parse outside data once, at the boundary.
- Build the smallest slice: the tracer bullet first, then widen it case by case
  and edge by edge.
- Add no cast, ignore, suppression, or widened escape hatch to pass a check.
- Test at the seam the task names, and say what it catches and misses. Red-first
  where the contract is knowable; test-after only against a settled interface.
- Build the lever when a step will be run three times: a fixture, migration,
  rename, or extraction, kept out of product code.

## Beat 2: make it right

**Gate:** every rule and error path in the slice is covered, the cause is fixed,
and the diff is as small as the intent allows.

- Fix the cause. Reproduce, trace backward to the first wrong assumption or
  violated invariant, and check sibling callers. A guard is not a fix.
- Delete before abstracting. Remove paths that earn no keep, establish they are
  unused or superseded, and record a capability dropped on purpose.
- Harden at trust boundaries. Enforce each invariant where the value is created,
  fail loudly, refuse a plausible wrong result, and keep one writer for shared
  state.
- Cover the slice. Every rule, branch, and error path it introduces is in the
  suite. A test that defends replaced behaviour is deleted with the path.
- Clean last. Names, comments, and docs earn their place or go. Leave the code
  you touched better; do not refactor what you did not touch.
- Measure before optimising, and only inside the task.

### Simplify on the settled diff

Run the `wet-or-dry` skill on the diff once the behaviour is settled and the
tests pass. It gives every copy and abstraction a verdict with evidence. Apply
the verdicts inside the task's boundaries and record the rest. That is an
internal step, not the independent review.

### Self-review the diff

Read the diff against the task's contract for the structural defects: preserved
complexity, a flag growing one per caller, an empty indirection, a weakened
boundary, logic in the wrong owner, avoidable duplication, or an abstraction with
no present caller. Cite the evidence, name the smallest move, and separate
contract violations from taste. This is not `code-review`: the independent,
three-lens review belongs to the next stage.

## Beat 3: follow the practice

**Gate:** the task's proof passes at its seam, the log is complete, and every
commit says why, what, and how it was proved.

### Run the proof

Restate the acceptance check in observable terms, then run the proof the task
names, at the surface it names. Use the cheapest direct check at the right
boundary: the endpoint, the CLI output, the stored record, the rendered page, the
metric. Report what was checked and what it showed, and name what remains
unverified. A passing test proves what it checks, not the task. A failing proof
stops the task: fix code inside the boundaries, or return a wrong design to
`design`.

Read the signals then. CRAP, duplication, mutation, and coverage are notes, not
gates: a high CRAP score is a prompt to read the function, surviving mutants in
changed code are worth killing, and coverage never earns a test that asserts
nothing. Detail: [`signals.md`](references/signals.md).

### Commit and update the tracker

Commit small and ordered, each saying why, what changed, and how it was proved. A
declared red intermediate commit is allowed; the task ends green. Do not push, do
not set an author, and do not include unrelated changes.

Only when the project tracker is in use: add the proof and its result to the
current task, and mark it done only after the proof passes. Then set to `ready`
each task whose blockers are now all done and that waits on nothing; that
computes the frontier, it does not reorder. Never create, reorder, or
reprioritise tasks.

## Report and stop

Report the classification and its evidence, what changed, the proof and what it
showed, what remains unverified, findings recorded but not fixed, and the
commits. Name the next frontier task if useful, then stop. Do not start it or
invoke `code-review`, `prove-and-hand-over`, `triage`, `spec-and-tasks`, or
`design`.

## Gate

- [ ] The work was settled: boundaries, check, proof, and seam known; a spec,
      where one exists, approved; any blockers done. The classification is
      stated with evidence.
- [ ] Every behaviour change has a test at the task's seam that fails when
      reverted; no valid test was weakened and expected values are independent.
- [ ] The cause was fixed, not the symptom guarded.
- [ ] The diff stays inside the task's boundaries; unrelated finds are recorded.
- [ ] `wet-or-dry` ran, and its verdicts were applied or recorded.
- [ ] The proof ran at the named surface, and its result is reported.
- [ ] Commits say why, what, and how proved; nothing was pushed.

## Boundaries

`implement` owns one ready task, end to end. It does not own:

- **The design, the spec, or an unnamed bug cause**: a design that fails in code
  returns to `design`, and a bug without a named cause returns to `bug-diagnose`.
- **The order or the scope**: blockers, slicing, and the order of the frontier belong to
  `spec-and-tasks` and the tracker. A task too large is split there, not here.
- **The independent review**: three lenses belong to `code-review`, run by
  `prove-and-hand-over`.
- **The final change proof, operation, and handover**: those belong to
  `prove-and-hand-over`. Beat 3 here is task-level: prove, log, commit, report.
- **The next stage**: it reports and stops.
