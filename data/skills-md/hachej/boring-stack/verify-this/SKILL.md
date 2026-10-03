---
name: verify-this
description: "Verify a claim with fresh local evidence: restate it falsifiably, capture baseline and treatment, compare artifacts, and return VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Use when asked to verify this, prove it works, did this fix it, or show the evidence."
---

# Verify This

Adapted from Cursor's `cursor-team-kit/verify-this` (MIT, see THIRD_PARTY.md), with this app's surfaces.

Verification is not a recap. It proves or disproves a specific claim with repeatable evidence.

## When To Use

- The person asks "verify this", "prove it works", "did this fix it", or "show me the evidence".
- A bug fix needs a before/after repro.
- A page, API, agent-output or performance claim needs measurement.
- A test passes but the user-visible behaviour still needs confirmation.

Do not use this for vague claims like "the code is cleaner". Ask for a measurable claim first.

## Workflow

1. Restate the claim in falsifiable form: condition, metric, and threshold.
2. Pick the smallest local surface that can disprove it (below).
3. Capture a baseline from the old state: the merge base, the parent commit, or the current broken repro (a git worktree of the base gets its own verify instance).
4. Capture the treatment from the changed state with the same command, data and environment.
5. Compare raw artifacts: numbers, snapshots, HTTP responses, run rows, eval tables.
6. Return exactly one verdict: `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

## Local surfaces in this app

- Code behaviour: a focused unit test (`node --test test/unit/<file>`).
- The page: `node scripts/verify.mjs` (the **verify-app** skill): `snapshot`, `screenshot`, `network-summary --since-mark`, `trace`.
- The API and the wire: `verify api <path>` before and after.
- What an agent writes: `node scripts/verify.mjs up --real` and drive it, or the evals of hachej/boring-stack for the expert's skill.
- Performance: `verify perf`, or timings from the same machine for baseline and treatment.

## Verdict Rules

- `VERIFIED`: baseline and treatment differ in the predicted direction, by the claimed threshold, with no obvious confound.
- `NOT VERIFIED`: the behaviour is unchanged, moves the wrong way, or misses the threshold.
- `INCONCLUSIVE`: no valid baseline, noisy signal (agent outputs on 3 cases are noisy), failed measurement, or an environment difference invalidates the comparison.

## Output

```text
VERIFIED | NOT VERIFIED | INCONCLUSIVE
Claim: <falsifiable claim>

Evidence:
<metric/artifact>: baseline=<...>, treatment=<...>, delta=<...>, threshold=<...>

Reasoning:
<one tight paragraph naming the evidence and any confounds>
```

Do not soften a negative result. A clear `NOT VERIFIED` is useful. Never put real user data in an artifact you commit.
