---
name: ux-design-tips
description: Use when asked for UX strategy or behavior guidance on landing pages, onboarding, pricing, CTAs, social proof, personalization, login, permissions, or brand memorability.
---

# UX Design Tips

## Overview
Provide goal-based UX tips derived from uidesign.tips/ux-tips. Prioritize actionable guidance, map to a single primary goal, and keep each tip unique.

**Scope:** This skill targets UX strategy and behavior. For visual layout or component-level UI critique, use `ui-design-tips`.

## Workflow
1. Read references/ux-tips.txt.
2. Confirm the Tip Index has 27 tips; if not, revisit the source before answering.
3. Identify the user's primary goal: trust, value, action, friction, or brand.
4. Select 3-7 tips from that goal; optionally add 1 cross-goal tip as "Also consider".
5. Translate each tip into concrete actions for the user's context (product stage, audience, surface).
6. If the user requests a complete checklist, return all tips grouped by goal in the same order as the reference file.

## Output Pattern
- Start with a one-line goal statement that mirrors the user's intent.
- Provide short bullets: Tip name -> action -> where to apply.
- Avoid quoting the original copy; paraphrase into actionable steps.
- Keep guidance specific and testable (what to change, where, why).

## Example
User: "Our pricing page converts poorly. What should we change?"
Answer:
Goal: Show value and reduce hesitation on the pricing decision.
- Distinguish Pricing Plans -> Use distinct plan icons and labels so each tier has a clear persona; apply in the plan cards.
- Better Pricing Plans -> Add a visual indicator that highlights the recommended plan and its outcome; apply next to the price.
- Use More Numbers -> Add specific outcome metrics (not rounded) to each plan; apply under the plan description.
- Show Product Value with Visuals -> Add a small screenshot that previews what the plan unlocks; apply near the plan CTA.
- Also consider: Leverage Social Proof -> Add a short logo row or quote near the pricing grid.

## Quick Reference
- Trust: numbers, social proof, testimonials at signup, permission transparency, relatable faces.
- Value: calculators, product visuals, before/after, realistic mockups, CTA-adjacent previews, pricing plan differentiation, localization.
- Action: CTA copy, red for destructive actions, gaze direction, preview/blur for curiosity, segmented header CTAs.
- Friction: social auth primary, easy migration, login screen value reinforcement.
- Brand: mascots/branding, cute characters, uniqueness, humor, easter eggs.

## Common Mistakes
- Mixing multiple goals without naming a primary goal.
- Repeating the same tip across categories instead of cross-referencing.
- Giving generic advice without specifying UI surface or placement.
- Using red for primary success CTAs instead of destructive actions.
- Adding personalization that feels creepy or uses irrelevant data.

## Resources
- references/ux-tips.txt: Full tip list and goal-based grouping.
