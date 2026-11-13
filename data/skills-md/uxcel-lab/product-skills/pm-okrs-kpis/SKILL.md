---
name: pm-okrs-kpis
description: Write OKRs, KPIs, or a North Star Metric derived from product strategy — or review an existing goal set. Enforces outcome-based key results with baselines and targets, one focus objective per team per cycle, leading+lagging balance, and guardrails against gameable targets. Trigger when asked to write OKRs, set quarterly goals, define KPIs or success metrics, choose a North Star Metric, or run goal-setting/planning for a team or product.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# OKRs & KPIs Skill

## How this skill behaves (read first)

Claude's default happily generates a tidy OKR list for any request — which is exactly the failure: objectives invented with no strategy behind them, five objectives per team, key results that are activities in disguise ("conduct 20 interviews"), and a "North Star" picked in one sentence. Goals written this way actively misdirect a team for a quarter.

So this skill is **generative but gated**:

1. **Establish context** — strategy, level, cycle, and what data exists. No strategy → say so and work at the right level instead of inventing one.
2. **Apply the always-true core** — outcome KRs with baseline/target/timeframe, one focus objective, leading+lagging mix.
3. **Surface the context-dependent decisions** — framework weight, North Star, cadence, cascading model — with trade-offs; let the user choose.

Then it **hands the result to `pm-okr-metric-validity-audit`** for validation.

---

## Step 0 — Establish context before writing any goal

Ask if not known; state the assumption if proceeding without an answer:

- **Is there a strategy to derive from?** Strategy is the "why/what"; OKRs are the "how much/by when." Without strategic choices, OKRs become disconnected targets that move numbers without advancing position. If none exists, flag it — offer to define the strategic priority first rather than generating goals from nothing.
- **Level** — company, product, or team? Team OKRs should be each team's *chosen contribution* to product objectives, not product KRs mechanically divided up.
- **Team size & maturity** — a small squad may be better served by the simpler levers / rate-limiting-step framing (which metrics move the North Star; which is the bottleneck) than by full OKR ceremony. A squad often needs only 1–2 KRs per objective.
- **Cycle** — quarterly is the default rhythm; annual strategy breaks into sequenced quarterly checkpoints (not every priority appears every quarter).
- **What data exists** — a KR without a collectible number is theater. If the right metric doesn't exist yet, a legitimate KR is "research and define the activation metric" — better than chasing a target you don't understand.

---

## The always-apply core (correct for almost every case)

**Objectives — qualitative, ambitious, memorable:**

- An objective answers "where do we want to go?" — concise, inspiring, time-bound, *not* a solution.
  - ❌ "Launch mobile app by Q3" (an output wearing outcome clothes) ✅ "Delight users with seamless mobile experiences"
  - ❌ "Optimize customer acquisition efficiency" (corporate fog) ✅ "Make our signup the simplest in the industry"
- It must pass the **"So what?" test**: achieving it represents meaningful strategic progress, not completed activity. "Conducted 10 user interviews" fails; "validated that customers will pay 3× more for real-time collaboration" passes.
- **One focus objective per team per quarter.** If only ~1 in 4 experiments works and a team runs one a week, that's ~3 wins a quarter — spreading across multiple objectives spreads to zero. Achieve the highest-impact objective before queueing the next.

**Key results — falsifiable, outcome-based:**

- It's not a key result unless it has a **number**: baseline → target, unit, timeframe. Obviously achieved or not — no room for debate.
  - ❌ "Improve website performance" ✅ "Reduce page load time from 4.2s to under 1.5s by end of Q2"
- KRs measure **outcomes** (behavior/business change), never activity or shipped things.
  - ❌ "Ship the redesigned dashboard" ✅ "Reduce user error rate on dashboard tasks by 40%"
