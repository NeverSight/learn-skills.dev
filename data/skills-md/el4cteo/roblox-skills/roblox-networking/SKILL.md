---
name: roblox-networking
description: Client-server communication - RemoteEvent, UnreliableRemoteEvent, RemoteFunction, what survives serialization, typed remote modules, server validation and rate limiting, bandwidth (deltas, buffers, batching), synced time, Zap/Blink. Use when adding remotes, syncing state to clients, debugging nil/lost remote arguments, or reducing lag and bandwidth.
---

# Roblox networking

## Pick the right channel

| Channel | Delivery | Use for |
| --- | --- | --- |
| `RemoteEvent` | Reliable, ordered | Requests (client→server), game events, UI updates. The default. |
| `UnreliableRemoteEvent` | May drop or reorder; payload ≤ **1000 bytes** (larger payloads are dropped) | Continuous, superseded-by-next data: aim direction, cosmetic VFX, positions of non-physics objects. |
| `RemoteFunction` | Request/response, yields caller | Client→server queries that need an answer (e.g. "can I buy X?"). |
| Attributes / properties | Automatic replication server→client | Persistent state clients read (health, team, round state). |
| Physics replication | Automatic for owned assemblies | Moving parts; see `roblox-physics`. |

Never use `RemoteFunction:InvokeClient`: if the client errors, disconnects, or never returns, the server
throws or **yields forever**. Use a `RemoteEvent` to the client and another back if you need a reply.

## Defining remotes once (typed)

Create remotes on the server; clients wait for them. Centralize names so typos can't happen.

```luau
--!strict
-- ReplicatedStorage/Shared/Net.luau
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local FOLDER_NAME = "Remotes"
local IS_SERVER = RunService:IsServer()

local folder: Instance
if IS_SERVER then
	folder = ReplicatedStorage:FindFirstChild(FOLDER_NAME) or Instance.new("Folder")
	folder.Name = FOLDER_NAME
	folder.Parent = ReplicatedStorage
else
	folder = ReplicatedStorage:WaitForChild(FOLDER_NAME)
end

local function get<T>(className: string, name: string): T
	if IS_SERVER then
		local existing = folder:FindFirstChild(name)
		if existing then
			return existing :: any
		end
		local remote = Instance.new(className)
		remote.Name = name
		remote.Parent = folder
		return remote :: any
	end
	return folder:WaitForChild(name) :: any
end

return {
	RequestPurchase = get("RemoteEvent", "RequestPurchase") :: RemoteEvent,
	InventoryChanged = get("RemoteEvent", "InventoryChanged") :: RemoteEvent,
	AimDirection = get("UnreliableRemoteEvent", "AimDirection") :: UnreliableRemoteEvent,
	GetShopStock = get("RemoteFunction", "GetShopStock") :: RemoteFunction,
}
```

## Server handler template

Every `OnServerEvent`/`OnServerInvoke` handler: **rate limit → type-check every argument → check
game rules → act**. The first parameter is always the real `Player` (Roblox fills it in; it can't be forged).

```luau
--!strict
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Net = require(ReplicatedStorage.Shared.Net)

local ITEM_PRICES: { [string]: number } = { Sword = 100, Shield = 150 }
local MIN_INTERVAL = 0.25
local lastRequest: { [Player]: number } = {}

Net.RequestPurchase.OnServerEvent:Connect(function(player: Player, itemId: unknown)
	local now = os.clock()
	if now - (lastRequest[player] or 0) < MIN_INTERVAL then
		return -- rate limited
	end
	lastRequest[player] = now

	if typeof(itemId) ~= "string" or #itemId > 64 then
		return -- malformed: never trust argument types
	end
	local price = ITEM_PRICES[itemId]
	if not price then
		return -- unknown item
	end
	-- check the player's server-side balance, deduct, grant, then notify:
	Net.InventoryChanged:FireClient(player, { added = itemId })
end)

game:GetService("Players").PlayerRemoving:Connect(function(player)
	lastRequest[player] = nil -- avoid leaking Player keys
end)
```

Full validation toolkit (NaN/inf checks, instance ownership, distance and cooldown checks): `roblox-security`.

## What survives the wire

- Tables are **copied**: identity and metatables are lost; functions become `nil`.
- Don't mix array and dictionary keys in one table; don't put `nil` holes in arrays.
- Non-string dictionary keys (Instances, numbers in sparse tables) are converted to strings — send arrays of pairs instead.
- Instances arrive as `nil` if the receiver can't see them (e.g. `ServerStorage` items, or parts not
  yet streamed in on the client).
- Supported: `nil`, booleans, numbers, strings, tables, `buffer`, Roblox datatypes (`Vector3`, `CFrame`,
  `Color3`, `EnumItem`, ...), and replicated `Instance` references.
- Server→client ordering vs. property replication is not guaranteed: a remote may arrive before or
  after a property change it relates to.

## Bandwidth and CPU

- Send **changes**, not full state (item added, not the whole inventory). Send on change, not per frame.
- Throttle input-driven sends on the client (e.g. aim at most 20 Hz) and still rate-limit on the server.
- Send IDs/enums as small numbers; quantize floats; pack hot, high-frequency data into a `buffer`.
- Batch many small messages into one per frame (queue in a table, flush on `Heartbeat`).
- Server-side `TweenService` replicates every frame and looks jittery: tween on clients instead.
- VFX: the server decides the outcome and fires a minimal event; each client spawns effects locally.
- Profile with the MicroProfiler (`ProcessPackets`, `Allocate Bandwidth and Run Senders`) and the
  Developer Console **Network** tab.

```luau
--!strict
-- Pack a hit notification into 11 bytes instead of a table with string keys.
local function encodeHit(targetId: number, damage: number, position: Vector3): buffer
	local b = buffer.create(11)
	buffer.writeu32(b, 0, targetId)
	buffer.writeu16(b, 4, math.clamp(math.round(damage), 0, 65535))
	buffer.writei16(b, 6, math.clamp(math.round(position.X), -32768, 32767))
	buffer.writei16(b, 8, math.clamp(math.round(position.Z), -32768, 32767))
	buffer.writeu8(b, 10, math.clamp(math.round(position.Y / 4), 0, 255))
	return b
end

local function decodeHit(b: buffer): (number, number, Vector3)
	return buffer.readu32(b, 0),
		buffer.readu16(b, 4),
		Vector3.new(buffer.readi16(b, 6), buffer.readu8(b, 10) * 4, buffer.readi16(b, 8))
end

print(decodeHit(encodeHit(42, 25, Vector3.new(10, 20, 30))))
```

For many remotes with hot paths, schema-driven generators (**Zap**, **Blink**) produce typed,
validated, buffer-packed remotes automatically. Adopt them when profiling shows network cost.

## Time and latency

- `workspace:GetServerTimeNow()` is a synchronized clock on server and clients: send a start timestamp
  and let clients compute progress locally (round timers, cooldown bars, projectiles).
- `player:GetNetworkPing()` returns round-trip network latency in seconds (clients may only query
  `LocalPlayer`); use it to size lag-compensation windows.
- Don't send countdown ticks every second; send the end time once.

More patterns (request/response with timeouts, state snapshots + deltas, per-frame batching, client
prediction): [references/patterns.md](references/patterns.md).

## Related skills

`roblox-security` (validation, anti-exploit), `roblox-architecture` (where remotes live),
`roblox-physics` (network ownership, server authority), `roblox-performance`.
