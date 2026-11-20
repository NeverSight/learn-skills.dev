---
name: triage
description: >
  Classify an arriving work item and name its next stage, then give one verdict
  and one next action. Use at the start of a change, when new work arrives, when
  a spec task looks like the next one, or when it is unclear whether something
  should be done now. Covers requests, tracker issues, spec tasks, review
  findings, retro lessons, bug reports, metric targets, and PR comments. Not for
  doing the work: no diagnosis, design, tasks, code, review, or estimates.
argument-hint: "[work item | ticket | task reference]"
---

# triage

Work arrives from everywhere. Triage is the gate every item passes before a
stage takes it: should this be done now, and by which stage? It does not answer
how, and it is read-only by default: no code, no spec, no tasks, no tracker
edits, no next-stage invocation.

Triage is recurring, not a first step. It runs at the start of a change and
again whenever a new item appears: a review finding, a closed task, a comment, a
bug report. It reports and stops.

References: [`routing.md`](references/routing.md) for the source and kind tables,
each path, skipped stages, entry requirements, and examples;
[`verdicts.md`](references/verdicts.md) for validation, blockers, the frontier,
the no-rank rule, and the anti-patterns.

## 1. Name the item and its source

State the item in one line and where it came from: user request, tracker issue,
spec task, review finding, retro lesson, bug report, metric target, or PR
comment. The source decides which checks apply. No item, no triage: if the
message names nothing to act on, say so and stop.

## 2. Read enough to classify, not to solve

Read the item, the tracker, the named code, and the record only as far as the
verdict needs: enough to check validity and find a duplicate, to see whether a
blocker or a wait stands in front, and to size the blast radius. Do not
reproduce the bug, diagnose the cause, sketch a fix, or review the diff. That is
the next stage's job, and doing it here makes triage a second discovery pass.

## 3. Classify the kind

Name one: question, mechanical change, bug, feature, refactor, metric campaign,
or structural work, and name the source beside it. If the kind is unclear, the
verdict is `needs framing/info`: name the one question that would settle it and
its owner. Do not ask three.

## 4. Validate

Is the item still valid, already done, or a duplicate? Search the tracker by
title, symptom, and the key nouns, and check the spec, task, PR/MR, commit, or
release where the item points. For a duplicate, name the canonical item and
recommend closing this one. For already done, name the commit, release, or
behaviour that shows it.

Recommend, do not act: no close, merge, label, or comment unless the user asks.

## 5. Check actionability

Is anything in the way? Name it and its owner: a decision the user has not made,
a fact nobody has gathered, another task whose output this needs (a blocker), or
an external wait: a credential, a deployment, a release.

A spec task is actionable only when its status is `ready` and every blocker is
done. A blocked task is deferred, never picked. A wait that is not a blocker
still keeps the task blocked.

## 6. Size and blast radius

Name a size class, never an estimate: one function, one module, cross-module,
repo-wide, or unknown. "Unknown" is honest when the read was too thin to say,
and it makes the first stage a read.

Blast radius is evidence: callers, public surface, stored data, formats, and the
tests that will break. "Small" is not a blast radius. Never give hours, days,
points, or effort.

## 7. Pick the path

The kind decides the stages, except a spec task, which enters at `implement`
whatever its kind. The source decides the checks and supplies the evidence.

| Kind | Path | Skipped |
|---|---|---|
| Question | answer, or `show-me` | design, tasks, code |
| Mechanical change | `implement` → `prove-and-hand-over` | design, tasks |
| Bug | `bug-diagnose` → `implement` → `prove-and-hand-over` | design, tasks |
| Feature or refactor | `design` → `spec-and-tasks` → `implement` → `prove-and-hand-over` | none |
| Metric campaign | `hillclimb` → `prove-and-hand-over` | design, tasks |
| Structural work | `architecture` → `design` → ... → `prove-and-hand-over` | none |

