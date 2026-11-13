---
name: pm-prioritization
description: Decide what to build first, or critique a prioritization. Derives criteria from strategy, picks the right framework for the context (RICE/ICE/MoSCoW/Kano/Impact-Effort), scores to expose trade-offs rather than manufacture false precision, sequences for flow, and says no with strategic context. Applies the always-true core and gates context-dependent decisions (which framework, scoring rigor, roadmap horizon, appetite vs. estimate, bets vs. tactical) with trade-offs. Trigger when asked to prioritize features/backlog, rank or sequence work, choose a prioritization framework, decide what to build first or what to cut, run a RICE/ICE/MoSCoW/Kano exercise, or defend a prioritization decision.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Prioritization Skill

## How this skill behaves (read first)

This is a **generative** skill, and prioritization is where good intentions turn into a feature factory. Claude's defaults are the failure modes: reach for **RICE for everything** (the wrong tool for a brand-new product, where reach scores near zero), produce **scores that look objective but rest on guesses**, **rank without tracing to strategy** (so the loudest stakeholder wins), treat the **backlog as a dump**, and pretend you can optimize **time, scope, and quality at once**. Strong prioritization is the opposite: criteria derived from strategy, the *right* framework for the situation, scoring used to *surface trade-offs* rather than fake precision, sequencing that protects flow, and a defensible "no." So this skill gates:

1. **Establish the strategy, the stage/constraints, and the decision's reversibility** — these determine the criteria, the framework, and how much rigor is warranted.
2. **Apply the always-true core** — derive criteria from strategy, treat the backlog as a funnel, score to expose trade-offs, balance value × business × feasibility, make trade-offs explicit, sequence don't just rank, say no with context.
3. **Surface the context-dependent decisions** (which framework, scoring rigor, roadmap horizon, appetite vs. estimate, bets vs. tactical) with trade-offs.

Then it **hands off to `pm-prioritization-rigor-audit`** (its primary pairing), plus `pm-okr-metric-validity-audit`, `pm-assumption-rigor-audit`, and — for high-stakes irreversible calls — `pm-decision-quality-audit`.

Scope: this skill owns the **prioritization decision and its sequencing**. It defers the **roadmap artifact and its communication** to `pm-roadmap`, the **strategy itself** to `pm-vision-strategy`, **finding/validating the problems** to `pm-discovery` and `pm-problem-statement`, and the **spec** to `pm-product-spec`.

---

## Step 0 — Establish context before prioritizing

Ask if not known; state the assumption if proceeding without an answer:

- **What's the strategy and the desired outcomes?** Prioritization criteria are your strategy made explicit. Without named outcomes (retention, enterprise expansion, activation), you're ranking blind and will drift into a feature factory. Establish the vision → strategy → outcomes → opportunities hierarchy first.
- **What stage and constraints are you in?** A brand-new product has no reach to estimate (RICE misfires); a fixed launch date makes scope the only variable; a satisfaction-driven bet calls for Kano. Name capacity, deadlines, dependencies, and technical risk up front.
- **How reversible is the decision?** Rigor scales to stakes: a reversible, cheap call deserves a quick ICE pass; a costly, hard-to-undo bet earns heavier scoring and evidence. Over-analyzing a two-way door wastes the cycle.

---

## The always-apply core (true for any prioritization)

