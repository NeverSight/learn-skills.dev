---
name: think-backcasting
description: Produces a backcast path by fixing a vivid desired future state and reasoning backward through the milestones and preconditions required to reach it, ending at the next concrete step available now. Use when planning toward a transformative or long-horizon goal that forward planning anchors too low, when a chosen future needs a route mapped back to today, or when milestones and dependencies between now and the goal must be made explicit.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.backcasting
  family: risk-and-resilience
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Backcasting

Forward planning anchors on today's constraints and tends to extrapolate the status quo. Backcasting reverses the direction: it fixes a vivid, concrete *desired future state* first, then reasons backward to the milestones and preconditions that must be true for that future to exist, link by link, until it reaches the next concrete step available now. The reversal is what does the work - it decouples the goal from present limits, forces each milestone to name what had to be true just before it, and connects an aspirational future to something executable today. The output is a **backcast path**, not a discussion. This is a route to a chosen success, not a forecast and not a test of whether the goal is right.

## When to Use

- Planning toward a transformative or longer-horizon goal where forward planning anchors too low and just extrapolates the present.
- A desired future has been chosen and needs a route mapped backward to the next step today.
- The milestones, dependencies, and sequencing between now and the goal need to be made explicit.
- The desired end state can be described concretely (you can say what is true once you have succeeded).

## When NOT to Use

- **Near-term, simple plans.** When the path is short and obvious, forward planning is sufficient and the backward overhead buys nothing.
- **When the goal is unsettled or unvalidated.** Backcasting assumes the endpoint; it does not choose or test it. Settle the goal first with a decision or option-evaluation skill. A clean path to the wrong goal is worse than no path.
- **To imagine how the plan could fail.** That is a premortem (work back from *failure* to causes). Backcasting works back from *success* to the *path*.
- **To trace forward consequences of a decision.** That is a futures wheel (first/second/third-order effects radiating outward), not a goal-first backward route.
- **For personal follow-through on an already-chosen goal.** That is WOOP (an if-then plan for one actor's intention-action gap), not a route to a future.

## Instructions

When asked to backcast, follow these steps:

1. **Fix the desired future state, vividly.** Describe success as if it already exists, in the definite present: "It is [horizon]. The following is true: ..." Make it concrete and observable, not "things are better." If the goal is unsettled or unvalidated, say so and stop - choose the goal first.
2. **Name the success conditions.** List what is demonstrably true in that future (capabilities, metrics, states, relationships). These are the things the path must arrive at.
3. **Step backward one milestone at a time.** Starting from the future, ask "what had to be true just before this for it to happen?" Record each milestone and, for each, its **preconditions** - the capability, decision, resource, or dependency that had to be in place first. Continue backward toward the present. Do not switch into forward order.
4. **Check the chain for gaps and ordering.** Verify each milestone's preconditions are themselves produced by an earlier milestone or already exist today. Surface missing links and dependencies between branches; a dangling precondition is a gap to fill, not to hide.
5. **Land on the next concrete step.** The final (earliest) link must be an action that can be taken now. This connection from vision to next move is mandatory; a future with milestones but no executable first step is not a backcast.
6. **Emit the backcast path and a short summary.** Produce the artifact in `references/TEMPLATE.md`: a one-paragraph summary naming the future and the single most important near-term move, above the ordered milestone chain with preconditions.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled backcast path (future state, backward milestone chain with preconditions, next concrete step) plus its summary, not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The desired future is stated vividly and concretely as an already-true state with a horizon, not a vague aspiration.
- [ ] The chain is built *backward* from the future, and each milestone names the preconditions that had to be true before it (not a forward to-do list relabeled).
- [ ] Preconditions and dependencies are checked for gaps and ordering; dangling links are surfaced, not hidden.
- [ ] The earliest link is a concrete next step that can be taken now.
- [ ] The output is the backcast-path artifact, not prose.
- [ ] No overclaiming: the path is a constructed route to a *chosen* future, not a forecast, not proof the goal is right, and not a guarantee of the outcome (see `evidence/dossier.md`).

## Evidence

Tier **P** (practitioner). Backcasting is a well-documented, widely adopted foresight and sustainability-planning method (Robinson 1982, 1990; Dreborg 1996; The Natural Step), valued for reframing planning around a desired endpoint and surfacing the preconditions a forward extrapolation would miss. Its validation is qualitative and case-based; there is **no strong controlled evidence** that it improves goals or outcomes, it does **not** validate whether the chosen future is right, and the backward chain is a structured hypothesis, not a forecast. The evidence is transferred from human practice, not AI-validated. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed backcast path on a real decision.
