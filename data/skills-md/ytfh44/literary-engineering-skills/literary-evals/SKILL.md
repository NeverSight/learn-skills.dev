---
name: literary-evals
description: Use when testing literary skills, prompts, rubrics, or repeated model outputs for trigger accuracy, causal understanding, counterexample handling, cross-language transfer, regression, or newly learned stock phrases rather than revising one passage only; use for the pack's per-skill trigger batteries (22 skills) and minimal-pair suites.
license: Apache-2.0
---

# Literary Evals

## Use when

You are testing a method, not merely judging a sentence. Prefer paired cases and falsifiable mechanisms over a single “literariness” score.

## Do not use when

For one passage and one suspected variable, use `counterfactual-revision`. For broad diagnosis without an existing rubric, use `literary-style-router` first.

## Core test

**A rule is useful only if it improves the target case and spares the
counterexample.**

The pack's trigger battery covers all 22 skills with four fixture families
per skill (should-trigger, should-not-trigger, ambiguous, quality cases);
see `tests/eval_cases.yaml` and `tests/run_trigger_battery.py`. Fixture
coverage is checked statically; prompt-trigger accuracy must be executed by
the host agent that will use the skills.

## Evaluation families

1. **Trigger cases** — should load / should not load / ambiguous near-miss.
2. **Minimal pairs** — one variable causes the target effect.
3. **Counterexamples** — the suspicious form is necessary and must survive.
4. **Adversarial cases** — the obvious heuristic points the wrong way.
5. **Transfer cases** — a mechanism moves across languages through native
   carriers rather than calques; includes transfer-residue checks (what
   could not survive).
6. **Regression cases** — outputs after a skill edit do not acquire a new
   stock phrase.
7. **Convergence cases** — different words, same operation skeleton (see
   `corpus-convergence-audit`).

## Workflow

1. Name the behavior under test.
2. Build a no-guidance or previous-version control when possible.
3. Pair a positive case with a near-miss negative.
4. Add at least one case where the heuristic must not fire.
5. Grade the mechanism, not polish: did the answer identify the causal variable?
6. Inspect repeated wording across outputs. A skill that kills one cliché by installing another has regressed.

## Minimal pair

Case A: `“黑得像墨。”是否精确？` — metaphor skill should inspect whether “ink” adds anything beyond darkness.

Case B: `“墨汁在纸纤维里停成一圈毛边。”是否精确？` — the same source domain may now be literal or object-specific; the heuristic must not reject “墨” by association.

The target is discrimination, not cliché counting.

## Counterexamples

- A conventional metaphor can be exact when its conventional trait is the scene's needed trait.
- A relation-heavy sentence can be correct when it is an argument, not scene prose.

## Rule strength

**Method — eval protocol.** No literary-quality scoring, no numeric
“literariness” verdicts. The reliable outputs are per-case verdicts
(mechanism identified / missed), fixture coverage, and regression deltas.
Scores may summarize a suite but never replace the per-case reason.

## Script

`scripts/phrase_recurrence.py` detects repeated n-grams and scaffolds across outputs. Treat recurrence as a manual-inspection trigger, never as proof of bad style.

## Read next

- [minimal-pair-suite.md](references/minimal-pair-suite.md) for pair design.
- [adversarial-prompts.md](references/adversarial-prompts.md) for heuristic traps.
- [multilingual-regression.md](references/multilingual-regression.md) for transfer tests.
- [grading-rubrics.md](references/grading-rubrics.md) for causal grading.

## Return shape

Prefer a case table with **expected mechanism, pass condition, fail condition, observed result**. Numeric scores may summarize a suite, but never replace the per-case reason. For convergence work, return the operation trace alongside the surface text.
