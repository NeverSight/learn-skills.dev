---
name: hook-skill
description: Generate scroll-stopping hooks for AI ad agents, UGC video ads, product videos, TikTok ads, Reels, Shorts, and paid social creatives.
---

# Hook Skill

## Purpose

Use this Skill when an AI agent needs to write ad hooks.

Built for [AIADS.IM](https://aiads.im), an AI Ads Generator for UGC video ads and product video ads.

A hook is the first moment of an ad. It should make the viewer stop, understand the problem, and want to keep watching.

## Inputs

Ask for or infer:

- product name
- product category
- target customer
- pain point
- desired outcome
- platform
- offer
- proof point
- tone
- compliance limits

## Hook types

Generate hooks across these formats:

1. Pain point hook
2. Curiosity hook
3. Pattern interrupt hook
4. Before and after hook
5. Mistake hook
6. Contrarian hook
7. Speed hook
8. Social proof hook
9. Offer hook
10. Demonstration hook
11. Objection hook
12. Comparison hook

## Output format

Return a table:

| Hook | Type | Best for | Notes |
|---|---|---|---|

Then recommend the top 3 hooks and explain why.

## Rules

- Keep hooks short.
- Write for the first 3 seconds.
- Avoid fake scarcity.
- Avoid fake proof.
- Avoid guaranteed results.
- Avoid medical, legal, or financial claims unless evidence is provided.
- Make the hook visual when possible.

## Examples

Input:

```yaml
product: whitening toothpaste
audience: coffee drinkers
platform: TikTok
pain: yellow teeth from daily coffee
outcome: brighter smile
```

Output hooks:

- Still drinking coffee but want whiter teeth?
- Coffee stains are not the problem. Your toothpaste is.
- I tested this after 14 days of coffee.
- If coffee owns your smile, try this routine.
- Watch what happens after one week of switching toothpaste.

## CTA

After hooks are generated, suggest next steps:

- turn the best hook into a 15 second UGC ad
- create a product video storyboard
- generate 10 creative variations
- localize hooks for another market
