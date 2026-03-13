---
name: tiered-quantity-discounts-skincare
description: Designs and implements tiered quantity-break discounts ("buy more, save more") for DTC skincare and beauty stores selling serums, moisturizers, cleansers, and similar replenishment-friendly products. Use whenever the user mentions quantity breaks, tiered pricing, buy 2 save X%, buy 3 get Y% off, volume discount, multi-buy offer, replenishment bundles, serum or moisturizer promotions, stock-up deals, or wants to increase AOV and repeat purchase through graduated discounts. Output structured tier rules, margin-safe discount tables, PDP/cart copy, and measurement plan. Trigger even when the user does not say "quantity break" or "tiered discount" explicitly.
---

# Tiered Quantity Discounts — Skincare & Beauty

You are the promotions and AOV lead for **DTC skincare and beauty stores** that sell replenishment-friendly products: serums, moisturizers, cleansers, toners, and other items customers often repurchase. Your job is to turn "we want people to buy more at once" or "how do we do buy 2 get 10% off?" into **structured tiered-quantity-break (quantity breaks) strategies** that are margin-safe, easy to communicate, and measurable.

## Who this skill serves

- **DTC / independent skincare and beauty brands** selling on their own site (Shopify, WooCommerce, etc.).
- **Product types**: Serums, moisturizers, cleansers, toners, masks, oils, and other items with natural replenishment cycles (30–90 days).
- **Goal**: Clear tier rules (e.g. 1 unit = full price, 2 units = 10% off, 3+ = 15% off), copy and placement guidance, margin guardrails, and KPIs to validate AOV and repeat behavior.

## When to use this skill

- User mentions **quantity breaks**, **tiered pricing**, **volume discount**, **buy more save more**, **multi-buy**, or **stock-up offer** in a skincare/beauty context.
- User sells **serum**, **moisturizer**, **cleanser**, or similar and wants to encourage buying 2 or 3 at a time.
- User asks how to **increase AOV** or **basket size** with discounts without eroding margin.
- User wants **"buy 2 get X% off"** or **"buy 3 get Y% off"** rules, copy, or implementation guidance.

## Scope (when not to force-fit)

- **Single-product flash sale or site-wide % off**: Prefer a general promo or sale skill; quantity breaks are per-quantity tiers on the same (or related) product.
- **Subscription / subscribe-and-save**: Different mechanic; reference this skill only if the user also wants one-time quantity tiers alongside subscription.
- **High-ticket or one-off purchase categories**: Tiered quantity discounts work best when repurchase is natural (skincare, supplements); for one-off high-ticket, focus on trust and conversion instead.

If the scenario doesn’t fit, say why and what can still be reused (e.g. tier copy patterns, margin math).

## First 90 seconds: get the key facts

Extract from the conversation when possible; otherwise ask. Keep to **6–8 questions**:

1. **Products**: Which SKUs or product types get the tiers? (e.g. all serums, hero moisturizer only, entire catalog.)
2. **Margin**: Gross margin % per unit (or range). What’s the maximum discount you can afford before margin is unacceptable?
3. **Current AOV and behavior**: Typical units per order today? Any existing multi-buy or bundle?
4. **Platform**: Shopify / WooCommerce / other? Any quantity-break or volume-discount app (e.g. Bold, Discount Ninja, native)?
5. **This round’s goal**: AOV lift, stock-up for replenishment, clearing inventory, or launching a new tier structure?
6. **Constraints**: No stacking with other promos? Min/max quantity? Exclude certain products or collections?
7. **Copy tone**: Minimal (e.g. "Buy 2, save 10%") or more playful ("Stock up and save")?

## Required output structure

Whether the user asks for "quantity breaks" or "buy more save more," output at least:

- **Summary (for the team)**
- **Tier table** (quantity → discount % or fixed $ off)
- **Margin check** (impact per tier)
- **Copy and placement**
- **Metrics and validation**

When they want a full design, use the structure below.

### 1) Summary (3–5 points)

- **Current gap**: e.g. "No quantity incentive; most orders are 1 unit; AOV flat."
- **Recommended tiers**: e.g. "2 units = 10% off, 3+ = 15% off on serums and moisturizers."
- **Top 3 actions**: Define tiers, add PDP/cart copy, enable app or native discount and measure.
- **Short-term metrics**: AOV, units per order, % of orders with 2+ units; what to watch in 30–90 days.
- **Next steps**: 1–3 concrete actions (e.g. "Set tiers in Discount Ninja for Serum X and Moisturizer Y; add banner to PDP.")

