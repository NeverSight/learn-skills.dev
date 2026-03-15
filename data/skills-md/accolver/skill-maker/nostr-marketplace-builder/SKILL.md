---
name: nostr-marketplace-builder
description: Build Nostr marketplace applications using NIP-15 stalls, products, auctions, and NIP-69 P2P orders. Use when creating e-commerce on Nostr, building product listings, setting up stalls with shipping zones, implementing auction bidding systems, constructing checkout flows with NIP-04 DMs, creating P2P trading orders, or generating marketplace UI configurations. Covers kind:30017 stalls, kind:30018 products, kind:30020 auctions, kind:1021 bids, kind:1022 bid confirmations, kind:30019 marketplace UI, and kind:38383 P2P orders.
---

# Nostr Marketplace Builder

## Overview

Construct correct Nostr marketplace events for commerce applications. This skill
handles the non-obvious parts: stall/product relationships, shipping cost
calculations, auction lifecycle rules, checkout message sequencing via NIP-04,
and P2P order tag structures from NIP-69.

## When to Use

- Creating a merchant stall with shipping zones (kind:30017)
- Listing products with categories and specs (kind:30018)
- Setting up auctions with bidding (kind:30020, kind:1021, kind:1022)
- Building checkout flows (NIP-04 order → payment → status)
- Creating P2P buy/sell orders for bitcoin trading (NIP-69 kind:38383)
- Configuring a custom marketplace UI (kind:30019)
- Calculating shipping costs across zones and products

**Do NOT use when:**

- Building generic Nostr events (use nostr-event-builder)
- Implementing relay WebSocket logic
- Working with NIP-19 encoding/decoding

## Workflow

### 1. Identify What to Build

| Intent                         | Kind(s)    | NIP    |
| ------------------------------ | ---------- | ------ |
| Create/update a merchant stall | 30017      | NIP-15 |
| List a product for sale        | 30018      | NIP-15 |
| Configure marketplace UI       | 30019      | NIP-15 |
| Create an auction listing      | 30020      | NIP-15 |
| Place a bid on an auction      | 1021       | NIP-15 |
| Confirm/reject a bid           | 1022       | NIP-15 |
| Checkout (order/pay/status)    | NIP-04 DMs | NIP-15 |
| P2P buy/sell order             | 38383      | NIP-69 |

### 2. Build the Event

#### Stall (Kind:30017) — Addressable

The stall is the merchant's store. Products belong to stalls. Shipping zones are
defined at the stall level with base costs.

```json
{
  "kind": 30017,
  "tags": [["d", "my-stall-001"]],
  "content": "{\"id\":\"my-stall-001\",\"name\":\"Satoshi's Electronics\",\"description\":\"Quality electronics for sats\",\"currency\":\"USD\",\"shipping\":[{\"id\":\"us-domestic\",\"name\":\"US Domestic\",\"cost\":5.99,\"regions\":[\"US\"]},{\"id\":\"worldwide\",\"name\":\"Worldwide\",\"cost\":15.00,\"regions\":[\"EU\",\"AS\",\"SA\"]}]}"
}
```

**Rules:**

- `d` tag value MUST equal the `id` in content JSON
- `id` should be a UUID or descriptive slug — sequential IDs (`0`, `1`, `2`) are
  discouraged
- `currency` is a string (e.g., `"USD"`, `"BTC"`, `"EUR"`)
- `shipping` array defines zones; customer must choose exactly one zone at
  checkout
- Each zone has a base `cost` in the stall's currency

#### Product (Kind:30018) — Addressable

Products belong to a stall via `stall_id`. They can add per-product shipping
costs on top of the stall's base shipping cost.

```json
{
  "kind": 30018,
  "tags": [
    ["d", "product-xyz-789"],
    ["t", "electronics"],
    ["t", "gadgets"]
  ],
  "content": "{\"id\":\"product-xyz-789\",\"stall_id\":\"my-stall-001\",\"name\":\"Lightning Node Kit\",\"description\":\"Pre-configured Bitcoin node\",\"images\":[\"https://example.com/node.jpg\"],\"currency\":\"USD\",\"price\":299.99,\"quantity\":25,\"specs\":[[\"processor\",\"ARM Cortex-A72\"],[\"storage\",\"1TB SSD\"],[\"connectivity\",\"Ethernet + WiFi\"]],\"shipping\":[{\"id\":\"us-domestic\",\"cost\":10.00},{\"id\":\"worldwide\",\"cost\":25.00}]}"
}
```

**Rules:**

- `d` tag value MUST equal the `id` in content JSON
- `stall_id` MUST reference an existing stall's `id`
- `quantity`: integer for limited stock, `null` for unlimited (digital
  goods/services)
