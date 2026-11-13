---
name: ux-pricing
description: Design or critique a pricing page. Applies the always-true core (plan ordering, CTA clarity, ethics guardrail) and gates context-dependent levers (freemium, usage sliders, live chat, PPP pricing, charm vs. round numbers) with trade-offs. Trigger when designing pricing tiers, plan tables, monetization screens, or when a pricing page isn't converting.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Pricing Page Skill


## How this skill behaves (read first)

This is a **generative** skill, and pricing is the textbook case for **gating** rather than applying every best practice. The lessons offer many ways to make a pricing page stand out — badges, per-tier graphics, interactive sliders, charm pricing, anchoring, social proof. Apply them all at once and you get an overdesigned, cluttered, psychologically overwhelming page that *hurts* conversion and trust. So:

1. **Establish context** (Step 0) — pricing decisions hinge on it more than almost any other screen.
2. **Apply the always-true core** — the patterns correct for essentially every pricing page.
3. **Surface the context-dependent decisions** as a *menu* — present each with its trade-off and a recommendation, and let the user pick the few that fit. Stacking many of them is the failure mode.

Then **hand the result to the audit skills** to validate it didn't tip into clutter or dark patterns.

Scope & composition (per `docs/orchestration-policy.md` §9): this skill owns the **pricing page itself** and composes lower-scope skills rather than re-deriving them. **Core children (built as part of the page):** `ux-cards` (tier-card mechanics — shadows, padding, clickable card) and `ux-buttons` (the CTAs). **Downstream (offer, don't auto-build):** the post-click `ux-checkout-payment`. **Inherit, don't regenerate:** under an existing design system, take color/type/spacing from its tokens — only set those when designing from scratch.

---

## Step 0 — Establish context before designing

Pricing output changes sharply with these. Ask if unknown; state the assumption if proceeding.

- **Pricing model** — subscription, one-time, usage-based, freemium, or hybrid? Drives the billing toggle, free-tier triggers, and what a "plan" even is.
- **Positioning** — bargain/value vs. premium/enterprise? Drives charm vs. round pricing and how rich the visuals should be.
- **Market & deal size** — global (PPP?) vs. single-market; high-ticket/complex (sales-assisted) vs. low-ticket self-serve. Drives plan count, live support, "Talk to sales."
- **Business goal** — which plan do you want most users to land on? Drives emphasis (ethically).

---

## The always-apply core (correct for almost every pricing page)

**Plan table**

- **Show only the key differentiating features per tier** — lead each tier with what makes it distinct from the one below. Cut the long feature matrix; link to a full comparison instead. A wall of 30 checkmark rows raises cognitive load and stalls the decision.
- **Communicate the difference clearly** — state each tier's unique value at the top (e.g. "1 project / 3 projects / unlimited"), details below.
- **Meaningful, value-communicating plan names** — "Basic Website" / "E-commerce Powerhouse", not "Standard" / "Advanced". The name should tell users which plan is *for them*.
- **Keep it legible and low-clutter** — simple fonts, limited palette, generous spacing. Clarity is never sacrificed for decoration.

**Ordering & honesty**

- **Order cheap → expensive, left to right.** Users tend to choose the first option they see; order toward the plan that genuinely fits them, not the most expensive.
- Never reverse the order (expensive → cheap) to anchor high — it's a dark pattern that erodes trust (see ethics guardrail).

**CTAs**

- **One primary CTA per plan**, no competing actions in the card.
- **Specific, value-driven labels** — "Get Pro", "Choose Team", "Start Free Trial" — never "Buy Now" or "Submit".
- **Visible and clearly clickable**, not overlapping other elements; repeat at the bottom of long pages.

**Clarity & trust baseline**

- **Lead with outcomes/benefits before price** — what will users accomplish?
- **Address cost concerns** with an FAQ (billing cycle, cancellation, refunds, trial terms) — it reduces anxiety and last-minute drop-off.
- **Surface guarantees / free trials / "no credit card required"** prominently rather than in fine print.

---

## The context-dependent decisions (a menu — pick what fits, don't stack everything)

Present each with its trade-off and a recommendation tied to Step 0, and let the user choose. **Applying all of these at once is the overdesign failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Pricing model** (subscription / one-time / usage / freemium / hybrid) | Match to how value is delivered (ongoing → subscription; consumption → usage-based) | Forcing subscription on a one-time-value product | Pick from the value-delivery pattern, not habit |
| **Number of plans** | 2–4 is the sweet spot | More → decision paralysis; fewer if the product is simple | Start ~3, but user-test the count rather than defaulting |
| **Plan emphasis / "Most Popular" badge** | You have a clear best-fit or middle plan to guide toward | Emphasizing nothing (no guidance) *or* badging several (no signal) | Emphasize one — the best-fit or middle plan; validate with research |
| **Billing toggle (monthly / annual)** | You actually offer both | No annual option | If offered, make annual savings obvious ("Save 20%", "2 months free") |
| **Charm vs. round pricing** | Charm ($9.99) for value/bargain positioning; round ($100) for premium/enterprise | Mismatched to brand tier | Match to positioning from Step 0 |
| **Price anchoring** | Showing a higher tier first to frame value honestly | Inventing a fake "original" crossed-out price | Use real anchors only |
| **Freemium / free trial** | Free tier that demonstrates value with upgrade triggers at value-realization moments (storage, seats, features) | Arbitrary time limits; free tier with no paid path | Tie limits to success moments; always pair free with a paid option |
| **Bundling / packaging** | Combining offerings adds real value and simplifies choice | Bundling to obscure cost of weak items | Bundle to simplify, not to hide |
| **International / PPP pricing** | Global audience with very different purchasing power | Single-market product (adds needless complexity) | Adjust for PPP + show local currency when global |
| **Per-tier graphics / illustrations** | A visual genuinely clarifies a plan's character at a glance | Decoration that competes with the comparison | Use sparingly; clarity first |
| **Interactive elements (seat sliders, usage estimators)** | Users self-select by seat count/usage and it aids the decision | Added for "engagement" on a simple 3-tier page | Only when they help users self-qualify |
| **Social proof (testimonials/logos near pricing)** | Space allows and proof addresses a real objection | Crowding the comparison; burying it below the FAQ | A focused, specific testimonial near the table beats many generic ones |
| **Live chat / phone support** | Complex or high-ticket products where buyers have questions | Simple low-ticket self-serve (use an inline help link) | Match support channel to deal complexity |

> The table is a menu, not a checklist. The more of these you switch on at once, the closer you get to the overwhelming, manipulative-feeling page this gating exists to prevent. Choose the few the Step 0 context justifies.

---

## Ethics guardrail (lines a pricing page must not cross)

Pricing is where dark patterns concentrate. Never:

- **Reverse-order plans** (expensive → cheap) to anchor high.
- **Fake anchors** — a crossed-out "original" price that was never real.
- **Hidden fees** — revealing per-seat charges, overages, or required add-ons only at checkout.
- **Urgency theater** — fake countdowns or "only 2 left" on unlimited digital products.
- **Confirmshaming** on downgrade/cancel ("No thanks, I don't want to save money") — use neutral dismissals.

A short-term conversion bump here costs long-term trust. The `ux-dark-patterns-audit` skill checks this systematically.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After generating or revising, hand the result to the audit lenses rather than declaring it done. These are **candidate** lenses — posture is set by `docs/orchestration-policy.md`, or route the whole page through `ux-design-review`. Here, **`dark-patterns`, `heuristics`, and `microcopy` are Tier A (auto-run); `aesthetics` is Tier B (offered, and suppressed under an existing design system)**. If the user invoked this skill for one specific thing, respect that scope — don't pull in the rest.

- **`ux-dark-patterns-audit`** *(Tier A)* — validates the ethics guardrail above (reverse ordering, fake anchors, hidden fees, urgency theater, confirmshaming).
- **`ux-heuristics-audit`** *(Tier A)* — usability failure modes: consistency, recognition (clear tier differences), visibility (CTA states).
- **`ux-microcopy-audit`** *(Tier A)* — plan names, value lines, and CTA wording carry the decision; vague labels ("Standard"/"Advanced") stall it.
- **`ux-aesthetics-audit`** *(Tier B — offer; suppress under a design system)* — the overdesign check this skill most needs: did the gated levers (badges, per-tier graphics, sliders, heavy social proof) create clutter or competing focal points, and is the recommended plan still the clear focal point?

If the audits flag clutter, resolve back toward the primary task: helping the user compare plans and choose. Pull the optional levers back out until clarity returns.

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| List every feature in every tier | Show key differentiators; link to a full comparison |
| Name plans "Basic / Standard / Premium" | Name by who they're for: "Solo / Team / Agency" |
| Order plans expensive → cheap to anchor high | Order cheap → expensive, toward the best-fit plan |
| "Buy Now" / "Subscribe" / one CTA for all plans | One distinct, value-driven CTA per plan ("Get Team") |
| Badge several plans "Most Popular" | Emphasize exactly one, chosen from Step 0 |
| Stack badges + graphics + sliders + heavy social proof | Pick the few levers the context justifies |
| Charm-price a premium/enterprise brand | Match pricing style to positioning |
| Hide annual savings or true costs | Show savings prominently; no hidden fees |
| Reverse ordering / fake "original" prices / fake urgency | Stay within the ethics guardrail |
| Ship without checking | Hand off to the heuristics audit |

---

## Source lessons (Uxcel)

- [Best Practices for Designing Pricing Pages](https://uxcel.com/lessons/pricing-best-practices-494)
- [Pricing & Monetization Strategies](https://uxcel.com/lessons/pricing-monetization-strategies-045)
- [Writing Action-Based Messages](https://uxcel.com/lessons/action-based-messages-095)