- **Derive criteria from strategy; trace every item back.** Translate strategic choices into 3–5 weighted, scoreable criteria (enterprise strategy → deal-size impact, security, admin depth). A feature that solves a real user problem is still wrong if it doesn't advance the current strategy. If you can't trace an item to a strategic goal, question whether it belongs. *This is the defense against the feature factory.*
- **Treat the backlog as a funnel, not a storage bin.** Keep it selective — the next sprint plus a small second tier of near-term priorities; everything else moves to separate longer-term lists. Bucket items (bugs / tech debt / customer requests / strategic initiatives) so urgent noise doesn't bury high-impact work. An everything-list is a black hole that hides what matters.
- **Score to expose trade-offs, not to manufacture precision.** A framework's value is transparency — it forces assumptions into the open and creates a shared language — *not* the number it produces. Watch for scores that look more reliable than the guesses underneath them; the discussion a score triggers ("why is confidence low here?") matters more than the digits.
- **Balance the three forces.** Weigh user value × business outcomes × feasibility together. Overweight user asks → many small wins that don't advance goals; overweight revenue → drift from real needs; overweight feasibility → you ship only what's easy. Don't let any single voice dominate.
- **Make trade-offs explicit; you can't optimize all three of time, scope, and quality (the Iron Triangle).** Fix any two and the third flexes. A fixed date + fixed budget silently means cut quality — name it before work starts, not after the bugs ship. Saying "yes" to A is saying "not now" to B; say so.
- **Sequence, don't just rank.** A scored list is not a plan. Group work by theme so users feel a coherent change (three checkout improvements together beat three unrelated items), order by dependency so upstream decisions settle first, and define "done" beyond code deployed — analytics firing, support/sales trained, release notes written. Planning the sequence without the enablement work ships code that generates no measurable value.
- **Say "no" with strategic context.** A flat refusal frustrates; "that doesn't align with our current strategy of targeting mid-market" reframes it from opinion to criteria. Keep a parking-lot backlog for misaligned-but-promising ideas. Every yes to a non-strategic feature is a no to something that matters more.
- **Communicate the decision.** Share the framework and the rationale, tailor it to the audience (execs want strategic alignment; engineers want context; sales/support want customer-impact), and show a roadmap grouped by strategic theme. Surprise about priorities usually means communication, not the decision, failed.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Defaulting to one framework for every decision is the failure mode — match the tool to the question.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Which framework** | **RICE**: comparing features in an existing product with estimable reach and higher stakes. **ICE**: quick, early, time-pressed calls. **MoSCoW**: negotiating scope under a fixed deadline (Must ≤ ~60% capacity). **Kano**: satisfaction-driven bets you can survey. **Impact×Effort**: fast early alignment. **Eisenhower**: filtering stakeholder noise, *not* a backlog tool | RICE on a brand-new product (reach → 0 punishes good ideas); using one framework everywhere; MoSCoW where everything becomes a "Must" | Match to context: ICE / Impact×Effort for speed, RICE when stakes and data justify the effort, MoSCoW under deadlines, Kano for satisfaction; then commit to it consistently |
| **Scoring rigor** | Heavier, data-backed scoring for high-stakes, irreversible bets | Manufacturing precise scores for a small reversible call | Scale rigor to reversibility; keep the number a conversation-starter, not a verdict |
| **Confidence vs. projected value** | When uncertainty is high, rank by *confidence it'll work* and validate first, not just projected value | Committing big resources to a high-value / low-confidence idea | Low confidence on a big bet → run a cheap experiment before it jumps the queue |
| **Roadmap horizon format** | **Now-Next-Later** to communicate certainty instead of dates for normal work | Date-committed roadmaps that create false certainty and erode trust when they slip | Now-Next-Later by default; **fixed-date, variable-scope** (Pareto/MVP cut line) only when the deadline is genuinely immovable |
| **Appetite vs. estimate** | **Appetite** (set the time, shape the solution to fit) to control investment | Open-ended estimates that default to extending the deadline when work runs long | Set an appetite; when it runs over, cut scope rather than extend time |
| **Strategic bets vs. tactical needs (and segments)** | Allocate capacity explicitly (e.g. 70/20/10) by product maturity; weight segments by strategic importance | Letting tactical firefighting or one big client crowd out strategic work | Set a target allocation, review it quarterly; escalate cross-segment conflicts to strategy rather than ad-hoc trades |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the reach/impact/confidence estimates are assumptions; is "confidence" grounded in evidence (a pattern, a test) or just optimism?
- **`pm-prioritization-rigor-audit`** *(offer — if it sets priorities)* — its primary pairing: false precision (scores dressed up as certainty), strategy-linkage (does each ranked item trace to a goal?), the feature-factory trap, must-have inflation, and rigor scaled to reversibility.
- **`pm-okr-metric-validity-audit`** *(offer — if it relies on an impact/value metric)* — the "impact/value" criterion the scoring rests on: is it a real outcome, not a vanity or gameable number?
- **`pm-decision-quality-audit`** *(offer — if it makes a high-stakes, hard-to-reverse call)* — process over outcome, reversibility-matched deliberation, sunk-cost and bias guards, documented reasoning and trade-offs.

**Composition (per `docs/orchestration-policy.md` §9):** the roadmap that communicates this (`pm-roadmap`) is downstream (offer to produce next, don't auto-generate). If the audits surface a conflict (e.g., the highest-scoring item doesn't actually advance the strategy, or "confidence" is unfounded), resolve toward the purpose: **prioritization exists to point limited resources at the work that most advances the strategy — keep it traceable, honest about uncertainty, and explicit about what you're saying no to.** For a full idea-to-plan build, `pm-idea-to-plan` is the compositional front door that sequences this step with the rest of the ladder and enforces evidence before the spec.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Reach for RICE (or any one tool) for everything | Match the framework to the context; RICE fails on new products with no reach |
| Rank by gut, then let the loudest stakeholder win | Derive weighted criteria from strategy; trace every item back |
| Treat scores as objective truth | Use them to expose assumptions and trigger discussion, not to fake precision |
| Pile everything into one backlog | Funnel it: next sprint + small second tier; bucket and park the rest |
| Promise fixed date *and* full scope *and* quality | Name the Iron Triangle; fix two, flex the third explicitly |
| Hand engineering a deadline and ask for an estimate | Set an appetite; cut scope, not time, when it runs over |
| Ship a scored list as a plan | Sequence by theme and dependency; define "done" past code-deployed |
| Date-stamped roadmap that slips and erodes trust | Now-Next-Later that communicates certainty; fixed-date only when real |
| Flat "no" that frustrates stakeholders | "Doesn't fit our strategy of X" + a parking lot for later |
| Ship the prioritization unchecked | Hand off to prioritization-rigor (+ okr-metric-validity, assumption-rigor, decision-quality) |

---

## Source lessons (Uxcel)

- [Ruthless Prioritization](https://uxcel.com/lessons/ruthless-prioritization-437)
- [The Frameworks that Guide You](https://uxcel.com/lessons/the-frameworks-that-guide-you-385)
- [The Art of Prioritization](https://uxcel.com/lessons/the-art-of-prioritization-474)
- [Using the Product Strategy to Prioritize](https://uxcel.com/lessons/using-the-product-strategy-to-prioritize-345)
- [Prioritization, Sequencing, & Flow](https://uxcel.com/lessons/prioritization-sequencing-flow-420)
- [Prioritization and Trade-Offs](https://uxcel.com/lessons/prioritization-and-trade-offs-183)
