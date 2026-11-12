---
name: brainstorming-game-ideas
description: Use when the user wants new mobile or web game ideas, concepts to build next, ways to cash in on a trend, a reskin or twist on a hit game, or ideas that fit a small budget and team.
---

# Brainstorming Game Ideas

Generate many ideas privately, cut most of them, and present **the top 3** as idea cards a builder can act on.

**REQUIRED BACKGROUND:** `using-game-trend-skills`. **Scoring:** use `evaluating-game-ideas/scoring-rubric.md` (in the `evaluating-game-ideas` skill).

## Inputs (get these first)

- **Creator profile.** If none exists and the user hasn't stated constraints, ask **one** question covering budget, team/engine and target platforms, then create the profile.
- **Fresh market context.** You need an insight report from the last 30 days. If there isn't one, run `scanning-game-trends` first, or at least do a short live pass on the trending lists and rising mechanics.
- **Seeds from the user** (optional): a theme, a mechanic they love, an unfinished game to rework.

## Generate (privately, ≥ 12 ideas)

Combine across these axes:

| Axis | Pull from |
|---|---|
| **Mechanic** | Emerging or rising mechanics from the report. Classic puzzles with proven retention (logic grids, sort, flow, merge). |
| **Theme** | Fresh, cute or funny, readable at thumbnail size. Original characters. Seasonal or local twists that still work globally. |
| **Social hook** | Results from `scouting-social-trends`: the verb and payoff, a shareable output (result card, timelapse, daily challenge). |
| **Automation lever** | How agents can make the content: procedural levels with a solver, image-to-level pipelines, generated variants. |
| **Monetization hook** | Natural rewarded moments (retry, +slot, hint, booster) and an IAP reason (no-ads, packs, meta collection). |

Also include at least 2 **"twist on a current riser"** ideas and 1 **"smallest possible"** idea (shippable in about 1 week, mainly to exercise the release pipeline).

## Cut

1. Drop anything that fails a hard gate in `evaluating-game-ideas`: third-party IP, over budget or skills, build time longer than the trend window, saturated with no visible twist.
2. Score the rest with the rubric. Keep the top 3 by total. Break ties with **Simplicity**, then **Content cost**.
3. Make sure the three are different from each other: different mechanics or a different risk profile. Don't present three reskins of one idea.

## Present

Start with a one-line comparison table (idea × 7 scores × total). Then give one card per idea using `idea-card-template.md`. Save the set as `reports/YYYY-MM-DD-ideas.md`.

End with a recommendation, **which one to build first and why**, then ask one question: which idea to take to `evaluating-game-ideas` in depth or straight to `writing-game-agent-briefs`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Listing 10 ideas | Present 3. The rest stay private. |
| "Why now" without evidence | Cite the trending title, chart move or report behind it. |
| Ideas that need content the creator can't produce | Every card names its automation lever, or explains why content is cheap. |
| Copying a hit 1:1 | Give each idea a twist that a muted 3-second clip can show, and say what you'd keep vs change. |
| Forgetting monetization until the end | Rewarded moments are designed into the core loop on the card. |
