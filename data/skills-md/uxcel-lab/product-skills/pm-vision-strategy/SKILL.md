---
name: pm-vision-strategy
description: Produce or critique a product vision and/or product strategy — an aspirational destination and the deliberate, trade-off-driven choices to reach it — not a buzzword poster or a feature list. Distinguishes the vision/strategy/roadmap/mission artifacts, ladders product vision up to company vision, forces a focused segment + differentiation + explicit "won't do", and sets the stability rule (stubborn on vision, flexible on strategy). Applies the always-true core and gates context-dependent decisions (which strategy framework, vision communication format, single vs. multi-product, B2B vs. B2C, new vs. existing, depth). Trigger when asked to write/define/critique a product vision, vision statement, product strategy, strategic themes, positioning/where-to-play/how-to-win, or to tell vision from strategy from roadmap.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Product Vision & Strategy Skill

## How this skill behaves (read first)

This is a **generative** skill, and vision/strategy is where an AI assistant produces its most confident, least useful output. Two default failure modes dominate:

1. **The inspirational poster.** Asked for a vision, Claude writes a buzzword sentence — "be the world's most loved, best-in-class platform that delights customers with seamless experiences" — that sounds good and guides zero decisions. If *any* feature can be justified by it, it's too vague to be a vision.
2. **Conflation and feature-listing.** Claude treats vision, strategy, roadmap, and mission as interchangeable, and writes "strategy" as a list of features to build rather than a set of deliberate choices about where to play, how to win, and **what not to do**. Strategy that targets "everyone" and skips trade-offs isn't strategy.

A real vision is a **specific, stable, user-centric destination**; a real strategy is a **focused set of interconnected, trade-off-driven choices** grounded in evidence and tied to outcomes. So this skill gates:

1. **Establish context** — vision, strategy, or both; company shape; product stage; market type; altitude.
2. **Apply the always-true core** — the artifact distinctions, the laddering, the focus-and-trade-off discipline, the stability rule.
3. **Surface the context-dependent decisions** (which framework, which communication format, portfolio/B2B/stage/depth) with trade-offs, and let the user choose. Running every framework at once is the failure mode.

Then it **hands off to `pm-okr-metric-validity-audit`** (the success metrics it names), **`pm-prioritization-rigor-audit`** (the themes/focus areas it sets, which drive what gets built), and **`pm-assumption-rigor-audit`** (the market-demand and competitive bets the strategy rests on).

Scope: this skill owns **the vision artifact and the strategy artifact, and the choices inside them**. It defers the **competitive/market analysis** that feeds strategy to `pm-competitive-analysis`, the **research/insight-gathering** to `pm-discovery`, **problem framing** to `pm-problem-statement`, the **prioritization decision itself** to `pm-prioritization`, the **OKR/KPI artifacts** to `pm-okrs-kpis`, the **roadmap artifact and sequencing** to `pm-roadmap`, **pricing** to `ux-pricing`, and **go-to-market** to `pm-gtm-plan`.

---

## Step 0 — Establish context before writing

Ask if not known; state the assumption if proceeding without an answer:

- **Vision, strategy, or both?** They're different artifacts at different altitudes (see the core below). Writing one when the user needs the other — or blending them into mush — is the first mistake. If they ask for "a strategy" but have no vision, flag that the vision is the anchor strategy derives from.
- **What's the company shape — single-product or multi-product?** A single-product company's product vision nearly equals its company vision; a multi-product portfolio needs each product's vision/strategy to ladder up to the company vision without colliding with siblings.
- **New product or existing/pivot?** New products derive vision from market research, problem interviews, and a small founder/early-team group; existing products have real usage data, feedback patterns, and a broader stakeholder set to draw on.
- **B2B or B2C?** B2B strategy serves multiple stakeholders (end user, champion, economic buyer), longer cycles, higher switching costs; B2C weights individual decision-makers, viral acquisition, and network effects.
- **What altitude / scope?** A feature-area vision shouldn't span the whole company; a company-wide product vision can be broad. Scope determines who must align and which decisions the vision governs.

---

## The always-apply core (true for any vision or strategy)

### Keep the four artifacts distinct (and ladder them)

