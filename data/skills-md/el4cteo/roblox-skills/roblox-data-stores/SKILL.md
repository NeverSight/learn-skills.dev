---
name: roblox-data-stores
description: Persistence and cross-server data - DataStoreService (UpdateAsync, retries, budgets, limits), session locking with ProfileStore, schema migrations, OrderedDataStore leaderboards, MemoryStore queues/sorted maps/hash maps, MessagingService, right-to-be-forgotten. Use when saving player data, building leaderboards or queues, or fixing data loss, duplication, or throttling.
---

# Roblox data stores and cloud services

## Choose the service

| Need | Service | Notes |
| --- | --- | --- |
| Player progress, inventory, settings | **DataStore** via ProfileStore (session-locked) | One key per player (`User_{UserId}`), ≤ 4 MB. |
| Global leaderboards | `OrderedDataStore` | Integer values only; periodic updates, cached reads. |
| Fast, temporary, cross-server state | `MemoryStoreService` | Sorted maps, queues, hash maps; everything expires (TTL ≤ 45 days). |
| Matchmaking queues, live events, server lists | MemoryStore queue / sorted map | Not durable — never the only copy of valuable data. |
| Broadcast to all servers | `MessagingService` | ≤ 1 kB per message, best effort, no delivery guarantee. |
| Values changed by live-ops without publishing | Experience configs (`ConfigService`) | See `roblox-analytics-liveops`. |

## Player data: use session locking

Two servers must never own the same player's data at once (teleports, fast rejoins), or items duplicate
and progress is lost. **ProfileStore** (loleris) implements session locking, auto-save, and
`BindToClose` flushing, and is the recommended default. Install it from Wally/the Creator Store and put
it in `ServerScriptService`.

```luau
-- ServerScriptService/Server/Services/DataService.luau (ProfileStore)
local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")

local ProfileStore = require(ServerScriptService.ServerPackages.ProfileStore)

local TEMPLATE = {
	version = 1,
	coins = 0,
	inventory = {} :: { [string]: number },
}
type PlayerData = typeof(TEMPLATE)

local PlayerStore = ProfileStore.New("PlayerData", TEMPLATE)
local profiles: { [Player]: typeof(PlayerStore:StartSessionAsync("")) } = {}

local function onPlayerAdded(player: Player)
	local profile = PlayerStore:StartSessionAsync(`User_{player.UserId}`, {
		Cancel = function()
			return player.Parent ~= Players -- stop waiting if the player left
		end,
	})
	if profile == nil then
		player:Kick("Could not load your data. Please rejoin.")
		return
	end
	profile:AddUserId(player.UserId) -- GDPR / right-to-be-forgotten linkage
	profile:Reconcile() -- fill in fields added to TEMPLATE since this profile was created
	profile.OnSessionEnd:Connect(function()
		profiles[player] = nil
		player:Kick("Your data was loaded on another server. Please rejoin.")
	end)
	if player.Parent == Players then
		profiles[player] = profile
	else
		profile:EndSession() -- left while loading
	end
end

for _, player in Players:GetPlayers() do
	task.spawn(onPlayerAdded, player)
end
Players.PlayerAdded:Connect(onPlayerAdded)
Players.PlayerRemoving:Connect(function(player)
	local profile = profiles[player]
	if profile then
		profile:EndSession() -- saves and releases the lock
	end
end)

local DataService = {}
function DataService.get(player: Player): PlayerData?
	local profile = profiles[player]
	return profile and profile.Data
end
return DataService
```

Mutate `profile.Data` directly on the server (it is cached in memory and auto-saved). Don't
`SetAsync` per change. Check the ProfileStore docs for the exact current API before relying on less
common features (global updates, `MessageAsync`, mock stores for Studio).

## Raw DataStoreService rules (when not using a wrapper)

- **Buffer in memory**: load once on join, mutate the in-memory table, save periodically (e.g. every
  2–5 minutes with random jitter), on leave, at checkpoints (purchases), and in `game:BindToClose`.
- **`UpdateAsync` over `SetAsync`** whenever the write depends on the old value or multiple servers may
  write the key. The transform function must be pure and fast (no yields); return `nil` to cancel.
- **Retry transient errors** with exponential backoff + jitter, capped attempts; process retries for
  a key in order (an old retry must not overwrite newer data). Treat a failed write as "outcome unknown".
- Never save `Instance`s, `Vector3`, `CFrame`, functions, or mixed/sparse tables: store plain tables,
  numbers, strings, booleans, and `buffer`s. Serialize datatypes (`{ x, y, z }`). Validate UTF-8 strings.
- Keys and data store names ≤ 50 characters; value ≤ 4,194,304 characters after JSON encoding.
- Stable key patterns (`User_{UserId}`), never display names. Few data stores, few keys per player.
- Studio needs **File → Experience Settings → Security → Enable Studio Access to API Services**; use a separate test
  universe or a different data store name so testing never touches production data.

