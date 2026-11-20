---
name: prove-and-hand-over
description: >
  Finish a change whose tasks are done: prove each acceptance criterion on the
  real surface, run one wet-or-dry pass across the whole change, run
  code-review, route the findings, and write the handover and the PR/MR body.
  Use when the last task is committed, or when a mechanical change or bug fix
  is implemented and needs its final proof, review, and report. Not for
  implementing fixes, writing the spec, pushing, or opening the PR/MR.
argument-hint: "[fixed point] [spec path]"
---

# prove-and-hand-over

A change is not finished when its last task is committed. It is finished when
every acceptance criterion is proven on the real surface, the whole change is
reviewed, every gap is named, and someone who did not watch it being made can
review it. This stage proves, reviews, routes, and reports. It does not write
code.

References: [`handover.md`](references/handover.md) for the handover template
and rules; [`pr-body.md`](references/pr-body.md) for the PR/MR body.

## 1. Confirm the input

This stage takes one finished change:

- every task of the change done, or a mechanical change or a bug fix with its
  bug diagnosis that `implement` finished;
- the fixed point: the commit before the change;
- the approved spec, if the change has one.

Read the spec whole, the task reports, and `git log <fixed point>..HEAD`. A
change without a spec takes its acceptance criteria from the task, the
mechanical change, or the bug diagnosis.

Stop and say what is missing when any of that is absent: an open task, an
unknown fixed point, a spec still at draft, or a change with no acceptance
criterion to prove. An open task goes back to `implement`; a missing or draft
spec goes back to `design`.

## 2. Prove each acceptance criterion

Prove the change, not the tasks. For each acceptance criterion:

- restate it in observable terms;
- run the direct check on the real surface the criterion names: the endpoint,
  the CLI output, the stored record, the rendered page, the metric;
- report what the check showed, and name what remains unverified and why.

A passing test proves what it checks, not the criterion. Task-level proofs are
evidence, not a substitute: a criterion closed by three tasks is proven once,
across all three. A check that fails is a finding for step 5, not something to
fix here.

## 3. Run `wet-or-dry` across the change

Run the `wet-or-dry` skill once on `<fixed point>..HEAD`. Per-task runs cannot
see copies spread across tasks. Report its verdicts and its balance; do not
apply them here. An **extract**, **reuse**, **inline**, or **delete** verdict
is a finding for step 5.

## 4. Run `code-review`

Run the `code-review` skill against the fixed point, with the spec. Keep its
lenses and severities as it reports them. The review is evidence, not a
substitute for the proof or the handover.

## 5. Route the findings

This stage does not implement. Route each finding from steps 2–4:

- **P0/P1**, or a failed proof: back to `implement` as a fix, with the finding
  as its acceptance check.
- **A fix that needs a decision**: a judgment call goes to the user; a change
  of shape goes to `design`. Do not settle it here.
- **P2/P3**: to the handover as found-not-fixed, unless the user picks some to
  fix. Those also go to `implement`.

Report the routing and stop until the fixes land. Then re-run the proof
(step 2) for every criterion the fixes touch, and run `code-review` again on
the fix commits only. A P0/P1 the user accepts unfixed is declared in the
handover, with the user's acceptance.

If two fixes fail the same check, stop routing fixes: write the Premise
section of the handover instead.

## 6. Write the handover

Write the handover with [`handover.md`](references/handover.md): proven per
criterion, seams, tested, not tested and why, departures, blast radius
re-checked, review, `wet-or-dry`, commits, and found-not-fixed. A blocked change
writes the Blocked section instead of pretending to finish.

## 7. Write the PR/MR body

Write the PR/MR body with [`pr-body.md`](references/pr-body.md): why, what
changed, how it was proved, what is not proved, a change outline made with the
`show-me` skill, and found-not-fixed. Follow the project's PR/MR template where
one exists.

Write it as text in the report, or to a file if the user asks. Never push,
never open the PR/MR, and never comment on the tracker: those stay with the
user.

## 8. Report and stop

Report the handover, then the PR/MR body. Then stop. The next stage is `retro`;
if it is not installed, say it is planned and stop. Do not invoke any other
skill after the report.

## Gate

- [ ] Every acceptance criterion is proven by a direct check on its real
      surface, or named unverified with the reason.
- [ ] `wet-or-dry` ran once across the whole change, and its verdicts are
      reported.
- [ ] `code-review` ran against the fixed point, with the spec.
- [ ] Every P0/P1 finding is fixed through `implement` and re-proven, or
      declared with the user's acceptance.
- [ ] Every P2/P3 finding is listed as found-not-fixed, or was fixed at the
      user's request.
- [ ] The handover is written.
- [ ] The PR/MR body is written.
- [ ] The working tree is clean: nothing uncommitted or untracked is left
      behind, or what is left is named in the handover.
- [ ] Nothing was pushed, opened, or posted to the tracker.

## Boundaries

`prove-and-hand-over` owns the end of one change. It does not own:

- **Code or fixes**: every fix goes to `implement`, including `wet-or-dry`
  verdicts.
- **The spec or the shape**: a criterion that cannot be proven as written, or a
  fix that changes the shape, goes to `design`.
- **The priority of findings**: the user decides which P2/P3 to fix and which
  P0/P1 to accept unfixed.
- **The push, the PR/MR, and the tracker**: the user opens, pushes, and
  comments.
- **The retrospective**: that is `retro`. This stage reports and stops.
