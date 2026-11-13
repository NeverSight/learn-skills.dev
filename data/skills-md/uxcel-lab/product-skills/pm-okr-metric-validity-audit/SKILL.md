---
name: pm-okr-metric-validity-audit
description: Run a structured validity audit on OKRs, KPIs, North Star Metrics, or any success-metric set. Produces a severity-rated issue list with concrete fixes — catches vanity metrics, unfalsifiable key results, outputs disguised as outcomes, gameable targets without guardrails, and metrics disconnected from business value. Use when reviewing OKRs, goals, KPIs, dashboards, or success metrics, or as a validation step after defining metrics in a spec, roadmap, or strategy doc.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# OKR & Metric Validity Audit Skill

## What this skill changes vs. default behavior

By default, Claude reviews OKRs by polishing wording and nodding at structure — it rarely challenges whether a key result is *falsifiable*, whether a metric is *vanity*, whether an "objective" is just a feature launch in disguise, or whether hitting the target could actually *harm* the product. This audit forces four things: every finding names the violated principle, every metric is tested for decision-usefulness ("what would we do differently if this number changed?"), every optimization target is checked for gaming exposure and guardrails, and findings come severity-rated with concrete rewrites — not general encouragement.

This is an **evaluative** skill: it auto-runs whenever OKRs, KPIs, or success metrics are present in work being reviewed or generated.

**Scope discipline.** When invoked directly (the user named this audit), review **only this concern** — don't pull in sibling audits. It runs alongside other lenses only when the `pm-product-review` orchestrator or a generative skill calls it under `docs/orchestration-policy.md`, where it sits in **an artifact-specific lens — offered (when metrics/OKRs are defined)**. Explicit scope always wins.

---

## The framework — what to check and what a violation looks like

### 1. Outcome, not output

Outputs are things teams ship (features, releases, launches). Outcomes are changes in user behavior or business results. Key results and metrics must measure outcomes; counting shipped things is the feature-factory signature.

**Flag when:** a KR or metric counts deliverables, launches, tickets closed, or activities performed; an objective prescribes a solution ("Launch mobile app by Q3").

- ❌ KR: "Ship 12 features this quarter" · Objective: "Launch the referral program"
- ✅ KR: "Increase week-4 retention from 22% to 30%" · Objective: "Make our signup the simplest in the industry"

### 2. Falsifiability (the SMART test)

Each key result is obviously achieved or not — a number, a unit, a baseline, a target, a timeframe. If reasonable people could disagree about whether it was hit, it's a wish, not a key result.

**Flag when:** no baseline or target value; no unit; no timeframe; verbs like "improve," "optimize," "enhance" with nothing measurable attached.

- ❌ "Improve user satisfaction" / "Significantly reduce churn"
- ✅ "Increase NPS from 42 to 50 by end of Q3" / "Reduce monthly churn from 4.1% to 3.0% by December"

### 3. Vanity exposure

Vanity metrics grow with time or marketing spend without informing any decision: page views, impressions, downloads, followers, registered totals. The test: *what decision changes when this number moves?* No answer → vanity.

**Flag when:** cumulative or attention-volume metrics presented as success; "active users" without an activity qualification; growth numbers with no conversion-to-value link (80k visitors, still 8 sales).

- ❌ "Reach 200,000 downloads" (3,000 active users hiding underneath)
- ✅ "Convert 12% of downloads to week-2 active users"

### 4. Objective quality

Objectives inspire direction; key results measure progress. An objective should be concise, qualitative, ambitious, and memorable — not corporate fog, and not a task list.

**Flag when:** objectives read as tasks or solutions; vague corporate language ("Optimize customer acquisition efficiency"); more than ~1 focus objective per team per quarterly cycle; KRs that don't actually evidence their objective.

- ❌ "Leverage synergies to optimize the funnel" + 9 objectives for one team
- ✅ One quarter, one focused objective + 3–5 KRs that prove it

### 5. Causal connection to value

Every metric earns its place by a testable cause-and-effect link to user value and business success. The hierarchy: **North Star** (user value + company success in one number) → **KPIs/L1 drivers** → **team input metrics**. An orphan metric — connected to nothing above it — is noise.

**Flag when:** a North Star that's pure business (revenue) or pure activity (time on site) without a user-value mechanism; metrics no one can trace to the level above; "measure everything" dashboards (30+ metrics) with no hierarchy.

- ❌ North Star: "Total registered users" — grows forever, says nothing about value delivered
- ✅ North Star: "Time spent listening" (Spotify) / "Orders delivered & positively rated" — value and success in one number

### 6. Gaming exposure & guardrails (Goodhart's law)

When a measure becomes a target, it stops being a good measure. Ask of every optimization target: *how would a cynical team hit this number while making the product worse?* If there's an easy answer and no guardrail metric, that's a finding.