- `t` tags are searchable categories — use multiple for discoverability
- `specs` is an array of `[key, value]` pairs for structured display
- Product `shipping[].id` MUST match a zone `id` from the parent stall
- **Total shipping = stall base cost + (product shipping cost × quantity)**

#### Marketplace UI (Kind:30019) — Addressable

Custom marketplace configuration grouping merchants together:

```json
{
  "kind": 30019,
  "tags": [["d", "my-marketplace"]],
  "content": "{\"name\":\"Bitcoin Bazaar\",\"about\":\"A curated marketplace for Bitcoin products\",\"ui\":{\"picture\":\"https://example.com/logo.png\",\"banner\":\"https://example.com/banner.jpg\",\"theme\":\"dark\",\"darkMode\":true},\"merchants\":[\"pubkey1hex...\",\"pubkey2hex...\"]}"
}
```

#### Auction (Kind:30020) — Addressable

Auctions are similar to products but with bidding mechanics:

```json
{
  "kind": 30020,
  "tags": [["d", "auction-rare-item-001"]],
  "content": "{\"id\":\"auction-rare-item-001\",\"stall_id\":\"my-stall-001\",\"name\":\"Signed Hal Finney Print\",\"description\":\"Limited edition signed print\",\"images\":[\"https://example.com/print.jpg\"],\"starting_bid\":50000,\"start_date\":1719391096,\"duration\":86400,\"specs\":[[\"condition\",\"mint\"],[\"authentication\",\"verified\"]],\"shipping\":[{\"id\":\"worldwide\",\"cost\":20.00}]}"
}
```

**Rules:**

- `starting_bid` is in the stall's currency (integer)
- `start_date` is a Unix timestamp; omit if start date is unknown
- `duration` is seconds the auction runs (excluding extensions)
- Actual end =
  `start_date + duration + SUM(all duration_extended from confirmations)`
- **Cannot edit auction after receiving first bid** — bids reference the event
  ID (not product UUID), so editing creates a new event ID and loses all bids

#### Bid (Kind:1021) — Regular

```json
{
  "kind": 1021,
  "content": "75000",
  "tags": [["e", "<auction-event-id>"]]
}
```

**Rules:**

