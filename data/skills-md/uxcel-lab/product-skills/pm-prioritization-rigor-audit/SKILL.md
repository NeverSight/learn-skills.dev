---
name: pm-prioritization-rigor-audit
description: Run a structured rigor audit on prioritization decisions, scored backlogs, RICE/ICE/MoSCoW outputs, or roadmap orderings. Produces a severity-rated issue list with concrete fixes — catches invented scores with false precision, priorities unmoored from strategy, feature-factory ordering, everything-is-a-must-have inflation, and trade-offs left implicit. Use when reviewing a prioritized backlog, scoring exercise, roadmap order, or "what should we build first" decision, or as a validation step after any prioritization work.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Prioritization Rigor Audit Skill

## What this skill changes vs. default behavior

By default, Claude *performs* prioritization confidently — it fills RICE tables with invented numbers, ranks features by plausible-sounding impact, and presents the result with unearned precision. Reviewing someone else's prioritization, it tends to accept scores at face value. This audit forces four things: every score is traced to its evidence (or flagged as decoration), every ranking is traced to a strategic outcome (or flagged as unmoored), every "must-have" is challenged, and every decision is checked for an explicit, stress-tested trade-off. Findings come severity-rated with concrete fixes.

This is an **evaluative** skill: it auto-runs whenever a prioritized list, scoring table, backlog order, or build-next decision appears in work being reviewed or generated.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when the `pm-product-review` orchestrator or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **an artifact-specific lens — offered (when work is prioritized or roadmapped)**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. Evidence behind scores (the false-precision check)

A RICE/ICE score is only as good as its inputs. Reach should come from real usage data, impact from a hypothesis someone can defend, confidence from the *quality of evidence* — not from optimism. Scores invented to two decimal places are intuition wearing a lab coat.

**Flag when:** scores appear without sources; confidence is uniformly high; effort estimates lack engineering input; the precision of the output (e.g., "RICE 847.5") exceeds the precision of any input; scoring was applied *after* the decision to justify it.

- ❌ "Reach: 9, Impact: 8, Confidence: 90% — RICE says build it" (no data named anywhere)
- ✅ "Reach: ~5,000 new users/mo (signup analytics); Impact: medium (2) — activation, not revenue; Confidence: 80% (interview evidence for the problem, none yet for the solution)"

### 2. Strategy linkage (the unmoored-priorities check)

Every ranking implies criteria, and the criteria must come from the product strategy — explicit, weighted, and written down. A priority list that can't name what strategic outcome each top item advances is ordered by loudness, recency, or stakeholder power.

**Flag when:** no stated criteria; criteria that don't trace to strategic goals; top items that serve a single deal or the loudest voice; a "weighted scoring" exercise whose weights nobody chose deliberately; priorities unchanged after a stated strategy change.

- ❌ Top of backlog: custom reporting dashboard for one enterprise prospect, rationale "sales needs it"
- ✅ "Criteria from strategy (mid-market expansion): deal-size impact 40%, security coverage 30%, admin depth 30% — scored 1–5, weights sum to 100%"

### 3. Outcome orientation (the feature-factory check)

Prioritization that ranks *outputs* produces a feature factory: many releases, no progress. Items should be framed as problems/outcomes with the user count and pain severity known, and each should map back to the hypothesis it serves.

**Flag when:** the list is pure feature names with no problem statements; nothing states how many users are affected or how severely; items can't be traced to an original hypothesis ("we believe [segment] will [behavior] because [reason]"); success of the ranked work is defined as "shipped."

- ❌ "1. AI assistant 2. Dark mode 3. New dashboard" — no problems, no outcomes
- ✅ "1. Activation drop-off at step 3 (affects 60% of signups, blocks the north-star driver) — candidate solutions listed beneath"

### 4. Honest categories (the must-have-inflation check)

MoSCoW and quick-win/major-project portfolios only work when categories have teeth. When everything is a must-have, nothing is; when "Won't have" is empty, scope creep is pre-approved.

**Flag when:** >~60% of items sit in Must Have; "Won't have" is empty or missing; no quick wins anywhere (momentum starves) or *only* quick wins (transformation never happens); Kano logic inverted — delighters prioritized while basics are broken.

- ❌ 14 of 18 items "Must Have," Won't-have list absent
- ✅ Musts = product fails without them; explicit Won't-haves with reasons; a balanced quick-win/major-project mix

### 5. Explicit trade-offs (the silent-cost check)

Every yes is a no to something. Rigor means the rejected alternatives, the costs of the chosen path, and the reasoning are visible — and would survive a stakeholder's "why this, why now?"

