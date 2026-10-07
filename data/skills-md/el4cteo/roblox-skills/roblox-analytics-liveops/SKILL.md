---
name: roblox-analytics-liveops
description: Analytics and live ops - AnalyticsService economy/funnel/onboarding/progression/custom events, player segments, experience configs via ConfigService, A/B experiments, badges, experience notifications, timed events, daily rewards, season passes. Use when instrumenting a game, tuning economy or onboarding, running A/B tests or feature flags, or planning live events and re-engagement.
---

# Analytics and live operations

## Analytics events (server-side, `AnalyticsService`)

Standard events feed the Creator Hub dashboards automatically (economy, funnels, progression,
custom). The `Fire*` methods are deprecated; use the `Log*` family.

```luau
--!strict
local AnalyticsService = game:GetService("AnalyticsService")

local Analytics = {}

-- Currency sources and sinks → Economy dashboard.
function Analytics.coinsEarned(player: Player, amount: number, balance: number, source: string)
	AnalyticsService:LogEconomyEvent(
		player,
		Enum.AnalyticsEconomyFlowType.Source,
		"Coins", -- currency type
		amount,
		balance, -- ending balance
		Enum.AnalyticsEconomyTransactionType.Gameplay.Name, -- or a custom string like "QuestReward"
		source -- item SKU / source id
	)
end

function Analytics.itemBought(player: Player, price: number, balance: number, itemSku: string)
	AnalyticsService:LogEconomyEvent(
		player,
		Enum.AnalyticsEconomyFlowType.Sink,
		"Coins",
		price,
		balance,
		Enum.AnalyticsEconomyTransactionType.Shop.Name,
		itemSku
	)
end

-- First-session tutorial funnel (steps must be sequential, 1-based).
function Analytics.onboarding(player: Player, step: number, stepName: string)
	AnalyticsService:LogOnboardingFunnelStepEvent(player, step, stepName)
end

-- Recurring funnels (e.g. shop purchase flow); share a session id per attempt.
function Analytics.shopFunnel(player: Player, sessionId: string, step: number, stepName: string)
	AnalyticsService:LogFunnelStepEvent(player, "ShopPurchase", sessionId, step, stepName)
end

-- Level progression.
function Analytics.levelStarted(player: Player, level: number)
	AnalyticsService:LogProgressionStartEvent(player, "MainPath", level, `Level{level}`)
end
function Analytics.levelCompleted(player: Player, level: number)
	AnalyticsService:LogProgressionCompleteEvent(player, "MainPath", level, `Level{level}`)
end

-- Anything else: numeric custom events, sliced by up to 3 custom fields.
function Analytics.bossKilled(player: Player, bossId: string, seconds: number)
	AnalyticsService:LogCustomEvent(player, "BossKillTime", seconds, {
		[Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = bossId,
	})
end

return Analytics
```

Guidelines:
- Log from the **server** (trustworthy, and required by these APIs). Keep event names and custom-field
  values low-cardinality (IDs of categories, not free text or user IDs).
- Economy events need accurate `endingBalance`; log every source and sink or the dashboard misleads.
- Design funnels before building features (onboarding steps, shop flow, first purchase).
- `AnalyticsService:GetPlayerSegmentsAsync(player)` returns segment info (payer status, account age in
  your game, ...) at runtime to tailor onboarding and offers — `pcall` it.

## Experience configs (live values without republishing)

Create configs in Creator Hub (or Open Cloud) — balance numbers, feature flags, event toggles — and read them
on the server with `ConfigService`. Published changes arrive in running servers.

```luau
--!strict
local ConfigService = game:GetService("ConfigService")

local ok, snapshot = pcall(function()
	return ConfigService:GetConfigAsync()
end)

local function get(key: string, default: any): any
	if not ok then
		return default
	end
	local value = snapshot:GetValue(key)
	return if value == nil then default else value
end

local bossHealth = get("bossHealth", 500)
print("boss health", bossHealth)

if ok then
	snapshot.UpdateAvailable:Connect(function()
		snapshot:Refresh() -- apply newly published values at a safe moment (e.g. between rounds)
		print("new boss health", get("bossHealth", 500))
	end)
end
```

- Always code a default: configs may fail to load.
- **Experiments / targeted configs** evaluate per player: use `ConfigService:GetConfigForPlayerAsync(player)`
  (`GetConfigAsync` ignores targeting). Experiments run 14–60 days, up to two variants plus control; pick a
  goal metric and respect the minimum detectable effect. Manage via Creator Hub or the Open Cloud
  experimentation API (`roblox-open-cloud`).
- Studio testing: `ConfigService:SetTestingValue(key, value)` / `ClearTestingValue`.

## Badges

`BadgeService:AwardBadgeAsync(userId, badgeId)` (server, `pcall`; skip if `UserHasBadgeAsync` or
`CheckUserBadgesAsync` already says owned). `AwardBadge`/`UserHasBadge` are deprecated. Badges are
great onboarding and progression milestones and show on players' profiles.

## Experience notifications (re-engagement)

1. Ask players to opt in at a meaningful moment: `ExperienceNotificationService:CanPromptOptInAsync()` then
   `PromptOptIn()` (client).
2. Create notification strings in Creator Hub; send from your backend via Open Cloud
   `POST /cloud/v2/users/{userId}/notifications` (e.g. "your crops are ready", "event starts now").
   Notifications are rate-limited and moderated; send ones players value.

## Live-ops patterns

- **Timed events**: schedule with UTC timestamps in a config (`eventStart`, `eventEnd`); compare with
  `os.time()` on the server; broadcast state via attributes; clients show countdowns from
  `workspace:GetServerTimeNow()`.
- **Season pass / rotating shops**: rotation seed = `math.floor(os.time() / 86400)` for daily shops; store
  claimed rewards per season id in player data.
- **Daily rewards/streaks**: store `lastClaimDay` (UTC day number) and streak count; grant on the server.
- Ship content behind config flags, validate with a small rollout/experiment, then roll out to 100%.
- Watch Creator Hub dashboards: retention (D1/D7/D30), session length, conversion, ARPPU, funnels, and
  performance (crash rate, FPS, memory) after every release.

## Related skills

`roblox-monetization` (offers, pricing), `roblox-data-stores` (streaks, season data),
`roblox-open-cloud` (configs/experiments/notifications APIs), `roblox-game-systems`.
