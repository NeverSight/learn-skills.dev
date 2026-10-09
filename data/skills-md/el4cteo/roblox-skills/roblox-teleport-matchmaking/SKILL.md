---
name: roblox-teleport-matchmaking
description: Multi-place and multi-server games - universes and places, TeleportAsync with TeleportOptions (reserved/specific servers, teleport data), retrying failed teleports, secure access control, lobby-to-match flows, parties and queues, Roblox matchmaking with custom signals, server type detection, data handoff. Use when adding lobbies, match servers, dungeons, parties, server browsers, or customizing server selection.
---

# Teleports, places, and matchmaking

## Structure

- A **universe** (experience) contains a start place plus sub-places. All places share DataStores,
  MemoryStores, MessagingService, developer products, and passes.
- Typical layouts: Lobby (start place) → Match place (reserved servers) → back to Lobby; or a hub with
  separate world places. Keep shared code in packages or a shared Rojo tree.
- **Access Control for Places** (Creator Dashboard): `Fully open`, `Limited to same universe`, or
  **`Secure within universe only`** (only server-initiated teleports into non-start places — recommended
  for progression gates and test places). Clients can otherwise teleport themselves anywhere in the universe.

## Teleporting (server)

```luau
--!strict
local TeleportService = game:GetService("TeleportService")

local ATTEMPTS = 5
local RETRY_DELAY = 1
local FLOOD_DELAY = 15

local function safeTeleport(placeId: number, players: { Player }, options: TeleportOptions?): (boolean, any)
	local ok: boolean, result: any = false, nil
	for _ = 1, ATTEMPTS do
		ok, result = pcall(function()
			return TeleportService:TeleportAsync(placeId, players, options)
		end)
		if ok then
			break
		end
		task.wait(RETRY_DELAY)
	end
	if not ok then
		warn("Teleport failed:", result)
	end
	return ok, result
end

-- A teleport can still fail after TeleportAsync succeeds: retry transient failures.
TeleportService.TeleportInitFailed:Connect(function(player, teleportResult, errorMessage, placeId, options)
	if teleportResult == Enum.TeleportResult.Flooded then
		task.wait(FLOOD_DELAY)
	elseif teleportResult == Enum.TeleportResult.Failure then
		task.wait(RETRY_DELAY)
	else
		warn(`Invalid teleport [{teleportResult.Name}]: {errorMessage}`)
		return
	end
	safeTeleport(placeId, { player }, options)
end)

return safeTeleport
```

`TeleportOptions`:
- `ShouldReserveServer = true` → a new **reserved server** (private, only reachable by access code) —
  ideal for matches, dungeons, and parties. Returns `TeleportAsyncResult` with `ReservedServerAccessCode`
  and `PrivateServerId`.
- `ReservedServerAccessCode = code` → join an existing reserved server (from `ReserveServerAsync(placeId)`
  or a previous result).
- `ServerInstanceId = jobId` → a specific public server (e.g. "join friend's server").
- `SetTeleportData(table)` → non-secure data readable on arrival with `player:GetJoinData().TeleportData`
  (server) or `TeleportService:GetLocalPlayerTeleportData()` (client). **Clients can tamper with it**:
  never trust it for currency, items, or permissions — use DataStores/MemoryStores keyed by user ID
  or by the reserved server's `PrivateServerId`.

Deprecated: `Teleport`, `TeleportToPlaceInstance`, `TeleportToPrivateServer`, `TeleportPartyAsync`,
`TeleportToSpawnByName`, `ReserveServer` → `TeleportAsync` + `TeleportOptions` / `ReserveServerAsync`.

## Data handoff between places

1. Save the player's data **before** teleporting (ProfileStore: end the session / wait for save).
2. The destination loads with session locking (ProfileStore retries while the old server releases).
3. For match parameters (mode, map, team assignments), write a MemoryStore/DataStore entry keyed by
   the reserved server's `PrivateServerId` (or the access code) before teleporting; the match server reads
   `game.PrivateServerId` on start and loads its config.
4. On arrival, `TeleportService:SetTeleportGui(gui)` (client, before teleport) keeps a loading screen
   up across the transition; use `ReplicatedFirst` loading screens on arrival.

## Detecting server type

| Server | `game.PrivateServerId` | `game.PrivateServerOwnerId` |
| --- | --- | --- |
| Public | `""` | `0` |
| Reserved (`ReserveServerAsync`/`ShouldReserveServer`) | non-empty | `0` |
| Private (VIP) server | non-empty | owner's user id |

## Lobby → match flow

1. Players queue in the lobby (party leader invites; party members stored server-side).
2. Queue in a **MemoryStoreQueue** / sorted map by mode and rating (see `roblox-data-stores`), or use
   Roblox matchmaking to fill public servers.
3. When a match forms: write match config to MemoryStore keyed by a new id, `TeleportAsync` all players
   with `ShouldReserveServer = true`, store the returned `PrivateServerId` ↔ match id mapping.
4. Match server: waits for expected players (timeout), runs the round, saves results, teleports everyone
   back to the lobby place (a public server, or the party's lobby via `ServerInstanceId`).

## Roblox matchmaking (which server a joining player gets)

Default matchmaking scores eligible public servers by signals (friends, latency, language, age group,
occupancy...) and picks the highest weighted sum. You can customize it per place in Creator Hub:
- Adjust weights of Roblox signals, or add **custom signals** based on **custom attributes**:
  - Player attributes: values stored in a **DataStore** (e.g. `PlayerElo`), configured in the matchmaking settings.
  - Server attributes: set at runtime with `MatchmakingService:SetServerAttribute(name, value)` (e.g.
    `GameMode`, `ServerLevel`); `InitializeServerAttributesForStudio` for testing.
- Preview scores against mock servers before applying, then apply the configuration to places.
Use it for skill-based public servers; use reserved servers when you need exact team composition.

## Server lifecycle

- `game:BindToClose` for shutdown saves; `game.JobId` identifies the server; soft shutdowns after updates
  (Open Cloud `:restartServers` or "Restart servers for updates") teleport players to fresh servers.
- Server browsers: each server heartbeats `{ jobId, players, mode }` into a MemoryStore sorted map
  (TTL) — see `roblox-data-stores`.

## Related skills

`roblox-data-stores` (session locking, MemoryStore queues), `roblox-security` (access control),
`roblox-game-systems` (round loops), `roblox-open-cloud` (server restarts).
