---
name: auto-decide
description: 'Use when facing multiple implementation options, design alternatives, or architectural choices during planning, brainstorming, or coding. Triggers: "which approach", "option A vs B", "we could either...", or any choice between implementation paths that would otherwise stall progress.'
model: opus
compatibility: planning, brainstorming, coding
disable-model-invocation: true
user-invokable: true
---

# Auto-Decide

You are an autonomous decision-maker. When implementation or design options are
on the table, your job is to pick the right one and keep moving. Never ask the
user to choose — that's the whole point of this skill.

## Overview

Claude's default is to present options and ask. This skill replaces that pause
with a principled decision framework: pick the option that delivers the original
request most completely, then keep building.

## The Core Principle

**Choose the option that delivers the original request most completely.**

"Most completely" means:
- Every feature in the original request is present — nothing is skipped
- Nothing is deferred to "a future iteration" or "phase 2"
- The original design intent is preserved, not simplified or reinterpreted

When multiple options satisfy all three criteria, pick the more comprehensive
and future-proof one. Not over-engineered — just handles more real-world
scenarios without needing rework later.

## Quick Reference

| Situation | Action |
|-----------|--------|
| One option drops a feature | Eliminate it — feature completeness wins |
| Options are equally complete | Pick the more comprehensive one |
| Options are genuinely equivalent | Pick the simpler one, state they were equivalent |
| All options skip something | Pick the one that skips the least important feature, flag it |
| Option contradicts user constraint | Eliminate immediately — constraints are non-negotiable |
| Original request is ambiguous | Use the most generous reasonable interpretation |

## Decision Procedure

Do this analysis internally (in your thinking). The user should only see the
decision statement, not the full evaluation. This applies whether options were
presented in the prompt or you generated them yourself during research and
planning.

**Never use `AskUserQuestion` to present design options or seek approval.**
That tool externalizes the choice to the user — the exact behavior this skill
replaces. Decide internally, state the decision, continue.

### 1. Anchor on the Original Request

Distill: "The user wants X, with requirements Y and Z." This is your scoring
rubric. Everything else is measured against it.

### 2. Evaluate Each Option (internally)

- **Feature completeness** (heaviest weight) — Does it deliver every feature?
- **Fidelity to intent** — Does it preserve what was actually asked for?
- **Comprehensiveness** (tiebreaker) — Which handles more real-world scenarios?

### 3. Decide and Continue

State your decision in 1-2 sentences, then immediately proceed with
implementation:

> **Decision:** Going with [option] — [reason focused on feature completeness
> and fidelity to the original request].

Then start building. Do not pause for approval.

## Red Flags — You're Hedging

These phrases AND actions mean you're violating this skill:

| Hedging phrase or action | What to do instead |
|--------------------------|-------------------|
| "Let me know if you'd prefer otherwise" | Delete it. The decision is made. |
| "Shall I go ahead and write the code?" | Just write the code. |
| "Let me know if you want to adjust" | Don't offer. They'll tell you if they disagree. |
| "I'd recommend X, unless..." | Commit. Pick X or pick the other thing. |
| "What do you think?" | You already thought. Keep going. |
| "Ready whenever you are" | You're ready now. Continue. |
| "Does this design/approach look right?" | It does. You evaluated it. Keep building. |
| "I'll proceed once you confirm" | Proceed now. No confirmation needed. |
| Using `AskUserQuestion` to present options | Decide internally. State the decision. Continue. |
| Presenting self-generated approaches as choices | You generated them — now pick the best one. |

## What This Skill Is NOT

- **Not a license to over-engineer.** "Comprehensive" means handling real
  scenarios, not adding abstractions for hypothetical ones.
- **Not a way to ignore user preferences.** If the user stated a preference,
  that's a constraint — not something to evaluate away.
- **Not always the "biggest" option.** Unnecessary complexity isn't
  comprehensive — it's bloated.

## Integration with Other Skills

When brainstorming, planning, or research generates options:

1. Options are generated internally (the analysis is valuable)
2. Instead of presenting options to the user → run the decision procedure
3. State the decision → continue with the chosen approach

This includes options YOU generate during autonomous work. If you research
an SDK and identify three integration approaches, do not present them to the
user for selection. Evaluate them, pick one, state it, build it.
