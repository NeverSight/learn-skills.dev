---
name: bug-hunter
description: >
  MUST USE when debugging, fixing a bug, 排查/调试/修 bug/为什么报错/不工作,
  or when tests fail unexpectedly. Systematic root-cause workflow:
  reproduce → isolate → hypothesis → minimal fix → regression test.
  Forbids shotgun fixes and "fix around the symptom".
  Part of claude-skills-pro - 8 more skills (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) + 11-chapter CN handbook, all free: github.com/Hahaknight/claude-skills-pro
---

# Bug Hunter — Root Cause Debugging

## Prime directive

Find the CAUSE, not a patch that silences the symptom. A bug is a discrepancy between what the code does and what someone believes it does. Your first job is to locate the exact line where belief and reality diverge.

## Workflow

1. **Define the bug precisely.** Reproduce it. Write the exact steps/input, expected vs actual. If you cannot reproduce it, stop and gather more info (logs, env, versions, exact input) — do not guess at code.
2. **Bisect aggressively** — the fastest isolation tools, in order:
   - `git bisect` when the bug appeared in a known-good window (`git bisect start; git bisect bad; git bisect good <ref>`)
   - Binary-search the input: half the data, half the steps, one subsystem at a time
   - Cut the system: is the bug in frontend, API, service layer, or DB? Prove it with a direct probe (curl, SQL query, unit call) instead of tracing code by eye
3. **Form one falsifiable hypothesis.** "X is null because Y doesn't await Z, so the map silently drops the entry." Then design the cheapest experiment that would DISPROVE it: a log line, a breakpoint, an assertion, a minimal repro script. One hypothesis at a time — never two changes between observations.
4. **Read the error properly.** Full stack trace, bottom-up for async. `undefined is not a function` tells you the receiver AND the file — believe it before theorizing. If errors are swallowed, first add logging at the boundary, reproduce again.
5. **Fix minimally** at the root: the smallest change that makes reality match intent. No drive-by refactors in a bugfix. If the proper fix is large, do the minimal safe fix + flag the follow-up.
6. **Write the regression test first** from your repro (see test-forge), watch it fail on the old code, pass on the new.
7. **Check for siblings.** Search the codebase for the same pattern elsewhere (`grep` the idiom). Same-author bugs cluster. List what you found.
8. **Post-mortem in one paragraph**: root cause, why tests missed it, what now prevents recurrence.

## Anti-patterns (hard bans)

- NEVER wrap the crash site in try/catch to "make it work" — that buries the disease.
- NEVER change two things before re-running the repro; you'll learn nothing and create new bugs.
- NEVER blame the framework/compiler/stdlib until you have a minimal repro proving it. 99% of the time it's your code's assumptions (cache, timezone, encoding, race, stale build, dirty env).
- If the bug "disappeared" without explanation, it did not disappear. Keep hunting (usually environment/stale state) or explicitly downgrade with a note.
---

*(Part of [claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro) — 15 skills in total: 7 MIT samples in-repo plus 8 more in the free full pack (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) and an 11-chapter CN handbook. Everything is free — grab the pack from [Releases](https://github.com/Hahaknight/claude-skills-pro/releases).)*