**Flag when:** no record of what was deprioritized or why; decisions jump from problem to choice with the tension smoothed over; the user-value vs. business-viability conflict is presented as naturally aligned; no answer to "what evidence would change this decision?"

- ❌ "We prioritized onboarding improvements." (and silence)
- ✅ "Onboarding over advanced reporting: activation lifts the whole base; reporting serves 8% of accounts — revisit if enterprise pipeline doubles. Cost: reporting customers wait a quarter."

### 6. Framework fit and consistency

Frameworks are tools with known failure modes: RICE needs data and time; MoSCoW ignores effort; Kano needs real survey input (not guessed "delighters"). And a framework applied selectively — abandoned whenever results are inconvenient — is worse than none.

**Flag when:** a framework mismatched to the situation (RICE with zero data; Kano categories assigned by gut); framework-hopping between decisions; scores overridden by intuition without documenting why; constraints (time/scope/complexity triangle) ignored in effort estimates.

- ❌ Kano "delighter" labels assigned in a meeting, no user survey behind them
- ✅ "MoSCoW for this release (fixed deadline, low data); RICE deferred until analytics mature"

> **Tension note:** rigor vs. speed — not every decision deserves a full scoring exercise; a reversible, low-stakes choice made quickly is *good* prioritization. Flag missing rigor where the decision is expensive to reverse, not everywhere. And strategic bets legitimately override scores — the requirement is that the override is explicit and reasoned, not that math always wins.

---

## Severity rating

Rate each finding by **decision damage** — what the prioritization, left as-is, would cause the team to build or skip:

| Severity | Meaning |
|---|---|
| **Critical** | The ordering would steer the team wrong (priorities serving one deal over strategy, invented scores driving an expensive irreversible bet, feature-factory list with no outcomes) |
| **Major** | The reasoning can't be defended or audited (no criteria, no evidence trail, silent trade-offs, must-have inflation) |
| **Minor** | Process hygiene (framework mismatch on low-stakes items, missing Won't-have list, stale priorities after strategy shifts) |
| **Cosmetic** | Formatting/labeling polish; don't pad the report with these |

Overlaps: whether the *metrics* used as criteria are themselves valid belongs to `pm-okr-metric-validity-audit` — this audit assumes the criteria and checks the *ranking discipline*. Broader decision-process quality (bias, reversibility, process-vs-outcome) belongs to `pm-decision-quality-audit`.

---

## Output format

```
## Prioritization Rigor Audit — [Target]
Context: [team/product · decision stakes · framework used · data available, if known]

### Critical
- [Issue] — what's wrong → concrete fix. (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest decision-damage fixes, each with the specific question the team must answer.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — decision stakes and reversibility, what data exists, deadline pressure, and which framework (if any) was used. These set the rigor bar.
2. **Only flag real costs** — directional evidence is legitimate; flag *absent* or *fabricated* evidence, not imperfect evidence.
3. **Respect the speed tension** — quick calls on reversible items are healthy; don't prescribe ceremony.
4. **Prioritize, don't enumerate** — the three findings that would change what gets built next quarter beat ten hygiene notes.
5. **Be specific in fixes** — name the missing data source, propose the criteria weights, draft the Won't-have entry. Never just "add more rigor."

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Accept a RICE table at face value | Trace each score to its evidence; flag decoration |
| Fill in plausible scores when auditing a gap | Name the gap: "Reach is unmeasured — pull signup analytics" |
| Treat a ranked feature list as prioritization | Demand problems/outcomes with affected-user counts |
| Let "everything is critical" stand | Force Must-have teeth and an explicit Won't-have list |
| Praise the framework choice and move on | Check the framework fits the data and the stakes |
| Demand full scoring for every small call | Scale rigor to reversibility and cost |
| Re-audit the metrics' validity | Defer metric quality to `pm-okr-metric-validity-audit` |
| Deliver an unranked issue dump | Severity by decision damage + top-3 with the questions to answer |

---

## Source lessons (Uxcel)

- [Ruthless Prioritization](https://uxcel.com/lessons/ruthless-prioritization-437)
- [The Frameworks that Guide You](https://uxcel.com/lessons/the-frameworks-that-guide-you-385)
- [Using the Product Strategy to Prioritize](https://uxcel.com/lessons/using-the-product-strategy-to-prioritize-345)
- [Prioritization and Trade-Offs](https://uxcel.com/lessons/prioritization-and-trade-offs-183)
- [The Art of Prioritization](https://uxcel.com/lessons/the-art-of-prioritization-474)