Complete raw implementation (session lock, autosave, BindToClose, retries):
[references/raw-datastore.md](references/raw-datastore.md).

## Budgets and limits (2026)

| Limit | Value |
| --- | --- |
| Experience-wide standard reads / writes | `300 + 40 × CCU` / `300 + 20 × CCU` per minute (shared with Open Cloud) |
| Default per-server reads/writes | `60 + 40 × players` per minute each (configurable) |
| Ordered writes per server | `30 + 5 × players` per minute |
| Per-key throughput | 25 MB/min read, 4 MB/min write |
| Storage (latest versions, compressed) | `500 MB + 1 MB × lifetime users` per experience |
| Queue per request type | 30 pending requests, then errors 301–306 |

- `UpdateAsync` consumes both read and write budget.
- Check `DataStoreService:GetRequestBudgetForRequestType(Enum.DataStoreRequestType.StandardWrite)` before
  bulk work; tune per-server limits once at startup with `SetRateLimitForRequestType`.
- Don't pre-compress data; Roblox compresses automatically. Shard only genuinely hot keys.
- Use versions (`ListVersionsAsync`, `GetVersionAtTimeAsync`) to restore data instead of writing backup keys.

## Schema versioning and migrations

Store a `version` field. On load, run ordered migration functions until the data reaches the current
version, then reconcile defaults. Never delete fields in the same release that stops writing them;
never reuse field names with different meanings.

```luau
--!strict
type Data = { [string]: any }

local MIGRATIONS: { (Data) -> () } = {
	[1] = function(data) -- v1 -> v2: "gold" renamed to "coins"
		data.coins = data.gold or 0
		data.gold = nil
	end,
	[2] = function(data) -- v2 -> v3: inventory list -> counts
		local counts: { [string]: number } = {}
		for _, itemId in data.inventory or {} do
			counts[itemId] = (counts[itemId] or 0) + 1
		end
		data.inventory = counts
	end,
}
local CURRENT_VERSION = #MIGRATIONS + 1

local function migrate(data: Data): Data
	local version = data.version or 1
	while version < CURRENT_VERSION do
		MIGRATIONS[version](data)
		version += 1
	end
	data.version = CURRENT_VERSION
	return data
end

print(migrate({ gold = 5, inventory = { "Sword", "Sword" } }))
```

## Leaderboards (OrderedDataStore)

- Values must be integers. Write on a schedule or on meaningful change, not every increment.
- Read top N with `GetSortedAsync(false, 100)` on **one** server loop (e.g. every 60 s), cache the
  result, and replicate to clients. Don't let every server/client read constantly.
- For "this week" boards, include the period in the store name (`Wins_2026W39`) or use a MemoryStore sorted map.

## MemoryStore essentials

- Quotas are experience-wide: memory `64 KB + 1.2 KB × users`; requests `1000 + 120 × CCU` units/min.
- `MemoryStoreSortedMap`: ranked data, server browsers, live leaderboards (`SetAsync` with expiration,
  `GetRangeAsync`, `UpdateAsync`).
- `MemoryStoreQueue`: matchmaking/work queues (`AddAsync`, `ReadAsync` + `RemoveAsync` with the returned id
  after successful processing, invisibility timeout for crash safety).
- `MemoryStoreHashMap`: high-volume key-value without sorting (`SetAsync`, `GetAsync`, `UpdateAsync`, `ListItemsAsync`).
- Always set expirations; handle throttling (`pcall` + retry); keep items small.

## MessagingService essentials

- Message ≤ 1 kB. Per server: `600 + 240 × players` sends/min; `20 + 8 × players` subscriptions.
- Delivery is **best effort** and not ordered: use it for notifications ("refresh your cache",
  global announcements), never as the source of truth. Pair with DataStore/MemoryStore for state.
- Wrap `SubscribeAsync`/`PublishAsync` in `pcall`; they can fail or yield.

More code (MemoryStore queue matchmaking, cross-server announcement, RTBF): [references/memory-and-messaging.md](references/memory-and-messaging.md).

## Right to be forgotten

Use static key patterns so **automated RTBF** (configured in Creator Dashboard) can delete player data
templates like `PlayerData/User_{userId}`. Otherwise handle the right-to-erasure webhook (see
`roblox-open-cloud`). Link keys to user IDs: `SetAsync(key, value, { userId })`, return them as the second value from an
`UpdateAsync` transform, or call ProfileStore's `AddUserId`.

## Related skills

`roblox-security` (duplication and trade exploits), `roblox-monetization` (receipts),
`roblox-open-cloud` (external access, bulk operations), `roblox-teleport-matchmaking`.
