---
name: pm-analytics
description: "Run a product-analytics analysis that produces a decision, not a dashboard — start from the question, pick actionable over vanity metrics, separate signal from noise, segment (averages lie), pair quant with qual, and end in an insight→impact→action story. Catches the defaults Claude misses: vanity metrics, correlation-as-causation, reacting to small samples/short windows, survivorship/selection bias, unsegmented averages. Trigger when asked to analyze product data/metrics, plan what to measure, build a funnel/cohort/segment/retention analysis, read analytics, or turn data into a recommendation."
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Product Analytics Skill

## How this skill behaves (read first)

This is a **generative** process skill (it plans or performs an analysis, and can critique one). Analytics is where an AI assistant produces confident, wrong conclusions: Claude reports **vanity metrics** (page views, total signups), treats **correlation as causation**, reacts to a **two-day spike** or an **n=20 sample** as if it were a trend, quotes the **average** (which hides every interesting subgroup), and stops at "here are the numbers" instead of a decision. A dashboard nobody acts on, or an insight built on a bias, is worse than no analysis.

So this skill gates:

1. **Establish context** — the decision/question this informs, the goal it ladders to, and the data available (these set what to measure and which method).
2. **Apply the always-true core** — question first, actionable metrics, signal vs. noise, segment, quant+qual, end in a recommendation.
3. **Surface the context-dependent decisions** (analysis method, leading vs. lagging, tooling, attribution model, cohort type, retention window) with trade-offs; let the user choose.

Then it **hands off to `pm-okr-metric-validity-audit`** (are the chosen metrics valid, not vanity?) and **`pm-assumption-rigor-audit`** (do the causal claims and read-outs survive scrutiny?).

Scope: this skill owns **the analysis process** — what to measure, funnels/cohorts/segments/journeys, reading signal from noise, and the data-to-decision story. It defers the **rigorous validity of a metric's definition** to `pm-okr-metric-validity-audit`, the **statistics of a controlled change** (sample size, significance, guardrails) to `pm-experimentation-ab`, **OKR/KPI artifacts** to `pm-okrs-kpis`, and the **discovery research that generates qualitative "why"** to `pm-discovery`.

---

## Step 0 — Establish context before analyzing

Ask if not known; state the assumption if proceeding without an answer:

- **What decision or question does this inform?** Start from the question, not the data — "why did activation drop?" or "which onboarding step loses users?" An analysis with no decision attached produces noise.
- **What goal does it ladder to?** Tie the metric to a business/user objective so you measure what matters, not what's convenient to track.
- **What data exists, and is it trustworthy?** Event coverage, time range, segments available, known tracking gaps. Thin or biased data changes what you can honestly conclude.

---

## The always-apply core (true for any analysis)

### Measure what matters

- **Question first, then data.** Follow the analytics lifecycle: set the measurement goal → collect → analyze → **act**. Each insight feeds the next question.
- **Actionable over vanity metrics.** Page views and total registered users flatter a deck but don't guide a decision. The test: *"if this number moves significantly, do I know exactly what to do?"* If not, it's a vanity metric. Prefer behavior-linked measures (first-week activation, feature adoption, retention).
- **One primary metric + guardrails.** Tie the analysis to one success metric and watch health/guardrail metrics so a "win" isn't paid for elsewhere. (The rigorous validity check of those metrics belongs to `okr-metric-validity`.)

### Read the data honestly

- **Separate signal from noise.** Don't react to small or short-term fluctuations; use rolling windows (30/90/365-day), moving averages, and look for patterns that repeat across periods and segments before acting.
- **Avoid the data traps** — name them and design around them:
  - **Correlation ≠ causation** — two things moving together (push notifications ↑ and usage ↑) may both be driven by a third (a holiday campaign). Look for a mechanism; confirm cause with an experiment (`experimentation-ab`).
  - **Survivorship bias** — analyzing only the users who stayed hides why others left. Ask who's missing from the data.
  - **Sample-size seduction** — a 50% lift on n=10 vanishes at n=1,000. Wait for enough data.
  - **Selection bias** — decide success metrics *before* looking; document all analyses, not just the flattering ones.
- **Averages lie — segment.** The "typical user" usually doesn't exist. Break results down by device, new vs. returning, acquisition source, and behavior; the interesting story is almost always in a subgroup (overall +10% can hide mobile −5%).

### Turn numbers into a decision

