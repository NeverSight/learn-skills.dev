---
name: dogfood
description: Use after each material behavior slice and before handoff or shipping to exercise runnable work at its real entrypoint.
---

# Dogfood

A material runnable slice changes behavior at a real entrypoint or public seam.
Dogfood each slice and final PR. Tests are not dogfood.

## Inventory

1. Resolve the comparison base with
   `BASE=$(PR_BASE_REF="${DOGFOOD_BASE_REF:-}" "${CLAUDE_PLUGIN_ROOT:-.}/scripts/resolve-pr-base.sh")`.
2. Inspect the full PR from merge-base through committed, staged, unstaged, and untracked work.
3. Map changed behavior to its real entrypoint. A skill includes references, assets, and
   scripts; a hook runs through its actual event. Standalone docs, tests, and evals need no
   experiential coverage.

Locally, cover this turn. Before PR or shipping, cover every runnable branch behavior.

## Loop

Run **use -> abuse -> repair -> replay** on the current implementation.

### Use

Perform each intended journey through the actual implementation. Inspect visible output,
state transitions, side effects, console, network, and logs rather than inferring from code.

Use representative live-scale data with production-like shape and cardinality. Compare
expected and observed counts, ordering, timing, state, and side effects; run long enough to
expose accumulation.

For a bug, first replay the reporter's exact steps on the unfixed behavior. If you cannot reproduce it,
stop diagnosis and request the missing environment or evidence.

### Abuse

Apply each relevant lens and at least one plausible break attempt:

- Careless: empty, invalid, oversized, duplicate, or reordered input.
- Impatient: repeat, double-submit, reload, navigate away, cancel, or interrupt.
- Unlucky: stale or missing data, slow or failed dependency, partial completion.
- Live data: sparse fields, duplicate IDs, mixed versions or tenants, long text, Unicode,
  timezone boundaries, realistic cardinality.
- Performance: measure response time, network, render, CPU, and memory against a baseline or budget.

Prefer credible user behavior over arbitrary cases. Observe failure and recovery directly.

### Repair

An observed defect fails the checkpoint. When automatable, add a RED public-contract test,
fix through `/tdd`, and rerun focused checks. Any behavior edit invalidates prior evidence.

### Replay

Restart at the real entrypoint and repeat intended use plus every break attempt. For a bug,
replay the identical original reproduction and verify adjacent behavior. PASS binds only to
the current runnable state.

## Entrypoints

| Change | Exercise |
|---|---|
| Web/UI | Run, navigate, act, reload, inspect console/network |
| CLI/TUI | Invoke realistic, invalid, and interrupted flows |
| API/worker | Send real requests/events; inspect response and side effects |
| Library | Call the public API from a minimal consumer |
| Hook/automation | Trigger the actual event with representative fixtures |
| Skill/agent | Use on a fresh realistic task and inspect behavior |
| Demo/prototype | Operate it until the question has observed evidence |

Use project-native tools. Fresh agents require explicit delegation.

If a project-local `verify-*` skill exists, use its doctor, drive, evidence, and cleanup.
Verifier drift routes to `/maintain-verification-skill`; a recurring missing path routes to
`/create-verification-skill` after proof.

## Receipt

Bind entrypoint, actions, and observations to the current implementation.
Report `Verdict: PASS | FAIL | BLOCKED`, then:

- **Entrypoint:** exact command, URL, event, or consumer.
- **Actions:** intended journey and break attempts.
- **Observations:** data, outputs, state, effects, console/network/logs, and timing.
- **Repairs:** defects, RED tests, fixes, and replay result.
- **Limits:** untried behavior and reason.

PASS requires direct evidence for every changed behavior. FAIL leaves an observed defect.
BLOCKED names the missing access, environment, hardware, or safety condition.
