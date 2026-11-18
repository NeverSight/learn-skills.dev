---
name: stockout-prevention
description: >-
  Monitors FBA inventory health, identifies stockout risks from sales velocity,
  and orchestrates prevention actions — primarily inbound-shipment gap analysis and
  restocking. Triggers on: inventory check, stockout risk, FBA stock levels,
  days of cover, days of supply, replenishment, "am I going to run out". Do NOT use
  for: catalog management, new product listings, advertising, or order fulfillment.
version: 1.0.0
license: Apache-2.0
metadata:
  author: Amazon Selling Partner
  persona: Maya (non-technical FBA seller)
  pattern: Pipeline + Inversion
  tags: [sp-api, inventory, fba, stockout, pricing]
  platforms: [claude-desktop, aws-quick]
  apis: [fba-inventory, sales, fba-inbound, listings]
---

# Stockout Prevention Skill

## Description

Helps a Fulfilled-by-Amazon seller stay ahead of stockouts. It pulls current FBA
inventory, derives sales velocity, computes **days of cover** per SKU, checks
whether inbound shipments arrive in time, and proposes preventive actions. Write
actions (e.g. price changes) are **always drafted for the seller's approval** —
never executed silently.

## When to use this skill

Use when the seller asks anything about inventory health, running out of stock,
replenishment timing, or "what should I prioritize" for their FBA stock. Do not
use for listing content, advertising, or order management.

## Tools this skill orchestrates

All are SP-API MCP tools served via the Amazon Selling Partner Connector (the `amazon-selling-partner` MCP server):

| Step | Tool | Purpose |
|------|------|---------|
| Inventory | `fbaInventory_getInventorySummaries` | Current fulfillable units per SKU |
| Velocity | `sales_getOrderMetrics` | Units sold over a window (per SKU when possible) |
| Inbound | `fbaInbound_listInboundPlans` | In-transit shipments + ETAs |
| Action | `listings_patchListingsItem` | Draft a price change (VALIDATION_PREVIEW first) |

