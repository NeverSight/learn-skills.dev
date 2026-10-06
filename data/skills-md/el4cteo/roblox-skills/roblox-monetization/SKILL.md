---
name: roblox-monetization
description: Robux monetization - developer products with idempotent ProcessReceipt, passes, subscriptions, rewarded video ads, personalized shops, regional pricing and trade arbitrage, paid random item policy (PolicyService), commerce products, private servers, Roblox Plus. Use when adding purchases, shops, game passes, subscriptions, ads, or loot boxes, or debugging lost/duplicated purchases.
---

# Roblox monetization

## Product types

| Type | Buy | Use for | Grant via |
| --- | --- | --- | --- |
| Developer product | Repeatedly | Currency, consumables, boosts, revives | `MarketplaceService.ProcessReceipt` (server) |
| Pass | Once, permanent | VIP, permanent perks, extra slots | `UserOwnsGamePassAsync` check on join + purchase-finished event |
| Subscription | Monthly, revocable | Recurring perks (daily currency, VIP) | `GetUserSubscriptionStatusAsync` + `UserSubscriptionStatusChanged` |
| Rewarded video ad | Free (watch ad) | Small rewards (≈3–10 Robux value) | Developer product granted through `ProcessReceipt` |
| Commerce product | Real money (physical goods) | Merch with bundled digital benefits | `CommerceService`; digital benefits via `ProcessReceipt` |
| Private server | Monthly | Paid private servers | Configured in Creator Dashboard |

All granting happens on the **server**. Never grant from client events like
`PromptProductPurchaseFinished` — clients can fake them.

## Developer products: ProcessReceipt

