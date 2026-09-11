---
name: think-random-frameworks
description: Generates three off-pattern framework analyses of a topic by drawing frameworks at random, applying each regardless of fit, and harvesting the non-obvious angles the unexpected lenses expose. Use when a framing feels frozen or fixated and the goal is to break out of it with deliberately unranked methods rather than the obvious best-fit ones. Use when relevance-ranked selection would only reinforce the stuck view and a random draw is wanted to surface what a fitted analysis would miss.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.random-frameworks
  family: meta-thinking-and-reflection
  evidence-tier: "C"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Random Frameworks

When a framing is stuck, the frameworks you would naturally reach for tend to reinforce the stuck view. This skill does the opposite: it draws three frameworks at random from the library, ignoring fit on purpose, and applies each to your topic to force lenses the situation would never summon. The value is exactly what relevance ranking suppresses. The deliberate randomness, the same logic as a random-stimulus creativity move, dislodges a frozen framing and surfaces angles a fitted analysis would miss.

## When to Use

- A framing feels frozen or fixated, and the obvious frameworks would only confirm it.
- You want off-pattern lenses to surface non-obvious angles, not the best-fit analysis.
- You are exploring, early, and want breadth and surprise over precision.

## When NOT to Use

- **You actually want the right frameworks for a real, stakes-bearing decision.** Use `think-framework-advisor` (it routes to the fewest fitting moves) or `think-top3` (it ranks and applies the most relevant three). Applying three ill-fitting frameworks to a high-stakes, irreversible call is worse than noise.
- **You are not stuck or fixated.** With no frozen framing to dislodge, a random draw is overhead; route to a fit-first path.
- **A single random-stimulus move would do.** Use `think-far-analogy-ideation` (the library's home for random stimulus); this skill is the meta-rotation of three whole frameworks, not one stimulus. For flipping a single default premise, use `think-assumption-reversal`.
- **You want a structured rotation of fixed lenses within one method** (facts, upside, risk, intuition, alternatives, process). That is `think-parallel-perspectives-review`, which rotates a curated lens set inside one method; this skill draws whole different frameworks at random.
- **Not a thinking task** (lookup, drafting, coding): redirect.

## Instructions

When asked to apply random frameworks to a topic, follow these steps:

1. **Parse the topic.** Restate the situation in one or two sentences. If the input is under about 15 words or carries no concrete signal, ask one clarifying question, then proceed.
2. **Run the shared engine in RANDOM mode.** Follow `references/engine.md`: read the corpus, draw three frameworks uniformly at random without replacement (seeded only if the user supplies a seed), and apply each to the topic so it emits that framework's real artifact, flagging poor structural fit rather than swapping it out.
3. **Harvest the surprises.** Name the one to three non-obvious angles the random draw exposed that an obvious analysis would have missed. State plainly that the set is a fixation-breaker, not a fitted recommendation.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the three randomly drawn frameworks (with the seed or fresh-draw noted), the three filled artifacts, and the harvest of non-obvious angles, not a prose essay and not a recommendation to act.

## Quality Checklist

Before finalizing, verify:

- [ ] Exactly three frameworks, drawn at random (seed or fresh draw stated), each name existing in the recommendable corpus.
- [ ] Selection ignored relevance on purpose; frameworks were not quietly fitted to the topic.
- [ ] Each framework was applied, emitting its real artifact; poor structural fit was flagged, not swapped out.
- [ ] The harvest names the non-obvious angles the draw exposed and does not present the set as a fitted recommendation.
- [ ] No tier inflation; the random set carries no decision authority.

## Evidence

Tier **C** (conceptually plausible, under-tested). Random-stimulus and forced-connection moves are a recognized creativity practice for breaking fixation, but the meta-rotation of three whole frameworks at random is not measured, in humans or in AI use. Treat the output as a fixation-breaker, never as a fitted analysis. Full grading and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed run that draws, applies, and harvests three random frameworks on a real topic.