> Every call needs `entityId` (the seller's merchant id) and `marketplaceIds`
> (e.g. `ATVPDKIKX0DER` for US). If you don't know the entityId, ask the seller once
> and reuse it for the session.

## Workflow (Pipeline + Inversion — ask before acting)

### Step 1 — Assess inventory
Call `fbaInventory_getInventorySummaries` (granularityType `Marketplace`).
Record `sellerSku`, `productName`, and `fulfillableQuantity` for each SKU.

### Step 2 — Measure velocity
For each SKU with meaningful stock, call `sales_getOrderMetrics` over the **last 30
days** (`granularity: Total`, pass the `sku`). Compute:

```
avg_daily_units = unitCount / 30
days_of_cover   = fulfillableQuantity / avg_daily_units
```

### Step 3 — Classify risk
- **CRITICAL** — days_of_cover < 7
- **WARNING** — 7 ≤ days_of_cover < 21
- **HEALTHY** — days_of_cover ≥ 21 (do **not** flag these; say they look fine)

> **Reconciling with Amazon's canonical rule.** Amazon's own analysis rule is *days of
> supply < 14 → at risk*. These bands are intentionally more conservative: 7–14 is the
> canonical at-risk range, and 14–21 is an *early-warning* buffer this skill adds so a
> fast-moving SKU is caught before it crosses 14. For a SKU in the 14–21 range, say it is
> **approaching** risk — not yet at-risk by Amazon's rule — rather than implying it already
> breached the threshold.

Present a short table: SKU · fulfillable · ~daily sales · days of cover · status.

### Step 3b — Visualize the risk (render a chart artifact)
After the table, **create a visual artifact** so the seller can see the risk at a glance.
Render an HTML/JS artifact (a single self-contained file) with a **days-of-cover bar chart**:
- one bar per SKU, height = days of cover;
- color each bar by status — **red = CRITICAL (<7)**, **amber = WARNING (7–21)**, **green = HEALTHY (≥21)**;
- draw a dashed threshold line at 7 and 21 days; label each bar with the SKU and its day count.
Keep it clean and legible (large fonts, title "Days of Cover by SKU"). Use inline SVG or a
lightweight chart approach — no external network calls.

### Step 4 — Check the inbound pipeline (only for flagged SKUs)
Call `fbaInbound_listInboundPlans`. For each flagged SKU, find any in-transit
shipment containing it and read its `estimatedDeliveryWindow`. Compute the **gap**:

```
stockout_date    = today + days_of_cover
shipment_arrives = estimatedDeliveryWindow.start
gap_days         = shipment_arrives - stockout_date   (positive = will stock out first)
```

Call this out explicitly: "You'll run out ~N days **before** the next shipment lands."

### Step 4b — Visualize the gap (render a timeline artifact)
For the most critical SKU, **create a second visual artifact**: a horizontal **timeline**
showing **today**, the **projected stockout date**, and the **shipment arrival window** —
with the at-risk gap between stockout and arrival shaded red and labeled
"~N days out of stock". Title it "Stockout vs. Inbound Shipment". Self-contained, no network calls.

### Step 5 — Recommend options (for CRITICAL SKUs with a gap)
Offer concrete choices, each with its trade-off. Lead with the actions Amazon's own
inventory guidance points to. **Do not raise pricing as an option at all** — this skill
gives no pricing advice in either direction (see Step 6 if the seller names a price).
- **A. Get more units in, sooner** — expedite an existing inbound shipment or create a new
  one so stock lands before the run-out date (this is where the
  [fba-inbound-management](../fba-inbound-management/SKILL.md) skill takes over). This is the
  primary lever.
- **B. Accept the stockout and plan the recovery** — note the cost (lost sales, BSR/rank
  recovery, and that running very lean can trigger the **low-inventory-level fee**), and line
  up the restock so it doesn't repeat.

Then **ask the seller what else they'd like to explore** rather than steering them:
> "Would you like to look at anything else — for example some quick market research on
> demand, competing offers, or seasonality for this SKU — before deciding?"
If they'd like it, offer **market research** (demand, seasonality, competing offers) using
the analytics and catalog data available, so any decision is informed. Report what the data
shows; do not translate it into a pricing recommendation.

**If the seller raises price themselves**, do not advise for or against it and do not
discuss trade-offs. If they name a **specific price**, go to Step 6 and draft exactly that.
If they ask whether they should change price, say pricing is their decision and this skill
doesn't advise on it, then return to the restock options above.

### Step 6 — Draft actions (DO NOT EXECUTE without approval)
Only if the seller has named a specific price, call `listings_patchListingsItem` with
**`mode: VALIDATION_PREVIEW`** so nothing changes yet. Show them, as a numbered list:
- exact SKU, current → the price **they specified**

Draft only. Add no commentary on whether the price is advisable, no projected effect, and
no revert date — if the seller wants a revert, they will say so.

Then **WAIT** for the seller to type "approve" (or adjust). Never re-run the patch
in live mode unless they explicitly approve.

### Step 7 — Summarize
Recap what was found, what (if anything) was drafted, and the single most important
next action. Keep it short and seller-friendly.

## Guardrails
- **Give no pricing guidance, in either direction.** Never suggest raising or lowering a
  price, never present a price change as an option, and never comment on whether a price the
  seller names is wise, safe, or advisable. Coming from Amazon, pricing advice carries
  implications this skill must not create. Lead with getting units in sooner. If the seller
  names a specific price, draft exactly that, mechanically, per
  [price-change-guardrails.md](references/price-change-guardrails.md); if they ask for advice,
  say pricing is their decision and this skill doesn't advise on it.
- Read-only by default. The only write tool is `listings_patchListingsItem`, and it
  is run in `VALIDATION_PREVIEW` until the seller approves.
- Never invent inventory or sales numbers — only report what the tools return.
- If a healthy SKU comes back, say so plainly; do not manufacture risk.

## References
- [reports-vs-ordermetrics.md](references/reports-vs-ordermetrics.md) — why we use
  `sales_getOrderMetrics` (sync) instead of the async Reports API.
- [price-change-guardrails.md](references/price-change-guardrails.md) — the preview +
  approval mechanics for a seller-specified price write. No pricing guidance.