Rules:
- Exactly **one** server script sets `MarketplaceService.ProcessReceipt`.
- Return `PurchaseGranted` only after the grant is **persisted**. Otherwise return `NotProcessedYet`;
  Roblox retries later (including on the player's next join) with the same `PurchaseId`.
- Handlers must be **idempotent**: record handled `PurchaseId`s in the player's saved data so a retry
  never grants twice.
- Receipts arrive for players who may not be loaded yet or may have left: wait for their data, or
  return `NotProcessedYet`.

```luau
--!strict
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

type PlayerData = { coins: number, purchaseIds: { string } }
type ReceiptInfo = {
	PlayerId: number,
	ProductId: number,
	PurchaseId: string,
	CurrencySpent: number,
	CurrencyType: Enum.CurrencyType,
	PlaceIdWherePurchased: number,
}

local MAX_REMEMBERED_PURCHASES = 100

-- Provided by your data layer (ProfileStore profile.Data, etc.).
local function getLoadedData(_player: Player): PlayerData?
	return nil
end
local function saveNow(_player: Player): boolean
	return true
end

local PRODUCTS: { [number]: (Player, PlayerData) -> () } = {
	[1234567] = function(_player, data) -- 100 coins
		data.coins += 100
	end,
}

local function processReceipt(receipt: ReceiptInfo): Enum.ProductPurchaseDecision
	local player = Players:GetPlayerByUserId(receipt.PlayerId)
	if not player then
		return Enum.ProductPurchaseDecision.NotProcessedYet -- granted on their next visit
	end

	local data = getLoadedData(player)
	local deadline = os.clock() + 20
	while not data and player.Parent == Players and os.clock() < deadline do
		task.wait(0.5)
		data = getLoadedData(player)
	end
	if not data then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	if table.find(data.purchaseIds, receipt.PurchaseId) then
		return Enum.ProductPurchaseDecision.PurchaseGranted -- already granted earlier
	end

	local handler = PRODUCTS[receipt.ProductId]
	if not handler then
		warn(`No handler for product {receipt.ProductId}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	local ok, err = pcall(handler, player, data)
	if not ok then
		warn(`Grant failed for {receipt.PurchaseId}: {err}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	table.insert(data.purchaseIds, receipt.PurchaseId)
	while #data.purchaseIds > MAX_REMEMBERED_PURCHASES do
		table.remove(data.purchaseIds, 1)
	end

	if not saveNow(player) then
		return Enum.ProductPurchaseDecision.NotProcessedYet -- the idempotency list prevents a double grant
	end
	return Enum.ProductPurchaseDecision.PurchaseGranted
end

MarketplaceService.ProcessReceipt = processReceipt :: any
```

With ProfileStore, "persisted" means waiting until the `PurchaseId` appears in `profile.LastSavedData`
(or calling `profile:Save()` and waiting); see ProfileStore's developer products guide.

Prompt from the client (UI) — the server still grants:
`MarketplaceService:PromptProductPurchase(Players.LocalPlayer, productId)`.

## Passes

```luau
--!strict
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local VIP_PASS_ID = 987654

local function grantVip(player: Player)
	player:SetAttribute("VIP", true) -- apply perks from one place
end

local function checkPass(player: Player)
	local ok, owns = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, player.UserId, VIP_PASS_ID)
	if ok and owns then
		grantVip(player)
	end
end

Players.PlayerAdded:Connect(checkPass)
for _, player in Players:GetPlayers() do
	task.spawn(checkPass, player)
end

-- Fires on the server too; re-verify ownership rather than trusting `purchased` alone.
MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player, passId, purchased)
	if purchased and passId == VIP_PASS_ID then
		checkPass(player)
	end
end)
```

`UserOwnsGamePassAsync` results are cached per server; the purchase-finished handler covers in-session buys.

## Subscriptions

- Check with `MarketplaceService:GetUserSubscriptionStatusAsync(player, "EXP-...")` → `{ IsSubscribed, IsRenewing }`
  on join and on `Players.UserSubscriptionStatusChanged(player, subscriptionId)`.
- Benefits must be **revocable**: when `IsSubscribed` is false, remove perks you persisted.
- Prompt with `MarketplaceService:PromptSubscriptionPurchase(player, subscriptionId)`.
- Replacing a pass with a subscription: keep honoring existing pass owners, take the pass off sale.

## Shops that sell

- Personalize order with `MarketplaceService:RankProductsAsync(identifiers)` (call once on join —
  strict rate limit) and "Top picks" with `RecommendTopProductsAsync({ Enum.InfoType.Product, Enum.InfoType.GamePass })`
  (needs a sale in the last 28 days; call in `task.spawn`).
- Show live prices from `GetProductInfoAsync(id, Enum.InfoType.Product)` / `GetDeveloperProductsAsync()` — never
  hardcode Robux prices: **managed pricing** (regional pricing + price optimization) shows different
  users different prices. `receipt.CurrencySpent` has what the user actually paid.
- Contextual offers (revive on death, boost when stuck) outperform static menus. Also list items in
  the game's **Shop** tab in Creator Hub.

## Compliance

- **Paid random items** (loot boxes, gacha, spins bought with Robux or Robux-bought currency): disclose
  odds before purchase, and check `PolicyService:GetPolicyInfoForPlayerAsync(player)`:
  - `ArePaidRandomItemsRestricted` → offer a free earnable path, a disclosed fixed sequence, or direct purchase.
  - `IsPaidItemTradingAllowed` → disable trading of paid items when false.
- **Regional pricing arbitrage**: gate gifting/trading of purchased items using
  `MarketplaceService:GetUsersPriceLevelsAsync(userIds)` (1–1000, % of global price); fetch at join,
  don't cache across sessions.
- Rewarded video rewards must be developer products, not random, and must not harm the player's
  character while the ad plays.
- Respect age/region restrictions returned by `PolicyService` for ads, social links, and trading.

Rewarded video ads, commerce products, Premium/Roblox Plus hooks: [references/ads-and-extras.md](references/ads-and-extras.md).

## Related skills

`roblox-data-stores` (persisting grants), `roblox-security` (economy exploits), `roblox-ui` (shop UI),
`roblox-analytics-liveops` (economy events, funnels, experiments).
