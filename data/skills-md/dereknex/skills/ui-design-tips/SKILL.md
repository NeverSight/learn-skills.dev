---
name: ui-design-tips
description: Use when a user asks for UI design tips or quick critique about layout, hierarchy, CTAs, forms, navigation, cards, tooltips, charts, or confirmation patterns.
---

# UI Design Tips

## Overview

Provide concise, actionable UI advice using the curated tips dataset from uidesign.tips. Use the reference JSON to select and apply tips that match the user's context, then translate them into concrete design recommendations.

**Scope:** This skill focuses on UI layout and visual interaction patterns. For UX strategy, conversion psychology, onboarding flow, or pricing behavior, use `ux-design-tips`.

## Quick Start

1. Load `references/ui-design-tips.json`.
2. Identify the UI problem (CTA, layout, forms, navigation, hierarchy, cards, tooltips, charts, confirmation, notifications).
3. Select 3-7 relevant tips by category.
4. Convert each tip into a specific recommendation tailored to the user's UI.

## Selection Workflow

- Map the request to 1-2 categories.
- Prefer tips that address risk or clarity first (confirmation, hierarchy, CTA) before cosmetic tweaks.
- If two tips overlap, merge them into one recommendation.
- Keep output concise and prioritized.

## Quick Reference

| Scenario | Tips to consider |
| --- | --- |
| CTA unclear | Always Have A CTA; Pick The Correct Element; Use Better Link Button; Direct User Attention with Media; Highlight The Best Offer; How to Apply the Brand Color |
| Layout feels messy | Align Uneven Elements; Avoid Fullwidth Paragraphs; Visually Distinguish Elements; Visually Separate Elements |
| Visual hierarchy weak | The Gutenberg Principle; How To Enhance Hierarchy; Hack Visual Hierarchy |
| Forms unclear | Make Inputs Self-Explanatory; Use Labels Cleverly 1; Use Labels Cleverly 2 |
| Dangerous actions | Delete Modal; Validate Deletion; De-emphasize Dangerous Actions |
| Cards not obvious | Make Cards Look Clickable; Padding On Rounded Cards |
| Navigation/scroll | Design Better Menus; Prompt User to Scroll |
| Tooltips on mobile | Make Tooltips Responsive |
| Charts confusing | Choose Chart Types Carefully |
| Notifications | Inform Users Beforehand; User Hate Surprises |

## Example

User: "Our pricing page has three plans and conversions are low."

Response approach:
- Highlight the best plan visually.
- Ensure CTA is primary and high-contrast.
- Use brand color on CTA and key icons.

## Common Mistakes

- Listing too many tips without prioritization.
- Applying layout tips when the real issue is CTA or hierarchy.
- Ignoring overlaps (e.g., two alignment tips that say the same thing).

## Rationalization Table

| Excuse | Reality |
| --- | --- |
| "One generic tip is enough" | Users need 3-7 prioritized, contextual tips.
| "I do not need the dataset" | The skill is only useful when grounded in the curated tips.
| "Dump everything" | Overload reduces clarity and actionability.

## Red Flags

- You did not load `references/ui-design-tips.json`.
- You output tips without mapping to the user's context.
- You ignored critical-risk areas like confirmation or CTA.

## Resources

- `references/ui-design-tips.json`: Curated tip list and categories.
- Source: https://www.uidesign.tips/ui-tips
