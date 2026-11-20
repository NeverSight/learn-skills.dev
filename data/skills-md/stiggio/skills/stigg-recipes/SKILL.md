---
name: stigg-recipes
description: Use when implementing a complete end-to-end Stigg workflow that spans multiple skills — freemium, hybrid pricing, AI-credits monetization, in-app upgrade flows with checkout, trials with addons. Triggers include "implement freemium", "monetize AI tokens end-to-end", "set up hybrid pricing", "add a checkout experience", "trial with addons while on a paid plan", "run a payment-link signup", "complete Stigg integration for [scenario]". Skip for single-skill tasks — go straight to the relevant pillar skill.
---

# Stigg Recipes — Composed End-to-End Workflows

Each recipe in this skill ties together multiple pillar skills (`stigg-pricing-modeling`, `stigg-entitlements`, `stigg-subscriptions`, `stigg-credits`, `stigg-widgets`, `stigg-api`) into a complete flow. **Recipes don't duplicate content** — they orchestrate references.

## Before You Start

Per the umbrella `stigg` skill: **search first.** Recipes go stale faster than pillar skills since they integrate multiple surfaces. Confirm each step against live docs as you go.

## Index of Recipes

| Recipe | Reference |
|---|---|
| Implement a **freemium** model end-to-end | `references/freemium.md` |
| **Freemium with paid usage** after quota (the OpenAI-API archetype: 1k free, $X/unit after) | `references/freemium-with-paid-usage.md` |
| Add an **in-app checkout** experience | `references/checkout.md` |
| Configure **hybrid pricing** (flat + per-unit + usage) | `references/hybrid-pricing.md` |
| **Monetize an AI product with credits** end-to-end | `references/credits-monetization.md` |
| Run a **trial on add-ons** while keeping the paid plan active | `references/trial-with-addons.md` |
| Subscribe customers via a **payment link** | `references/payment-link.md` |

Each recipe lists the steps, names the pillar skill that owns each step, and surfaces the gotchas that only show up when the pieces compose.

## How Recipes Should Be Used

A recipe is a **map**, not a manual. It tells you:

1. The **shape** of the end-to-end flow (which Stigg surfaces touch what).
2. The **order** of operations (catalog → entitlements → subscriptions → UI).
3. The **gotchas** that show up only at the seams between skills.

For each step, the recipe **points at the pillar skill** that owns the implementation detail. Don't expect to find SDK init signatures or charge-config mechanics here — those live in the pillar skills.

> Use a recipe to guard against partial implementations — modeling a Pro plan but forgetting the Free plan, the gating, the paywall, or the upgrade flow. Walk every step.

## When NOT to Use This Skill

- Single-skill tasks: provisioning a customer (`stigg-subscriptions`), gating one feature (`stigg-entitlements`), creating a credit currency (`stigg-credits`).
- Pricing strategy / model selection — that's `stigg-pricing-expert`. Recipes assume the model is chosen.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating a recipe as an exhaustive guide | Recipes are skeletons; pillar skills carry the meat. Follow the cross-references. |
| Implementing the "modeling" steps but skipping the UI / entitlement-check parts | The flow isn't done until customers can experience it. Walk every step. |
| Authoring a fresh recipe inline instead of using one of the existing ones | If the user's request maps to a recipe, use it. Improvising a worse version doesn't help. |
| Using a recipe for a single-skill task | Overkill. Go to the pillar skill directly. |
| Skipping the "verify in production" step at the end of each recipe | An untested recipe is a bug magnet. Always exercise the flow end-to-end before declaring it done. |
