---
name: pythia-verify
description: Use before saying an Oracle task is done, fixed, deployed, faster or working - before the final report, before "xong roi", "da sua xong", "deployed", before ending an autopilot session. Collects the evidence from this session - compile errors, INVALID objects against the baseline, lint, journal entries, before/after plans when performance was the point - and reports only what that evidence proves.
---

# Verifying Before Claiming Done

**Announce at start:** "Using pythia-verify — checking the evidence before I report."

**Phase:** Learn → Ask — collect proof from the live database, then report what it shows and what it does not

The most expensive sentence an agent writes is "done" about something that
is not. In Oracle it is easy to say: a package can be written and INVALID,
a release can stop at statement 7 of 12, a "faster" query can have the same
plan. The evidence is three commands away — run them.

## The Iron Law

```
NO COMPLETION CLAIM WITHOUT EVIDENCE FROM THIS SESSION
```

Evidence is command output you saw after the last change, not a result you
remember from before it.

## The Checklist

1. **Every write's verdict** — the exit code of each `apply` / `deploy`,
   read unpiped (`| tail` returns tail's 0). Under autopilot:
   `pythia autopilot report`, every row.
2. **It compiles** — `pythia errors <OBJECT>` for every object you touched:
   empty, or the errors listed.
3. **Nothing else broke** — `pythia invalid` compared with the baseline you
   took in `pythia-impact`. Anything INVALID now that was VALID then is
   yours until proven otherwise.
4. **It meets the standard** — `pythia lint <files>`: zero errors; warnings
   fixed or named with a reason.
5. **Tables are documented** — `pythia cols T` matches the spec;
   `pythia comments T` says 0 missing; `pythia stats T` lists no unindexed
   foreign key you created.
6. **Performance claims** — the same `pythia explain` before and after,
   with the numbers (`pythia-tune`'s report format).
7. **Behaviour** — pythia does not run anonymous blocks, so it cannot prove
   behaviour by itself. Say what was tested (utPLSQL by CI or the
   developer, a query that shows the new rows) and what was **not**.

## The Report

```
Done:          PKG_ORDER spec+body, T_ORDER_LINE (+6 comments, 1 index)
Evidence:      deploy exit 0 (5/5); errors PKG_ORDER: none; invalid: 1, same
               as baseline (X_ALREADY_BROKEN); lint: 0 errors, 1 warning (named)
Decisions:     status codes N/C/X (agreed); qty NUMBER(12,3) (agreed)
Assumptions:   none
Not verified:  behaviour under load; ut_pkg_order not run (no utPLSQL here)
Undo:          pythia journal restore <entry>  (newest first, per object)
```

Three words are reserved: **done** (every check passed), **broken** (exit 3
or new INVALID — say it first), **not verified** (a check you could not
run). Never soften broken into "mostly done".

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "It compiled, so it works" | Compiling proves syntax. Say what proves behaviour, or say it is not verified. |
| "apply said ok earlier" | Earlier was before the last change. Check again. |
| "Those INVALID objects were already broken" | Show the baseline that proves it, or they are yours. |
| "The developer can check the details" | The details are the report. Run the commands. |
| "One statement failed but the rest landed — mostly done" | That is broken, with an undo list. Lead with it. |
| "I'll skip lint, I followed the standard" | Then lint costs one second and says so. |

## When NOT to use this skill

- Mid-task, between steps — `pythia-apply` already reads each result; this
  is the gate before the final word.
- Pure exploration with no change made — there is nothing to verify; say
  what you read.