**Flag when:** engagement/duration targets hittable via friction or addiction mechanics; conversion targets hittable by hiding information (→ dark-pattern territory); no guardrail thresholds (quality, support tickets, ease-of-use, opt-outs) paired with aggressive growth targets.

- ❌ "Increase average session duration by 20%" — with no quality guardrail
- ✅ Same target + guardrail: "task completion time does not increase; support contacts stay flat"

### 7. Leading/lagging balance

Lagging indicators (revenue, churn) confirm what already happened; leading indicators (activation, early engagement, onboarding completion) allow course-correction. An all-lagging metric set can only report failure after the fact.

**Flag when:** every KR is a lagging business outcome with no leading drivers; or all leading with no tie to lagging confirmation.

- ❌ Quarterly OKRs measured only by MRR and churn
- ✅ MRR target + leading drivers: trial-to-paid conversion, first-2-week engagement

> **Tension note:** ambition vs. falsifiability — OKRs should stretch (≈70% achievement is healthy), so don't flag a target merely for being aggressive; flag it for being unmeasurable, disconnected, or gameable. And rigor vs. focus — don't fix metric sprawl by demanding *more* metrics; the fix is usually fewer, better-connected ones.

---

## Severity rating

Rate each finding by **decision damage** — what the metric, left as-is, would cause the team to do:

| Severity | Meaning |
|---|---|
| **Critical** | Optimizing this metric as written would harm users or the business (gameable target without guardrails, vanity North Star, output-only OKRs steering a feature factory) |
| **Major** | Progress can't be honestly assessed (unfalsifiable KRs, no baselines, orphan metrics, all-lagging sets) |
| **Minor** | Hygiene that degrades the system (missing timeframe, >5 KRs per objective, mild metric sprawl, fuzzy objective wording) |
| **Cosmetic** | Phrasing polish; don't pad the report with these |

Overlaps: manipulative *UI* built to hit a metric belongs to `ux-dark-patterns-audit` — this audit flags the metric-and-guardrail gap, that one flags the interface. Spec-level requirement quality belongs to `pm-spec-quality-audit`.

---

## Output format

```
## OKR & Metric Validity Audit — [Target]
Context: [team/product · cycle · business model, if known]

### Critical
- [Issue] — what's wrong → concrete rewrite. (Principle)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest decision-damage fixes, with suggested rewrites.
```

Always end with the prioritized top issues — a flat list helps no one act.

---

## How to run a good audit

1. **Establish context first** — business model (SaaS vs. e-commerce metrics differ), product stage (early: activation/engagement; mature: retention/revenue), and which level you're auditing (company NSM vs. team OKRs).
2. **Only flag real costs** — an imperfect-but-honest metric beats a perfect-on-paper one nobody can collect. Ask what data actually exists.
3. **Respect the ambition tension** — stretch targets are a feature of OKRs, not a bug.
4. **Prioritize, don't enumerate** — three decision-damaging findings beat fifteen nitpicks.
5. **Be specific in fixes** — rewrite the KR; name the guardrail; propose the North Star candidate. Never just "make it more measurable."

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Polish OKR wording and call it a review | Test falsifiability, vanity, gaming, and value-connection per metric |
| Praise "200k downloads" as traction | Ask what decision the number informs; surface the active-user truth |
| Accept "Launch X" as a key result | Rewrite as the behavior/business change the launch should cause |
| Demand precision on every aspirational objective | Objectives inspire; KRs measure — audit each by its own job |
| Flag a stretch target as "unrealistic" | Flag unmeasurable, orphaned, or gameable — not ambitious |
| Recommend adding 10 more metrics | Fewer, hierarchy-connected metrics + guardrails |
| Duplicate the dark-patterns audit on manipulative UI | Flag the metric/guardrail gap; defer the interface to `ux-dark-patterns-audit` |
| Deliver an unranked issue dump | Severity by decision damage + top-3 priorities with rewrites |

---

## Source lessons (Uxcel)

- [OKRs, KPIs, and North Star Metrics](https://uxcel.com/lessons/okrs-kpis-and-north-star-metrics-714)
- [The Anatomy of Good (And Bad) Metrics](https://uxcel.com/lessons/the-anatomy-of-good-metrics-462)
- [Vanity vs. Actionable Metrics](https://uxcel.com/lessons/vanity-vs-actionable-metrics-745)
- [Thinking in Outcomes, not Features](https://uxcel.com/lessons/thinking-in-outcomes-not-features-287)
- [Selecting Effective Product Metrics](https://uxcel.com/lessons/selecting-effective-product-metrics-985)
- [Dark Patterns and the Importance of Guardrail Metrics](https://uxcel.com/lessons/dark-patterns-and-the-importance-of-guardrail-metrics-398)