A question is routed to an answer; triage does not answer it. `prove-and-hand-over`
runs `code-review` as part of the finish, so the review is not a separate stop in
the path.

Then apply the source: a review finding is fixed now, diagnosed, deferred, or
rejected with the risk recorded; a retro lesson goes to `retro` with its proposed
home; a PR comment is a change request, a question, or noise. The goal modifiers
(`find-the-core`, `north-star`, `prototype`, `why`) and the full source checks
are in [`routing.md`](references/routing.md). Naming the path ends this stage; do
not start it. If a named stage is not installed, mark it `(planned)` in the
path; the verdict stands, and the path ends before that stage.

## 8. Choose the verdict

One verdict, from five:

- **do now**: valid, unblocked, ready. One next action named. It does not mean
  started.
- **defer**: valid, but blocked, waiting, or not now. Name the trigger that
  would make it ready and its owner.
- **reject**: invalid, out of scope, already done, or not worth doing. Name the
  evidence, not a preference.
- **duplicate**: a canonical item exists. Link it and recommend close.
- **needs framing/info**: a missing goal, decision, or fact. Name one question
  and its owner, not a questionnaire.

What each verdict needs, and the ways triage goes wrong:
[`verdicts.md`](references/verdicts.md).

## 9. Frontier, for a spec task

The **frontier** is the tasks whose blockers are all done and whose status is
`ready`. Compute it from the tracker, not from memory. An item off the frontier
is deferred; name the open blocker. If several tasks are ready, use the
tracker's order; with no order, use the priority the user named; with neither,
report the frontier and ask. Never invent a ranking across unrelated work:
priority stays with the user or the tracker.

## 10. Report and stop

```
DO NOW → <next action>
  | DEFER until <trigger> (owner: <owner>)
  | REJECT: <evidence>
  | DUPLICATE of <canonical item>
  | NEEDS FRAMING/INFO: <one question> (owner: <owner>)
<the item, in one line>
<question | mechanical | bug | feature | refactor | metric | structural> · <size class> · <source>

Path      <stage> → <stage> → ...

Valid     <evidence: valid, done, duplicate of X, superseded by Y>
Blocked   <blocker or wait; owner>
Blast     <callers, public surface, data, formats, tests>
```

The decision comes first and names what its verdict must name. Evidence lists
only the fields that support the verdict, and never a field whose value is none.
Name a next stage as a skill, "run the `design` skill", not as a slash command:
harnesses invoke skills differently.

Then stop: no skill invoked, no task created or edited, no code, no tracker
edit. The user or `glen-mode` starts the next stage.

## Gate

- [ ] The item and its source are named; the kind is named, or
      `needs framing/info` carries one question and its owner.
- [ ] Validity is checked, and a duplicate names its canonical item.
- [ ] Every blocker or wait is named with an owner; a blocked task is deferred.
- [ ] A size class and an evidence-based blast radius are given, with no
      estimate.
- [ ] The path names its stages.
- [ ] One verdict leads the report, with what that verdict must name.
- [ ] Nothing was started, written, or invoked.

## Boundaries

`triage` owns intake and routing for any work item. It does not own:

- **The work**: no answer, design, diagnosis, code, review, or proof. A question
  is routed, not answered here.
- **The frame, shape, or tasks**: `find-the-core`, `north-star`, `design`, and
  `spec-and-tasks` own them; triage names what is missing.
- **Priority and the backlog**: the user and the tracker hold them. Triage
  reports the frontier and does not rank it.
- **The tracker and the next stage**: no close, merge, label, or comment unless
  the user asks, and no skill invoked. It reports and stops.

## No re-interview

Use the item, the tracker, the code, and the record. Ask at most the one
question that changes the verdict. If more than one thing is missing, name the
first missing item and its owner, and give `needs framing/info`. Do not run a
requirements interview: that belongs to `north-star`, `find-the-core`, or
`design`.

A ticket with enough context is classified without a new interview. If it lacks
what a stage needs on entry, name the gap and the owner; do not fill it in.
