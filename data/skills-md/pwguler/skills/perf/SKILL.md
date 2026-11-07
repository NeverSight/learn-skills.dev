---
name: perf
description: Make code faster or find why it is slow, from measurements and not from guesses. Read this skill before you change code to make it faster or use less memory. Use it when the user reports slow code, high latency, or high memory use. Use it also to check a speed claim, or to compare the speed of two options. Use it to diagnose a slow or stuck process, a profile, or a trace file.
---

Measure before you change code for speed. A claim about speed without a measurement is only a guess. A change that rests on a guess can make the code slower.

Fast path: when the user only asks whether a measured number holds, change no code. Read the `verify` skill, and check the number with [measurement.md](references/measurement.md). When the user asks only why code is slow, or gives a profile or trace file, also change no code. Go to step 4, and report as its reference says.

1. Before you measure anything, create a task list with these steps as its items. If a task list already exists, add the steps to it. When you skip a step, mark it done and add `skip: <reason>` to its text. To go back to an earlier step, add that step and each step after it again as new items.
2. State the target in one sentence: the operation, the input, and the number that counts as success. Take the target from the user or the spec. When nobody gave one, the target is a gain larger than the spread on a realistic input. Say so.
3. Build a measurement that you can run again: a script or a command, and a realistic input. Run each side five times or more. Check the measurement with [measurement.md](references/measurement.md) before you trust it. Step 4 answers its first check. Record the baseline: the number, its unit, the run count, and the spread.
4. Find the limiter, the one resource that stops the number from getting better, by observation. Do not guess it from the source. Use a profiler, a trace, or counters. A profiler slows the work, so never report a number from a profiled run. For a running process, follow [live-process.md](references/live-process.md). For a profile, trace, dump, or log file that already exists, follow [capture-file.md](references/capture-file.md).
5. Change one thing at the limiter, and try the cheapest kind of change first. First remove work whose result nothing uses. Then do the work once, and keep the result. Then do less work. Then do the work later. Then do it at a time when nobody waits. Then run it in parallel. Make the work itself cheaper only as the last option. A change that keeps results, delays work, or runs work in parallel can change behavior. Give it a failing test first, as implement says.
6. Measure again with the same setup, and run the old and new versions in alternating order. Run the tests that exercise the changed path. Keep the change only when they pass and the gain is larger than the spread. Otherwise revert it. When a kept change meets the target, go to step 7. Otherwise go back to step 4.
7. Before you report the gain, read the `verify` skill, and follow it for the tests, the build, and the linter. The measurement script is a demo of the gain, as verify defines a demo. Report the gain as a measured number, not as a verified criterion.
8. Report the result: the number before and after, each with its unit, run count, spread, and limiter. Name the change and the input that you measured.

Rules:

- Change no code for speed before the baseline exists.
- Make one change between two measurements, so that each gain has one cause.
- A request for a diagnosis gets a diagnosis, not a fix. Cite the evidence for each finding.
- A deadlock, a crash, or a wrong result is a defect, not slowness. Its fix goes to `debug`.
- Do not tune code that the measurement does not show as the limiter.
- Stop after three changes in a row that give no gain larger than the spread. Report the measurements and the limiter, and let the user decide.
- When the work continues after the session, keep the measurement script in the diff, as implement's build-the-lever principle says.
- Never invent a number. Report a measurement that failed as failed.
- A raw payload that you must read, and that is longer than about 2,000 lines, goes to a subagent. Keep only the reduced finding in the session, as research's guard-the-context-window principle says.
