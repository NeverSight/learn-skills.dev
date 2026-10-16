---
name: game-balance-analysis
description: Specialized in game numerical design, this skill designs first-pass game balance values, diagnoses and tunes existing systems, and evaluates balance proposals by building and running executable models, simulators, parameter sweeps, and evidence checks. Use for combat, progression, economies, items/builds, PvP/metagames, and random rewards when the task requires concrete numbers or a supported verdict. Do not use for broad qualitative game-design critique without a numeric or systemic balance decision.
---

# Game Balance Analysis

Design, analyze, and judge game balance through concrete models and player-
facing outcomes. Produce actual values, tables, calculations, tuning options,
or verdicts rather than a general discussion of balance theory.

## Core rules

### Select the balance target

Classify the task before modeling. A request may involve one or more of:

- mathematical relationships between costs, benefits, rates, and outcomes;
- difficulty for an intended audience or skill band;
- progression of player power, challenge, access, and reward timing;
- initial conditions such as turn order, side, spawn, map, or starting stock;
- viability and interaction of multiple strategies;
- comparative value of objects, abilities, characters, or builds;
- actual and perceived fairness.

When targets conflict, state the tradeoff and prioritize the user's intended
experience. Do not silently optimize one balance type at another's expense.

### Model the relevant context

Attach every conclusion to an audience, mode, content set, skill band, build,
time horizon, and version as relevant. Separate confirmed rules/data,
calculated predictions, design assumptions, and unknowns.

### Classify option relationships

Before comparing options, classify the dominant relationship:

- `transitive`: broadly more benefit should carry more cost or disadvantage;
- `intransitive`: value depends on the opposing choice or counter cycle;
- `situational`: value depends on content, state, timing, or frequency;
- `mixed`: more than one model is required.

Do not force an intransitive or situational set onto one absolute power curve.

### Preserve meaningful differences

Numerical equality is not the goal. Accept deliberate asymmetry or small
deviations when they support identity, discovery, risk, accessibility, or
varied decisions without collapsing the choice space. Recommend adjustment
when a difference makes one legitimate path compulsory, futile, unknowable,
or unfair for the intended context.

### Treat random systems at three levels

Always distinguish:

1. mathematical probability and outcome distribution;
2. player utility, including thresholds, loss, duplication, and diminishing
   value;
3. perceived probability produced by information, presentation, memory, and
   trust.

A mathematically fair random system may still need redesign when its utility
or perceived fairness contradicts the intended experience.

### Match confidence to evidence

Use mathematics for first-pass values and boundary checks, playtests for player
behavior and understanding, and telemetry for repeated population patterns.
One source does not substitute for the others. State what evidence would
confirm or overturn the result.

### Use two executable artifact lifecycles

For every non-trivial numeric design, use executable artifacts to verify the
model and parameters. Read `references/simulation-and-tooling.md` and choose:

- a **temporary verification script** for independent one-off calculation,
  invariants, boundary checks, or proposal judgment; run it, capture the
  evidence needed for the decision, then delete the script and scratch output;
- a **persistent simulation/tuning tool** for a balance system that will be
  designed, explored, or adjusted repeatedly; deliver and retain the tool,
  editable parameters, scenarios, and accepted result set.

Inline arithmetic is sufficient only when a few independent calculations fully
determine the result and parameter sweeps, repeated state, or randomness would
not add useful verification. State why no script is needed.

Do not accept a model from inspection alone. Execute a known baseline, ordinary
and boundary scenarios, and the proposed parameters. When the model is random
or iterative, use fixed seeds and report distributions rather than one run.

Treat a persistent simulator as the executable specification of the balance
model. Validate both **model fidelity** and **parameter fitness**. When results
conflict with confirmed rules, known cases, or observed behavior, determine
whether the model/tool is wrong or the parameters miss their targets. Fix and
version the model and simulator first, add the failed case as a regression
check, rerun validation, and only then tune parameters. Never use parameter
changes to compensate for a known model defect.

## Task routing

Read exactly one primary task playbook:

| Task | Read |
| --- | --- |
| Create first-pass numbers or a new balance model | `references/design-balance-model.md` |
| Diagnose an existing imbalance and tune it | `references/diagnose-and-tune.md` |
| Judge or compare a proposed balance change | `references/evaluate-balance-proposal.md` |

Then read only the relevant domain playbook:

| Domain | Read |
| --- | --- |
| Combat, enemies, XP, levels, rewards, PvE progression | `references/combat-and-progression-playbook.md` |
| Currencies, sources/sinks, prices, trading, inflation | `references/economy-playbook.md` |
| Competitive matchups, snowball, ratings, metagame | `references/pvp-and-metagame-playbook.md` |
| Loot, cards, dice, streaks, pity, duplicate protection | `references/random-reward-playbook.md` |

Read `references/calculation-recipes.md` only for the calculations required by
the task. Read `references/simulation-and-tooling.md` whenever a substantive
numeric model is designed, diagnosed, or judged. Read
`references/evidence-and-validation.md` when conclusions depend on playtests,
telemetry, experiments, or statistical inference.

## Working expectations

- Inspect actual rules, configuration, data, or code behavior before analyzing
  an existing system.
- Make a small set of labeled assumptions and continue when a provisional
  first pass is useful; stop only when plausible answers require opposite
  models or verdicts.
- Calculate ordinary, optimized, and relevant boundary cases.
- Translate parameter changes into player-facing outcomes.
- Trace material effects into adjacent systems and options.
- Create and run a temporary verification script or persistent simulation tool
  for every substantive numeric model. For temporary work, report what was
  checked and confirm cleanup. For retained tools, return the path, invocation,
  inputs, and result summary.
- End with recommended values, tuning options, or an explicit verdict and
  validation plan.

Do not implement the chosen changes unless the user's task or a separate
engineering workflow authorizes implementation.