- **2–4 KRs per objective** (1–2 for a single squad — a squad should own a KR; don't over-engineer).
- **Mix leading and lagging** — lagging outcomes (retention, MRR) confirm after the fact; leading drivers (activation, onboarding completion) allow course-correction. An all-lagging set can only report failure once it's too late.
- **Stretch is a feature**: ~70% achievement is healthy. Separate aspirational OKRs from committed deliverables so a miss is information, not betrayal.

**Every target gets the gaming question:**

- Ask "how could someone hit this number while making the product worse?" — and pair aggressive targets with a guardrail (check/health) metric.
  - ❌ "Increase session duration 20%" alone ✅ Same target + "task completion time does not increase; support contacts stay flat"

**KPIs vs. OKRs — don't conflate:**

- KPIs are ongoing health signals (churn, DAU/MAU, resolution time) that persist across cycles; OKRs are the quarterly push for *change*. A KPI can serve as a KR when an objective targets it — but a dashboard of KPIs is not an OKR set, and OKRs shouldn't try to monitor everything.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user decide. **Applying all of these by default is a mistake.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Define a North Star Metric** | Stable business model; need one number uniting customer value + business success (Spotify: time listening; Airbnb: nights booked) that's simple, frequently measurable, product-influenceable | Business model in flux (the wrong North Star misguides the whole strategy — Facebook had to abandon "time spent"); or one already exists | Propose 2–3 candidates with the value-exchange rationale; pressure-test before adopting — it should hold for years |
| **Full metrics hierarchy** (NSM → KPI drivers → team inputs) | Multiple teams need to see how their inputs ladder up; cross-team alignment is the pain | Single team / early product — hierarchy becomes ceremony | Sketch the causal chain (feature adoption → engagement → NSM) even if informal |
| **Cascading model** | Top-down breakdown: tight coordination needed across teams | Team-chosen contribution: teams closest to the work know what moves the objective | Set objectives top-down, let teams propose their own KRs; check team OKRs don't conflict |
| **Cadence ceremony** | Dual cadence (annual strategic + quarterly tactical) + weekly confidence check-ins (green/yellow/red) + mid-quarter review + retrospective: org large enough that drift compounds | Small team — keep planning + weekly check-in + retro only | Scale ceremony down before scaling targets down; never set-and-forget |
| **Metric ownership (RACI)** | Cross-functional metrics where shared responsibility becomes no responsibility | Obvious single-owner metrics | One accountable owner per KR, named at planning |
| **Mid-cycle OKR changes** | Genuine strategy shift (self-serve → enterprise pivot) | Tactical changes within an objective (email → in-app tutorials needs no new OKR) | Default to stability; if changing, document why and what was learned — constant metric-shifting destroys trust in the system |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`okr-metric-validity` is the always-relevant lens for this artifact (auto-runs)** — a goal set's whole value rests on metric validity. If the user invoked this skill for one specific thing, respect that scope. For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that pulls this in as the success-metrics rung after the plan is framed and de-risked.

- **`pm-okr-metric-validity-audit`** *(auto-runs)* — every objective, KR, KPI, and North Star candidate: vanity exposure, falsifiability, outputs-as-outcomes, gaming/guardrails, causal connection to value, leading/lagging balance. This skill writes; that audit interrogates.

If the audit surfaces a conflict, resolve back toward the primary goal: a small set of goals the team can actually steer by — fewer, better-connected metrics beat comprehensive ones.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Generate OKRs from a one-line request with no strategy | Gate: ask what strategic choice these goals serve; flag if none exists |
| Write 4 objectives per team "to cover everything" | One focus objective; queue the rest |
| "Increase engagement" as a KR | "Increase DAU/MAU stickiness from 18% to 25% by end of Q3" |
| Accept "launch X" as a key result | Rewrite as the behavior change the launch should cause |
| Pick a North Star in one sentence | Propose candidates, test the value-exchange logic, warn it should hold for years |
| Set an aggressive growth target alone | Pair it with a named guardrail metric |
| All-lagging KR sets (MRR, churn only) | Add the leading drivers the team can act on weekly |
| Divide product KRs mechanically among teams | Let teams propose their contribution; check for conflicts |
| Treat 70% achievement as failure | Frame stretch as designed; separate committed from aspirational |
| Ship the goal set as final | Hand off to `pm-okr-metric-validity-audit` |

---

## Source lessons (Uxcel)

- [OKRs, KPIs, and North Star Metrics](https://uxcel.com/lessons/okrs-kpis-and-north-star-metrics-714)
- [Using the Product Strategy to Defining OKRs](https://uxcel.com/lessons/using-the-product-strategy-to-defining-okrs-217)
- [Defining Success Metrics](https://uxcel.com/lessons/defining-success-metrics-773)
- [Thinking in Outcomes, not Features](https://uxcel.com/lessons/thinking-in-outcomes-not-features-287)
- [Cadence, Rituals, and Accountability](https://uxcel.com/lessons/cadence-rituals-and-accountability-263)
- [Product Metrics & KPIs](https://uxcel.com/lessons/product-metrics-kpis-278)
