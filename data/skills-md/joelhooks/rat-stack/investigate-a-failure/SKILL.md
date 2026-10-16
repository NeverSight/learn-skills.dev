---
name: investigate-a-failure
description: Find the cause of a crash, wrong output, flaky test, or slow run with evidence, fix it at its source, and leave a notebook a person can learn from. Use when something fails intermittently, when the first fix idea is "raise the timeout" or "swap the version", or when asked "why does this break" or "make this stable".
plain: "Make the failure happen on demand, test one idea at a time, fix the cause, and write down what each step proved."
diagram: |-
  bound the symptom
    │
  repro on demand
    │
  rebuild what runs
    │
  one hypothesis at a time
    ├ proved → next layer
    └ falsified → note it
    │
  fix at the cause
    ▼ notebook + recipe
---

# Investigate a failure

Find why something fails before you change it. A fix chosen before the cause is known can hide the failure without removing it. Swapping a version, image, or provider until the symptom stops teaches nothing. The next failure stays as mysterious as this one.

Read `AGENTS.md` first. Then read these leaves:

- `skills/rat-stack-mode/principles/find-the-cause-first.md`
- `skills/rat-stack-mode/principles/rebuild-what-you-run.md`
- `skills/rat-stack-mode/principles/measure-real-limits.md`
- `skills/rat-stack-mode/principles/keep-execution-receipts.md`

## Terms used here

- **Repro:** a script that makes the failure happen on demand, at a known rate.
- **Hypothesis:** one testable claim about the cause. It stays a hypothesis until an experiment proves it.
- **Probe:** temporary instrumentation that checks a hypothesis. It stops the run cleanly, with the values it saw, before the failure happens.
- **Asynchronous error:** an error reported after the work that caused it. Its stack trace names where it surfaced, which may be far from where it started.
- **Notebook:** the running record of the investigation, written as it happens.

## 1. Bound the symptom

Write down what fails, how often, and under which conditions. Keep receipts: logs, error codes, timestamps, and inputs. Separate the failure from events near it. Output that looks corrupted may be a side effect of a crash.

## 2. Make it happen on demand

Write the smallest repro that triggers the failure. Report its rate as counts, for example "17 in 1,000 runs". A rare failure needs enough runs per attempt to show up. Then make it deterministic where you can, so the same input fails every time. The repro proves the fix later.

## 3. Rebuild what runs

Investigate code you can read and rebuild. If the running artifact holds changes that exist nowhere else, extract them as readable patches and pin every commit. Confirm the rebuild reproduces the failure before you trust an experiment on it.

## 4. Test one hypothesis at a time

Record each hypothesis, then run one experiment that can prove or falsify it.

- Make asynchronous errors synchronous before you trust a stack trace.
- Prefer probes that check the suspected values and stop cleanly over runs that wait for the crash.
- Change one setting per experiment. Repeat each experiment enough times to see the rate change.

A falsified hypothesis is a result. Write it down with its evidence and move to the next layer.

## 5. Fix at the cause

Fix the cause where it lives, not where it surfaced. A setting that avoids the failure, such as a longer timeout or a disabled feature, is a workaround. Measure its cost and label it as one.

Prove the fix with the repro. Then repeat the original workload enough times to show the rate is zero.

Example: two web tests read the same build output while the build rewrote it. Two repro runs found 17 and 28 torn reads. The fix wrote each file to a temporary path and renamed it into place. After the fix, 8.5 million reads showed no torn read. The fix lives in `apps/web/scripts/reader-build.ts`.

## 6. Leave a notebook and a recipe

Write the notebook as you go, not at the end. Each entry records:

- the hypothesis;
- the exact command;
- what happened;
- what it rules in or out.

End the notebook with:

- the cause and its proof;
- each setting touched, what it trades, and what was measured;
- the rebuild recipe with pinned sources, so someone else can reproduce the failure and the fix.

If the cause is upstream, send the maintainer the repro and the proof. Sending it is an outward action and follows the project's approval rules.

## Report

Report these items:

- the cause and the experiment that proved it;
- the falsified hypotheses;
- the fix and its proof, as a rate before and after;
- any workaround and its cost;
- the notebook path.