- **Find the "why," then pair quant with qual.** Numbers show *what* happened; talk to the users behind an interesting pattern (almost-converted, churned power users) to learn *why* — then return to the data to validate what you heard.
- **End in insight → impact → action.** Lead with the problem in business terms, not the raw metric ("new users can't find the core feature, ~$50K/mo" beats "DAU −15%"), choose a visualization that clarifies the one insight, and close with a specific, owned, measurable recommendation. An analysis that doesn't change a decision isn't done.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Running every analysis type, or pulling every metric, is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Analysis method** | *Funnel* for step-by-step drop-off in a known flow; *cohort* for how behavior/retention evolves over time; *segment* for how groups differ; *journey/path* for non-linear, cross-touchpoint behavior | Forcing a funnel on exploratory behavior, or path analysis when a simple funnel answers it | Match the method to the question; funnel for conversion, cohort for retention, segment to explain variance |
| **Leading vs. lagging indicators** | Leading (activation, feature adoption) to act early when the goal is rare/slow; lagging (MRR, LTV) to validate outcomes | Steering day-to-day on lagging metrics alone (too late to act) | Pair both — leading to guide action, lagging to confirm it worked |
| **Tooling / platform** | GA for web traffic; Mixpanel/Amplitude for event/behavioral product analytics; Segment to unify pipelines; warehouse (BigQuery/Snowflake) for deep/historical; real-time for live monitoring | Over-engineering a warehouse pipeline for a question a product-analytics tool answers today | Use the event-analytics tool already in place; add a warehouse only when depth/history demands it |
| **Cohort type** | *Behavioral* (did action X) to find the "aha moment"; *time-based* to isolate a release/seasonality; *acquisition* to compare channel quality | Reading one cohort type as if it answered all three questions | Behavioral cohorts to find activation drivers; time-based to measure a change's impact |
| **Retention window** | N-day for daily-use products; weekly/monthly for less frequent; custom for natural cycles (Sunday meal-planning) | A daily-retention lens on a product used weekly (false alarm) | Match the window to the product's natural usage rhythm |
| **Attribution model** | Last-click for simple conversion credit; linear/time-decay when multiple touchpoints contribute | Last-click when upstream channels start journeys that convert elsewhere (under-credits them) | Multi-touch (linear/time-decay) when the journey spans channels; last-click only for simple cases |
| **Qual depth** | Light (support tickets, session notes) for a clear pattern; deep (interviews) when the "why" is load-bearing for a big decision | Acting on quant alone for a costly/irreversible call | Scale qual to the stakes; always sanity-check a surprising number against a user's words |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — do the causal claims hold (or are they correlation dressed as causation), is the read honest (not selection-biased), and are load-bearing conclusions evidenced rather than asserted?
- **`pm-okr-metric-validity-audit`** *(offer — if it names/relies on metrics)* — are the metrics actionable and valid (not vanity), correctly defined, and tied to the objective? This is the rigorous check this skill defers the metric-definition standard to.

**Composition (per `docs/orchestration-policy.md` §9):** for validating a *change* with statistical rigor (sample size, significance, guardrails, peeking), **`pm-experimentation-ab`** is downstream (offer to produce next, don't auto-generate); for a high-stakes, irreversible decision built on the analysis, **`pm-decision-quality-audit`** checks the decision process. If the audits surface a conflict, resolve toward the purpose: **an analysis exists to drive a better decision — if it rests on a vanity metric, an unsegmented average, or an unproven causal claim, fix that before anyone acts on it.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Lead with the data | Start from the decision/question, then measure |
| Report vanity metrics (page views, total signups) | Use actionable metrics — "if it moves, I know what to do" |
| Treat correlation as causation | Look for a mechanism; confirm cause with an experiment |
| React to a two-day spike or n=20 | Use rolling windows; wait for repeatable patterns / enough sample |
| Analyze only the users who stayed | Ask who's missing — guard against survivorship bias |
| Cherry-pick the flattering cut | Pre-commit success metrics; document all analyses |
| Quote the average | Segment by device/source/behavior — averages hide the story |
| Report *what* with no *why* | Pair quant with qual; validate one against the other |
| Stop at the numbers | End with insight → impact → action, owned and measurable |
| Reinvent A/B statistics here | Defer significance/guardrails to experimentation-ab |
| Ship the analysis unchecked | Hand off to okr-metric-validity + assumption-rigor |

---

## Source lessons (Uxcel)

- [Analytics Strategy & Planning](https://uxcel.com/lessons/analytics-strategy-planning-797)
- [Analytics Tools & Platforms](https://uxcel.com/lessons/analytics-tools-platforms-443)
- [Customer Journey Analytics](https://uxcel.com/lessons/customer-journey-analytics-664)
- [Digging into Data](https://uxcel.com/lessons/digging-into-data-610)
- [Analytics Storytelling](https://uxcel.com/lessons/analytics-storytelling-908)
- [User Funnel Analysis](https://uxcel.com/lessons/user-funnel-analysis-474)
- [Cohort & Segment Analysis](https://uxcel.com/lessons/cohort-segment-analysis-878)