- `content` is the bid amount as a string (in the auction's currency)
- The `e` tag references the **event ID** of the auction, not the product UUID
- This is why editing an auction after bids destroys those bids

#### Bid Confirmation (Kind:1022) — Regular

Sent by the merchant to validate bids:

```json
{
  "kind": 1022,
  "content": "{\"status\":\"accepted\",\"message\":\"Bid received and validated\",\"duration_extended\":300}",
  "tags": [
    ["e", "<bid-event-id>"],
    ["e", "<auction-event-id>"]
  ]
}
```

**Status values:** `accepted`, `rejected`, `pending`, `winner`

- `winner` is sent to the winning bid after auction ends
- `duration_extended` (optional): seconds added to auction duration
- Clients must verify the confirmation pubkey matches the merchant's pubkey

### 3. Checkout Flow (NIP-04 DMs)

Checkout uses encrypted direct messages. See
[references/checkout-flow.md](references/checkout-flow.md) for full details.

**Step 1 — Customer sends order (type:0):**

```json
{
  "id": "order-uuid-123",
  "type": 0,
  "name": "Alice",
  "address": "123 Bitcoin St, Miami, FL",
  "message": "Please ship ASAP",
  "contact": {
    "nostr": "<customer-pubkey-hex>",
    "phone": null,
    "email": "alice@example.com"
  },
  "items": [
    { "product_id": "product-xyz-789", "quantity": 2 }
  ],
  "shipping_id": "us-domestic"
}
```

**Step 2 — Merchant sends payment request (type:1):**

```json
{
  "id": "order-uuid-123",
  "type": 1,
  "message": "Payment required within 15 minutes",
  "payment_options": [
    { "type": "ln", "link": "lnbc..." },
    { "type": "btc", "link": "bc1q..." },
    { "type": "url", "link": "https://pay.example.com/order-123" }
  ]
}
```

**Step 3 — Merchant sends status update (type:2):**

```json
{
  "id": "order-uuid-123",
  "type": 2,
  "message": "Payment confirmed, shipping tomorrow",
  "paid": true,
  "shipped": false
}
```

### 4. P2P Orders (NIP-69 Kind:38383)

For peer-to-peer bitcoin trading. See
[references/marketplace-events.md](references/marketplace-events.md) for full
tag reference.

```json
{
  "kind": 38383,
  "tags": [
    ["d", "order-uuid-456"],
    ["k", "sell"],
    ["f", "USD"],
    ["s", "pending"],
    ["amt", "100000"],
    ["fa", "50"],
    ["pm", "zelle", "cashapp"],
    ["premium", "3"],
    ["network", "mainnet"],
    ["layer", "lightning"],
    ["name", "SatoshiTrader"],
    ["bond", "1000"],
    ["expires_at", "1719391096"],
    ["expiration", "1719995896"],
    ["y", "my-platform"],
    ["z", "order"]
  ],
  "content": ""
}
```

**Required tags:** `d`, `k`, `f`, `s`, `amt`, `fa`, `pm`, `premium`, `network`,
`layer`, `expires_at`, `expiration`, `y`, `z`

**Status flow:** `pending` → `in-progress` → `success` | `canceled` | `expired`

### 5. Validate Before Publishing

- [ ] `d` tag matches content `id` (for kinds 30017, 30018, 30020)
- [ ] Product `stall_id` references a valid stall
- [ ] Product shipping zone IDs match stall shipping zone IDs
- [ ] `quantity` is integer or null (not string, not undefined)
- [ ] Auction `starting_bid` is an integer
- [ ] Bid `e` tag references auction event ID (not product UUID)
- [ ] Bid confirmation has two `e` tags (bid + auction)
- [ ] Checkout messages use correct `type` values (0, 1, 2)
- [ ] P2P order has `z` tag set to `"order"`
- [ ] P2P order `f` tag uses ISO 4217 currency code
- [ ] P2P order `k` tag is `"buy"` or `"sell"`
- [ ] All timestamps are Unix seconds (not milliseconds)
- [ ] Content is stringified JSON where required

## Shipping Cost Calculation

Total shipping for an order:

```
base_cost = stall.shipping[chosen_zone].cost
per_product = SUM(product.shipping[chosen_zone].cost × quantity) for each item
total_shipping = base_cost + per_product
```

Example: Stall base shipping $5.99, buying 2 units of a product with $10 extra
shipping per unit → total shipping = $5.99 + (2 × $10) = $25.99.

## Common Mistakes

| Mistake                                          | Why It Breaks                                 | Fix                                             |
| ------------------------------------------------ | --------------------------------------------- | ----------------------------------------------- |
| `d` tag doesn't match content `id`               | Relay can't address the event correctly       | Always keep `d` tag and content `id` identical  |
| Sequential IDs (`0`, `1`, `2`)                   | Collision risk across merchants               | Use UUIDs or descriptive slugs                  |
| Editing auction after bids received              | Bids reference event ID which changes on edit | Never edit auctions that have bids              |
| Bid references product UUID instead of event ID  | Bid won't be associated with the auction      | Use the auction's Nostr event ID in the `e` tag |
| Missing `z` tag on P2P orders                    | Clients can't identify the event as an order  | Always include `["z", "order"]`                 |
| Using `buy`/`sell` without ISO 4217 `f` tag      | Currency is ambiguous                         | Use standard codes: USD, EUR, BRL, VES          |
| Product shipping zone ID doesn't match stall     | Shipping calculation breaks                   | Product shipping IDs must exist in parent stall |
| `quantity` as string `"10"` instead of int `10`  | Type mismatch in clients                      | Use integer or null, never string               |
| Checkout type as string `"0"` instead of int `0` | Message routing fails                         | Use integer type values: 0, 1, 2                |
| Bid confirmation missing auction `e` tag         | Can't link confirmation to auction            | Include both bid and auction `e` tags           |

## Quick Reference

| Event            | Kind  | Category    | Key Fields                                       |
| ---------------- | ----- | ----------- | ------------------------------------------------ |
| Stall            | 30017 | Addressable | id, name, currency, shipping zones               |
| Product          | 30018 | Addressable | id, stall_id, price, quantity, specs, shipping   |
| Marketplace UI   | 30019 | Addressable | name, ui config, merchant pubkeys                |
| Auction          | 30020 | Addressable | id, stall_id, starting_bid, start_date, duration |
| Bid              | 1021  | Regular     | amount in content, e tag → auction event ID      |
| Bid Confirmation | 1022  | Regular     | status, e tags → bid + auction                   |
| P2P Order        | 38383 | Addressable | k (buy/sell), f (currency), s (status), amt, fa  |

## Key Principles

1. **IDs must be consistent** — The `d` tag and the `id` field inside content
   JSON must always match. This is how addressable events are located.

2. **Shipping is hierarchical** — Stalls define base shipping zones and costs.
   Products add per-unit costs on top. The customer picks one zone at checkout.

3. **Auctions are immutable after bids** — Because bids reference the event ID
   (not a UUID), editing an auction creates a new event and orphans existing
   bids. Design auctions carefully before publishing.

4. **Checkout is sequential** — Order (type:0) → Payment request (type:1) →
   Status update (type:2). Each message references the same order ID. All
   messages are NIP-04 encrypted DMs.

5. **P2P orders are self-contained** — All trade parameters live in tags, not
   content. The `z` tag must be `"order"` for client discovery. Status
   transitions follow: pending → in-progress → success/canceled/expired.