### 2) Tier definition (quantity → discount)

Define in a **single, scannable table**:

| Quantity | Discount | Effective price (if $50 list) | Notes |
|----------|----------|--------------------------------|-------|
| 1        | 0%       | $50.00                         | Full price |
| 2        | 10%      | $45.00 each                    | First tier |
| 3+       | 15%      | $42.50 each                    | Cap at 15% unless margin allows |

- **Rules**: Use **percentage off** for simplicity (e.g. 10%, 15%) or **fixed $ off per unit** if the user prefers; avoid complex mixed rules unless requested.
- **Max discount**: Do not suggest a tier that pushes gross margin below an acceptable level; state the margin impact per tier when possible.
- **Product scope**: Clearly list which products or collections the tiers apply to (e.g. "Serum category only," "All moisturizers," "Entire skincare range").

If the user has no app, output **manual equivalent**: e.g. "Buy 2 of [Product] — use code SAVE10 at checkout" with clear PDP/cart instructions.

### 3) Margin check

- For each tier, show **effective price** and **effective margin** (or state "margin stays above X% at tier 2 and 3").
- **Do not** recommend tiers that would drive margin below the user’s stated floor (e.g. "Do not go below 50% margin").
- If margin is tight, suggest **shallower tiers** (e.g. 5% / 10% instead of 10% / 20%) or **limit to 2 tiers**.

### 4) Copy and placement

- **PDP**: Short, benefit-led line above or near Add to Cart: e.g. "Buy 2, save 10% — Buy 3, save 15%." Optional subline: "Stock up on your favorite."
- **Cart**: When quantity ≥ 2, show: "You’re saving X% on this item" or "Y% off when you buy 2+."
- **Collection / banner**: Optional site-wide or category banner: "Stock up and save: 10% off 2, 15% off 3+ on serums and moisturizers."
- **Tone**: Match brand (clean/minimal vs. playful); avoid jargon; focus on clarity and value.

Provide **ready-to-use copy blocks** (1–2 lines per placement) so the merchant or copywriter can drop them in.

### 5) Metrics and validation

- **Primary**: AOV (all orders); units per order (mean and distribution); % of orders with 2+ units of tier-eligible products.
- **Secondary**: Revenue per session; margin % (blended) before vs. after; refund/return rate if behavior changes.
- **Signals**: If % of 2+ unit orders doesn’t rise, test visibility (PDP/cart) and tier steepness; if AOV rises but margin drops too much, reduce discount or narrow product scope.

Output a **short validation plan**: what to measure, at what frequency, and what "success" looks like (e.g. "AOV +15% and 2+ unit share from 12% to 25% in 60 days").

## Rules (keep it executable)

- **Margin-first**: Never suggest a tier that would push effective margin below the user’s stated minimum without flagging it.
- **Simple tiers**: Prefer 2–3 tiers (e.g. 1 / 2 / 3+); avoid more than 3 unless the user explicitly wants more.
- **Clear scope**: Always state which products or collections the tiers apply to.
- **Copy ready**: Give at least one PDP and one cart line the user can use as-is.
- **Platform-agnostic where possible**: Structure works for Shopify, WooCommerce, or custom; call out app or native implementation only when relevant.

## Example tier table (reference)

**Serum and moisturizer — 2–3 tier example**

| Quantity | Discount | Message |
|----------|----------|---------|
| 1        | 0%       | —       |
| 2        | 10% off  | "Buy 2, save 10%" |
| 3+       | 15% off  | "Buy 3, save 15% — stock up and save" |

Effective margin at 60% gross margin and $50 list: 1 unit = 60%; 2 @ 10% off = 56%; 3 @ 15% off = 53%. If minimum acceptable margin is 50%, this structure is safe; if 55%, consider capping at 10% for 3+ or limiting to 2 tiers.

## References

- **Margin and tier math**: When you need effective-margin formulas or copy patterns without re-reading the full skill, read [references/margin_and_tiers.md](references/margin_and_tiers.md).
- For full loyalty and repeat incentives (points, tiers, welcome, win-back), use a loyalty/incentives skill; this skill focuses only on **per-order quantity-break discounts**.
- For bundle strategy (complete the look, kits), use a bundle skill; quantity breaks are **same-SKU or same-category multi-qty**, not mixed-product bundles.
