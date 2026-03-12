---
name: roblox-monetization
description: Use when developing Roblox games or experiences and need to earn Robux through Game Passes, Developer Products, UGC avatar items, or Premium Payouts — covers both Studio scripting and Creator Hub dashboard setup.
---

# Roblox Monetization

## Overview

End-to-end guide for earning Robux legitimately through Roblox's monetization systems. Covers dashboard configuration and Lua scripting for both developers and designers.

## Quick Reference

| System | Use For | Repeatable? | Min Price |
|--------|---------|-------------|-----------|
| Game Pass | Permanent perks/access | No (one-time) | 1 Robux |
| Developer Product | Consumables, currency, boosts | Yes (unlimited) | 1 Robux |
| UGC Item | Avatar marketplace sales | N/A | 1 Robux |
| Premium Payout | Passive playtime income | Automatic | No setup |

---

## 1. Game Passes

One-time purchases granting permanent perks. Player pays once per game per pass.

### Dashboard Setup
1. [create.roblox.com](https://create.roblox.com) → select experience → **Monetization → Passes**
2. **Create a Pass** → upload 512×512 PNG icon, set name, description, price
3. Save → note the **Pass ID**

### Server Script
```lua
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local PASS_ID = 000000 -- your Pass ID

-- Check ownership on join
Players.PlayerAdded:Connect(function(player)
    local success, hasPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, PASS_ID)
    end)
    if success and hasPass then
        -- grant perk
    end
end)

-- Prompt purchase (call from server)
local function promptPass(player)
    MarketplaceService:PromptGamePassPurchase(player, PASS_ID)
end

-- Grant immediately after purchase
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
    if purchased and passId == PASS_ID then
        -- grant perk
    end
end)
```

> **Always run on server (Script), never LocalScript** — client-side ownership checks can be spoofed.

---

## 2. Developer Products

Repeatable purchases — players can buy unlimited times. Use for coins, potions, boosts, in-game currency.

### Dashboard Setup
1. Creator Hub → experience → **Monetization → Developer Products**
2. **Create a Developer Product** → set name, description, icon, price
3. Note the **Product ID**

### Server Script
```lua
local MarketplaceService = game:GetService("MarketplaceService")
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local PRODUCT_ID = 000000 -- your Product ID
local coinStore = DataStoreService:GetDataStore("PlayerCoins")

local function processReceipt(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    if not player then
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end

    if receiptInfo.ProductId == PRODUCT_ID then
        -- Persist to DataStore FIRST — if server crashes after this line, coins are safe
        local ok, err = pcall(function()
            coinStore:UpdateAsync(tostring(player.UserId), function(current)
                return (current or 0) + 100
            end)
        end)
        if not ok then
            warn("DataStore failed:", err)
            return Enum.ProductPurchaseDecision.NotProcessedYet -- Roblox will retry
        end
        -- Now safe to update in-memory value (leaderstats, etc.)
    end

    return Enum.ProductPurchaseDecision.PurchaseGranted
end

MarketplaceService.ProcessReceipt = processReceipt

-- Prompt purchase
local function promptProduct(player)
    MarketplaceService:PromptProductPurchase(player, PRODUCT_ID)
end
```

> **Critical rules for `ProcessReceipt`:**
> - Must return `PurchaseGranted` or `NotProcessedYet` — never error silently
> - Persist to DataStore **before** returning — crashes can cause loss
> - Return `NotProcessedYet` on DataStore failure so Roblox retries the receipt
> - Only one `ProcessReceipt` handler allowed per server; combine all product IDs inside it
> - Roblox may call `ProcessReceipt` more than once for the same purchase — use `receiptInfo.PurchaseId` as a dedup key if double-granting is a concern

---

## 3. UGC / Avatar Items

Sell clothing, accessories, and bundles in the Roblox Marketplace.

### Requirements
- UGC Program access — apply at [roblox.com/create/ugc](https://www.roblox.com/create/ugc)
- ID verification completed on your account
- Roblox Studio or Blender for 3D mesh items

### Workflow
1. Design item (follow [Roblox mesh/texture specs](https://create.roblox.com/docs/art/accessories/specifications))
2. Creator Hub → **Avatar Items → Create** → upload, set category, tags, price
3. Submit for moderation (typically 1–3 business days)
4. Item goes live and appears in Marketplace

### Earning Rates

| Item Type | Creator Cut |
|-----------|-------------|
| Clothing (t-shirts, shirts, pants) | 70% of sale |
| UGC Accessories | 30% (40% with Premium subscription) |
| Limited UGC with resale | Up to 70% |

---

## 4. Communicating Purchase State to the Client

After granting a product server-side, notify the client via a `RemoteEvent` so the UI can update (show a boost timer, unlock a button, etc.):

```lua
-- Inside ProcessReceipt, after DataStore save succeeds
local NotifyClient = game:GetService("ReplicatedStorage").Remotes.PurchaseGranted
local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
if player then
    NotifyClient:FireClient(player, { productId = receiptInfo.ProductId })
end
```

---

## 5. Premium Payouts

Passive Robux from Roblox Premium subscribers spending time in your game. **No setup required.**

- Roblox tracks Premium member engagement automatically
- You receive a share of the Premium Payout Pool monthly, proportional to Premium playtime
- View earnings: Creator Hub → **Analytics → Monetization → Premium Payouts**

### Maximize Premium Payouts
- Build longer session loops (progression, story, replayability)
- Add Premium-exclusive cosmetics or bonuses to attract Premium players

---

## DevEx: Robux → Real Money

**Eligibility requirements:**
- 30,000+ Robux earned (purchased Robux do not count)
- Age 13 or older
- Verified email address on your Roblox account
- No active account violations
- Roblox Premium subscription

**Steps:**
1. Creator Hub → **DevEx (Developer Exchange)**
2. Submit exchange request
3. Roblox reviews request (typically 1–2 weeks)
4. Paid via **Tipalti** at approximately **$0.0035 per Robux** (~$122 per 35,000 Robux)

> **Tipalti:** You must create and verify a Tipalti account separately before your first payout. Set this up early to avoid delays.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ownership check in LocalScript | Move to server Script — client checks can be exploited |
| `ProcessReceipt` throws an error | Wrap logic in `pcall`; always return a decision enum |
| Not saving purchase to DataStore | Player loses item on crash — persist before returning `PurchaseGranted` |
| Multiple `ProcessReceipt` handlers | Only one allowed per server — combine all product logic in one function |
| Double-granting on receipt retry | Use `receiptInfo.PurchaseId` as a DataStore key to detect already-processed receipts |
| Selling UGC without program access | Apply to UGC program first; uploads will be rejected otherwise |
| Price below platform minimum | Minimum is 1 Robux for most item types |
| DevEx blocked despite enough Robux | Check all eligibility: age 13+, verified email, no violations, Premium subscription, earned (not purchased) Robux |