- **Don't conflate vision, strategy, roadmap, mission.** They form a hierarchy at decreasing altitude and increasing change-frequency: **company vision → company strategy → product vision → product strategy → roadmap/features.** Vision is the aspirational *destination* (stable for years). Strategy is *how you'll get there* (the choices; evolves every few quarters). Roadmap is *what and when* (changes often). Mission is *why you exist today*; vision is the *future you're creating*. When vision is absent, roadmaps become disconnected feature lists; when strategy masquerades as vision, you lose the inspirational anchor.
  - ❌ "Our vision: ship AI search, a mobile app, and SSO by Q4." (That's a roadmap.)
  - ✅ "Our vision: every analyst finds the answer in their data in seconds, without writing a query." (A destination; many strategies could reach it.)
- **Derive product vision from company vision.** Identify which slice of the company vision your product makes tangible; it should read as a natural, more-specific extension. Translate company strategy (markets, positioning, business model) into product choices (which problems, which users, which capabilities first).

### Make the vision specific, user-centric, and memorable

- **Three traits: user-centric, simple, future-facing.** Describe the changed *user* future, not your feature set, in language anyone can recall and repeat without the doc.
  - ❌ "Use integrated data systems to drive optimized wellness outcomes."
  - ✅ "Help people track their health in one simple app." / LinkedIn: "Create economic opportunity for every member of the global workforce."
- **Ban empty superlatives.** "Best-in-class," "world-leading," "seamless," "delight" sound impressive and mean nothing. Use concrete user outcomes instead.
  - ❌ "Empower teams to collaborate." ✅ "Help remote teams make decisions without meetings."
- **The decision-filter test.** A vision works only if it can *reject* a feature. If someone can justify any feature with it, it's too vague — tighten until a feature idea clearly aligns or conflicts.
- **3–5 year horizon.** Shorter than ~3 years is a roadmap, not a vision.

### Make the strategy a set of focused, trade-off-driven choices

- **Strategy = interconnected choices, not a feature list.** Name the winning aspiration (vision), where to play (segment + market), how to win (differentiation), the capabilities/resources required, growth mechanism (product-led vs. sales-led + channels), and key metrics — and check the elements reinforce each other.
- **Pick ONE primary segment; "everyone" means no one.** Define the target by the job/outcome they seek and their constraints, not just demographics. Win one segment and reach product-market fit before expanding (Instagram → iPhone users sharing photos fast, not "all mobile users").
- **Choose a differentiation path and defend it.** Cost leadership, unique value, or focus — not "better at everything." Back it with a barrier (proprietary tech, network effects, data, brand, partnerships). Apply the **"can't or won't" test**: competitors either *can't* copy you (real barrier) or *won't* (it conflicts with their model).
- **State the trade-offs — what you deliberately won't do.** This is the part Claude omits and the part that creates focus. "We won't serve enterprise," "we won't build native fidelity first," IKEA won't pre-assemble. No trade-offs = no strategy.
- **Set 3–5 focus areas, max.** More than that spreads teams thin and executes nothing well. Focus areas flow from the segment/problem/differentiation choices.
- **Tie strategy to outcomes, and ground it in evidence.** Frame goals as outcomes ("increase retention 10%") not outputs ("launch a loyalty program"), and connect each to a metric. Build it on real customer insight and competitive/market analysis, with assumptions flagged for testing — don't strategize in a vacuum (defer the analysis and research to the skills named above).

### Set the stability rule

- **Stubborn on vision, flexible on strategy.** Vision should hold 3–5 years and survive bumps; strategy is reviewed (at least) quarterly and changes as you learn. Distinguish a **vision pivot** (the problem itself doesn't matter to customers — rare, serious: Burbn→Instagram) from a **discovery pivot** (a different path to the same destination — frequent, normal: change monetization, growth tactic, or feature focus).
- **Define change-criteria up front** so the call is evidence-based, not emotional: what validation signal would prove the *problem* doesn't matter (vision), and what metric/learning would prove the *approach* isn't working (strategy). Persisting too long wastes resources; pivoting too fast never lets a good idea prove itself — most teams give up too soon, not too late.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Applying every framework and every communication format at once is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Which strategy framework** | *Playing to Win* (5 cascading choices) for a full strategy; *Porter's Five Forces* for industry attractiveness/defense; *Blue Ocean* to create uncontested space; *Kano* to classify must-have/performance/delighter features; *Three Horizons* to balance now/next/future; *Product Strategy Canvas* to capture it all on one page | Running all of them as ritual — "framework theater" that buries the actual choices | Pick the 1–2 that answer the question; Product Strategy Canvas as the documenting container |
| **Vision communication format** | Written statement as the foundation; story/storyboard to make the user journey tangible; video for all-hands/investor emotional pitch; visiontype (idealized prototype) to show a 3–5-yr future when teams need a concrete north star | Using one format for every audience, or polishing a video before the statement is even clear | Start with the concise written statement, then adapt to the audience; reinforce the same core message across formats |
| **Vision statement form** | Template — "For [target] who [need], [product] is a [category] that [benefit]. Unlike [alternative], we [differentiation]." — when you want rigor and comparability | Forcing the template when a one-line narrative ("entertain the world") lands harder | Draft with the template to force completeness, then cut to the most memorable phrasing |
| **Single vs. multi-product laddering** | Single-product: vision ≈ company vision, keep them tight | Multi-product: each product needs its own vision/strategy that ladders up without overlapping siblings; watch for products competing for the same users | Make the product↔company link explicit either way; define clear product boundaries in a portfolio |
| **B2B vs. B2C emphasis** | B2B: multi-stakeholder value, champions, integration/security/scalability, longer validation | B2C: individual decision-maker, viral/network effects, fast iteration | Match the strategic emphasis to the buyer reality; don't apply a B2C playbook to an enterprise product |
| **New vs. existing/pivot inputs** | New: market reports, competitor scan, problem interviews, small group (6–8), workshop or week-long sprint | Existing/pivot: usage analytics, feedback patterns, broader cross-functional stakeholders | Match inputs and the group to the stage; keep the core vision group ≤8 for decisiveness |
| **Depth — full doc vs. summary** | Full strategy doc (segments, value prop, differentiation, focus, trade-offs, metrics, rough timeline) for alignment; 2–3-sentence summary for daily internalization | Producing a long document nobody reads, or a one-liner with no rationale | Write both: the short version teams remember + the detailed version with reasoning and assumptions |

A few contexts flip several defaults at once: a **multi-product B2B company** needs portfolio laddering *and* multi-stakeholder strategy *and* a documented full strategy; a **pre-PMF startup** wants a tight written vision, one segment, one differentiation bet, and a lightweight strategy it expects to pivot.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising the vision/strategy, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)** — strategy is bets; the other two are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — strategy rests on bets about market demand, the target segment's problem, and the durability of the differentiation: are those load-bearing assumptions evidenced or asserted? Flag the riskiest for testing.
- **`pm-okr-metric-validity-audit`** *(offer — if it names metrics)* — the success metrics, KPIs, and North Star: valid outcome measures tied to the strategy, or vanity/output metrics? (Build the OKR/KPI artifacts themselves with `pm-okrs-kpis`.)
- **`pm-prioritization-rigor-audit`** *(offer — if it sets themes/focus areas)* — the 3–5 focus areas are prioritization choices that decide what gets built: evidence-based and traceable, or a feature-factory wish list / HiPPO pick? (Run the prioritization decision itself through `pm-prioritization`.)

**Composition (per `docs/orchestration-policy.md` §9):** this artifact sits high on the PM ladder and mostly **feeds from** upstream inputs and **feeds into** downstream artifacts rather than building them — the **competitive analysis** (`pm-competitive-analysis`), **problem** (`pm-problem-statement`), and **discovery** (`pm-discovery`) are upstream inputs; the **roadmap** (`pm-roadmap`), **OKRs** (`pm-okrs-kpis`), and **pricing/GTM** (`ux-pricing`, `pm-gtm-plan`) are downstream (offer to produce next, don't auto-generate). If the audits surface a conflict, resolve back toward the purpose: **a vision exists to guide and reject decisions, and a strategy exists to make focused trade-offs — if the vision can justify anything and the strategy says no to nothing, neither is done.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write a buzzword poster ("best-in-class, seamless, world-leading") | Name a specific, user-centric, memorable destination that can reject a feature |
| Treat vision, strategy, roadmap, mission as the same thing | Keep the hierarchy distinct and ladder product → company |
| Write "strategy" as a list of features to build | Make deliberate choices: where to play, how to win, what you won't do |
| Target "everyone" | Pick one primary segment by job/outcome, win it, then expand |
| Claim you're better at everything | Choose one differentiation path with a defensible barrier ("can't or won't") |
| Omit the trade-offs | State explicitly what you deliberately won't do — that's the focus |
| List 10 focus areas | Hold to 3–5; more spreads teams thin |
| Run every strategy framework as ritual | Pick the 1–2 that answer the question |
| Use one vision format for all audiences | Start with the written statement, adapt to the audience |
| Change the vision every quarter | Stubborn on vision (3–5 yrs); flexible on strategy (quarterly); know vision-pivot vs. discovery-pivot |
| Ship vision/strategy unchecked | Hand off to okr-metric-validity + prioritization-rigor + assumption-rigor |

---

## Source lessons (Uxcel)

- [What Is Product Vision?](https://uxcel.com/lessons/what-is-product-vision-146)
- [Defining the Product Vision](https://uxcel.com/lessons/defining-the-product-vision-044)
- [Communicating the Product Vision](https://uxcel.com/lessons/communicating-the-product-vision-099)
- [Your Product Vision and Strategy](https://uxcel.com/lessons/your-product-vision-and-strategy-291)
- [Context of Product Vision and Product Strategy](https://uxcel.com/lessons/context-of-product-vision-and-product-strategy-001)
- [Aligning Teams with Product Vision & Strategy](https://uxcel.com/lessons/aligning-teams-with-product-vision-strategy-572)
- [Lifetime of the Product Vision and Strategy](https://uxcel.com/lessons/lifetime-of-the-product-vision-and-strategy-789)
- [How to Build a Product Strategy](https://uxcel.com/lessons/how-to-build-a-product-strategy-738)
- [Building a Product Strategy](https://uxcel.com/lessons/building-a-product-strategy-012)
- [Defining the Product Strategy](https://uxcel.com/lessons/defining-the-product-strategy-212)
