---
name: pm-competitive-analysis
description: Produce or critique a competitive/market analysis that yields a strategic edge — not a flat feature table. Scopes to a research objective and industry context, finds direct/indirect/potential competitors, profiles them from honest public sources, applies the right framework (perceptual map, feature matrix, SWOT, Porter's, TAM/SAM/SOM), and ends with strategic implications and a positioning conclusion. Applies the always-true core and gates context-dependent decisions (which framework, primary vs. secondary research, competitor depth, positioning stance, expansion, AI's role). Trigger when asked to analyze competitors, do a competitive/market analysis, map a competitive landscape, build a feature-comparison or SWOT, size a market, or decide how to position/differentiate against rivals.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Competitive Analysis Skill

## How this skill behaves (read first)

This is a **generative** skill, and "do a competitive analysis" is where an AI assistant produces the most confident, least useful output: a flat feature-comparison table of the few obvious direct competitors, with invented specifics, no market context, no gaps identified, and no "so what." Two failure modes compound it — **fabricated competitor facts** (made-up features, pricing, or market share that read as authoritative) and **no strategic conclusion** (a report that lists but never decides). A real competitive analysis is **scoped to a decision, grounded in honest public evidence, structured by the right framework, and ends in implications and a positioning choice**. So this skill gates:

1. **Establish the research objective and the industry context** — what decision this informs, and the market it sits in, so competitor moves are read in context rather than in a vacuum.
2. **Apply the always-true core** — find all three competitor types, profile from real public sources, use the right framework, prioritize, and translate into strategic implications and a position.
3. **Surface the context-dependent decisions** (which framework, primary vs. secondary research, competitor depth, positioning stance, expansion, AI's role) with trade-offs.

Then it **hands off to `pm-assumption-rigor-audit`** (are the competitor facts, market-size estimates, and "gap exists" claims evidenced or assumed/hallucinated?) and **`pm-prioritization-rigor-audit`** (when it ranks opportunities or competitor tiers).

Scope: this skill owns the **competitive/market analysis and the positioning conclusion that follows from it**. It defers full **product strategy** to `pm-vision-strategy`, **pricing strategy** to `ux-pricing`, **go-to-market / market-entry timing** to `pm-gtm-plan`, the broader **research process and ethics** to `pm-discovery`, and **problem framing** to `pm-problem-statement`.

---

## Step 0 — Establish context before analyzing

Ask if not known; state the assumption if proceeding without an answer:

- **What decision does this inform?** Set specific research objectives tied to a decision ("which competitor features drive acquisition?") rather than "understand competitors." The objective scopes the work and prevents an endless, unfocused scan.
- **What's the industry context?** Sketch the overview first — market size and growth (TAM/SAM/SOM), key trends and drivers, regulatory/economic environment, and structural shifts (new entrants, substitutes). A rival losing share in a shrinking segment faces different pressures than one in a growing market; context changes the meaning of every move.
- **Who are the real competitors?** Not just the obvious direct rivals — also indirect (same need, different approach) and potential/aspirational ones. Surface them by asking customers what they considered, following where capital flows, monitoring industry news, and searching like a customer would.
- **What's the stage and resource budget?** This sets how much primary vs. secondary research, and how deep the analysis goes.

---

## The always-apply core (true for any competitive analysis)

- **Frame the industry before benchmarking rivals.** Lead with market size, trends, regulatory forces, and structural changes so individual competitor insights are interpreted in context, not as isolated comparisons.
- **Cover all three competitor types.** **Direct** (similar product, same customers), **indirect** (same need, different solution — Uber vs. public transport), and **potential/aspirational** (could enter, or set a benchmark worth learning from). Listing only direct rivals is the most common blind spot.
- **Profile systematically, and mine real customer reviews.** For each competitor capture features, pricing, UX, and how they position themselves (speed? quality? community?). Reviews are the richest signal: analyze *patterns* — a complaint echoed across dozens of reviews is a structural weakness; recurring praise is a strength you'll have to match or beat.
- **Use the right framework for the question — not all of them.** Perceptual/landscape **map** (2×2 on dimensions customers care about) to find white space; **feature/competitive matrix** to compare capabilities and separate *table-stakes* (everyone must have) from *differentiators* (what actually drives choice); **SWOT** to assess your position (the value is in the intersections — a strength that meets an opportunity — not the four lists); **Porter's 5 Forces** for industry profitability; **TAM/SAM/SOM** for whether the market is worth pursuing.
- **Prioritize competitors into tiers.** Primary (closest match, directly affects you), secondary (partial overlap), tertiary (could become relevant). Spend strategic energy on the primary tier rather than spreading thin across everyone.
- **Gather intelligence honestly, from public sources.** Public reviews, case studies, marketing materials, free-tier features, conferences, and honest conversations are legitimate. Fake accounts, misrepresenting identity, and ToS-violating scrapers are not. And — critically for an AI — **do not invent competitor facts**: every feature, price, and share figure must trace to a real source, or be flagged as unverified. The purpose is to understand and differentiate, not to copy or find ways to mislead.
- **End with strategic implications and a position — the "so what."** Translate findings at three levels: *feature* (where to match the standard, where to differentiate), *positioning* (which narratives are overcrowded, where you can own a distinct claim), and *strategic* (which moves need an immediate response vs. which are long-term trends to prepare for). Then land a clear position: pick **one** of cheapest / highest-quality / most-specialized (claiming two creates mixed signals that erode trust), tie it to a specific persona-problem-promise, and — for early stage — win a focused niche before expanding, one dimension at a time.

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Running every framework, or analyzing every competitor equally, is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Which framework** | Perceptual map to find white space; feature matrix to compare capabilities; SWOT for your position vs. a key rival; Porter's for industry attractiveness; TAM/SAM/SOM for market worth | Running all of them as ritual ("framework theater") that buries the insight | Pick 1–2 that answer the objective; always include the table-stakes vs. differentiator cut |
| **Primary vs. secondary research** | Secondary (reports, reviews, public data) first for breadth and speed; primary (interviews, surveys, focus groups) to fill specific gaps | Spending on primary research for questions public data already answers | Secondary to frame the landscape, targeted primary to validate the gaps that matter |
| **Competitor depth** | Tier them — deep on primary, lighter on secondary, monitor tertiary | Analyzing dozens equally (thin everywhere) or fixating on one rival | Depth proportional to tier; revisit tiers as the market shifts |
| **Positioning stance** | Cheapest, highest-quality, or most-specialized — the one your cost structure and strengths can actually sustain | Claiming two at once (premium + cheap, broad + specialized) — customers disbelieve at least one | Specialized/focused for early stage; one defensible stance, consistent across touchpoints |
| **Expansion direction** (if scope includes growth) | One dimension at a time — geography, customer size, or product line — matched to current strengths | Expanding multiple dimensions at once, or before winning the initial niche | Win the niche first; expand the single dimension your proven strengths support |
| **AI's role** | AI to draft landscapes, matrices, SWOTs, and positioning *from data you provide or will verify* | Trusting AI-generated competitor "facts" (hallucinated features, pricing, share) | Use AI to structure and accelerate; verify every competitor claim against a public source |

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the grounding check, and the antidote to AI's biggest risk here: are the competitor facts, the market-size figures, and the "this gap exists / is worth $X" claims backed by real public evidence, or are they assumed, anecdotal, or fabricated? Flag every load-bearing claim that hasn't been verified.
- **`pm-prioritization-rigor-audit`** *(offer — if it ranks tiers or sets opportunity priorities)* — when the analysis ranks competitor tiers or scores market opportunities: is the ranking evidence-based and tied to the decision, or false-precision scoring and a HiPPO pick?

**Composition (per `docs/orchestration-policy.md` §9):** the analysis feeds downstream rather than auditing it. The **problem** (`pm-problem-statement`) is an upstream input; the **full strategy** (`pm-vision-strategy`) and **pricing** (`ux-pricing`) are downstream (offer to produce next, don't auto-generate). If the audits show the analysis rests on unverified competitor claims or a comparison with no conclusion, resolve toward the purpose: **a competitive analysis exists to make a sharper strategic choice — if it doesn't change a decision and isn't grounded in real evidence, it's a table, not an analysis.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| List only the obvious direct competitors | Cover direct + indirect + potential/aspirational |
| Invent competitor features, pricing, or market share | Ground every claim in a public source; flag the unverified |
| Benchmark rivals with no market context | Frame industry size, trends, and structural shifts first |
| Dump a flat feature checklist | Separate table-stakes from differentiators; map the white space |
| Treat the SWOT as four lists | Mine the intersections — strengths that meet opportunities, threats that hit weaknesses |
| Analyze every competitor equally | Tier them; spend depth on the primary tier |
| Use fake accounts / ToS-violating scrapers | Public reviews, case studies, free tiers, honest conversations |
| Claim "cheapest *and* best" | Pick one stance — cheapest, quality, or specialized — and keep it consistent |
| Stop at a report | End with feature/positioning/strategic implications and a clear position |
| Trust an AI-generated landscape as fact | Use AI to structure; verify each fact yourself |
| Ship the analysis unchecked | Hand off to assumption-rigor (+ prioritization-rigor) |

---

## Source lessons (Uxcel)

- [Market Analysis & Competition](https://uxcel.com/lessons/market-analysis-competition-568)
- [Competitive Analysis and Market Research](https://uxcel.com/lessons/competitive-analysis-and-market-research-294)
- [Market Research and Competitive Analysis](https://uxcel.com/lessons/market-research-and-competitive-analysis-943)
- [Market and Competitor Research](https://uxcel.com/lessons/market-and-competitor-research-638)
- [Positioning, Focus & Strategic Expansion](https://uxcel.com/lessons/positioning-focus-strategic-expansion-857)
- [Ethics in Product Discovery & Definition](https://uxcel.com/lessons/ethics-in-product-discovery-definition-871)
