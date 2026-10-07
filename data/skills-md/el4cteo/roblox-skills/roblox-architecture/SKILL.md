---
name: roblox-architecture
description: Roblox project structure and client/server model - replication, where code and assets belong (ServerScriptService, ReplicatedStorage, StarterPlayer), RunContext, service/controller bootstrapping, player/character lifecycle, CollectionService components, attributes, streaming-safe client code, library choices. Use when starting a project, deciding where code goes, or fixing replication/streaming bugs.
---

# Roblox game architecture

## The model in one paragraph

Every Roblox game is a **server** (authoritative, runs `Script`s, sees everything, owns DataStores)
plus one **client** per player (runs `LocalScript`s / client `Script`s, renders, reads input).
The server's DataModel **replicates** to clients automatically. Client changes do **not** replicate
back, except: physics of parts the client has network ownership of (its character by default),
its own `Humanoid` state/animations, and remote calls. Assume every client is compromised
(see `roblox-security`). Design every feature as: *client requests → server validates and
decides → state replicates → clients render*.

## Where things go

| Container | Runs/visible on | Put here |
| --- | --- | --- |
| `ServerScriptService` | Server only | Server `Script`s and server-only ModuleScripts (game logic, data, anti-cheat). |
| `ServerStorage` | Server only | Server-only assets: maps, NPC templates, tools to clone, secrets-adjacent config. |
| `ReplicatedStorage` | Both | Shared modules (types, config, pure utils), `RemoteEvent`s, assets clients clone. |
| `ReplicatedFirst` | Client, first | Loading screen only. Replicates before everything else. |
| `StarterPlayer.StarterPlayerScripts` | Client (copied once to `PlayerScripts`) | Client entry point and controllers. |
| `StarterPlayer.StarterCharacterScripts` | Client (copied per spawn into character) | Per-character client scripts (rarely needed). |
| `StarterGui` | Client (copied to `PlayerGui`) | `ScreenGui`s. Set `ResetOnSpawn = false` unless you want reset on death. |
| `Workspace` | Both (streamed to clients) | The 3D world only. Not a place for code or templates. |
| `Lighting`, `SoundService`, `Teams`, `TextChatService` | Both | Their respective config objects. |

Rules:
- Code in `ReplicatedStorage` is **downloadable by exploiters**. Never put server logic, secrets,
  admin lists, or anti-cheat thresholds there.
- `Script.RunContext`: `Legacy` (default: behavior depends on the container), `Server`, `Client`, or
  `Plugin`. A non-Legacy RunContext makes a `Script` run **regardless of container** (e.g. a `Client`
  Script in `ReplicatedStorage` runs on every client) — so templates you clone must not contain such
  scripts unintentionally. Legacy `Script`s don't run in `ReplicatedStorage`/`ServerStorage`.

## Project layout (Rojo-style, recommended)

```text
src/
  server/            -> ServerScriptService.Server   (init.server.luau = entry point)
    Services/        -> one ModuleScript per system (DataService, CombatService, ...)
  client/            -> StarterPlayer.StarterPlayerScripts.Client (init.client.luau)
    Controllers/     -> one ModuleScript per client system (InputController, UIController, ...)
  shared/            -> ReplicatedStorage.Shared (types, config, pure logic, network definitions)
Packages/            -> ReplicatedStorage.Packages (Wally/pesde dependencies)
ServerPackages/      -> ServerScriptService.ServerPackages
```

One entry script per side, everything else is a ModuleScript. This gives deterministic load order,
testable modules, and a single place to wire dependencies. Roblox's own recommendation is equivalent:
one `Script` (`RunContext = Server`) in `ServerScriptService` and one `Script` (`RunContext = Client`) in
`ReplicatedStorage`, each requiring modules and calling their `start()`. Tooling setup: `roblox-tooling`.

## Bootstrapping services (no framework needed)

```luau
--!strict
-- ServerScriptService/Server/init.server.luau
type Service = {
	init: ((self: Service) -> ())?, -- sync setup; may reference other services; must not yield
	start: ((self: Service) -> ())?, -- runs after every init; may yield / connect events
}

local servicesFolder = script:WaitForChild("Services")
local services: { [string]: Service } = {}

for _, module in servicesFolder:GetChildren() do
	if module:IsA("ModuleScript") then
		services[module.Name] = (require :: any)(module)
	end
end

for name, service in services do
	if service.init then
		debug.setmemorycategory(name)
		service:init()
		debug.resetmemorycategory()
	end
end

for name, service in services do
	if service.start then
		task.spawn(function()
			debug.setmemorycategory(name)
			service:start()
		end)
	end
end
```

- Services reference each other with plain `require` (no cycles) or receive dependencies in `init`.
- The client mirrors this with `Controllers`. Keep names symmetrical (`ShopService` / `ShopController`).
- Frameworks like Knit are unnecessary for this; if a project already uses one, follow its conventions.

## Player and character lifecycle

```luau
--!strict
local Players = game:GetService("Players")

local function onCharacterAdded(player: Player, character: Model)
	local humanoid = character:WaitForChild("Humanoid") :: Humanoid
	humanoid.Died:Once(function()
		print(`{player.Name} died`)
	end)
end

local function onPlayerAdded(player: Player)
	-- Load data first (see roblox-data-stores), then set up character handling.
	if player.Character then
		task.spawn(onCharacterAdded, player, player.Character)
	end
	player.CharacterAdded:Connect(function(character)
		onCharacterAdded(player, character)
	end)
end

local function onPlayerRemoving(player: Player)
	-- Save data, release session locks, clear every table keyed by this player.
	print(`{player.Name} left`)
end

Players.PlayerAdded:Connect(onPlayerAdded)
Players.PlayerRemoving:Connect(onPlayerRemoving)
for _, player in Players:GetPlayers() do -- players who joined before this script connected
	task.spawn(onPlayerAdded, player)
end

game:BindToClose(function()
	-- Server shutdown: flush saves for remaining players (max ~30 s total).
end)
```

- Always handle players/characters that already exist when your code starts.
- Characters respawn: anything bound to a character must be re-created on `CharacterAdded`.
- On the client, character descendants may not exist yet (streaming): `WaitForChild` them.

## Components with CollectionService tags

Tag instances (Studio **Tags** section or `CollectionService:AddTag`) and attach behavior in code.
This scales better than copying scripts into every model and works with streaming because the
added/removed signals fire as instances stream in and out.

```luau
--!strict
local CollectionService = game:GetService("CollectionService")

local TAG = "KillBrick"
local cleanups: { [Instance]: () -> () } = {}

local function onAdded(instance: Instance)
	if not instance:IsA("BasePart") then
		return
	end
	local connection = instance.Touched:Connect(function(hit)
		local humanoid = hit.Parent and hit.Parent:FindFirstChildOfClass("Humanoid")
		if humanoid then
			humanoid.Health = 0
		end
	end)
	cleanups[instance] = function()
		connection:Disconnect()
	end
end

local function onRemoved(instance: Instance)
	local cleanup = cleanups[instance]
	if cleanup then
		cleanup()
		cleanups[instance] = nil
	end
end

CollectionService:GetInstanceAddedSignal(TAG):Connect(onAdded)
CollectionService:GetInstanceRemovedSignal(TAG):Connect(onRemoved)
for _, instance in CollectionService:GetTagged(TAG) do
	task.spawn(onAdded, instance)
end
```

Configure components with **attributes** (`instance:GetAttribute("Damage")`,
`GetAttributeChangedSignal`) instead of `IntValue`/`StringValue` children. Attributes replicate
server → client, are cheaper, and show in the Properties panel.

## Sharing state

| Need | Use |
| --- | --- |
| Small per-instance/per-player values visible to clients | Attributes on the instance / `Player` (server sets). |
| Events and requests | `RemoteEvent` / `UnreliableRemoteEvent` (see `roblox-networking`). |
| Large or per-player private state (inventory, quests) | Server-owned tables + remotes that send snapshots/diffs to that player only. |
| Same-side communication | Module function calls or a typed Signal module — not `BindableEvent`, `_G`, or `shared`. |
| Persistent data | `roblox-data-stores`. Cross-server: MessagingService / MemoryStore. |

## Streaming (on by default for new places)

With `Workspace.StreamingEnabled`, clients only have nearby parts. Client code must:
- `WaitForChild` (with a timeout when it may never arrive) or nil-check anything in `Workspace`.
- Use `ModelStreamingMode = Atomic` for models whose parts scripts need together;
  `Persistent` only when a model must always be present (costs memory).
- Treat `GetChildren`, raycasts, and property reads of streamed-out parts as partial/stale; do full-world
  queries on the server.
- Pre-stream destinations on the server with `player:RequestStreamAroundAsync(position)` before teleporting a character.

Full pattern catalog and recommended Workspace settings: [references/streaming.md](references/streaming.md).

## Anti-patterns

- Dozens of loose `Script`s inside parts/models (use tags + one service).
- Polling loops (`while task.wait(0.1) do check() end`) instead of events or `Heartbeat` with `deltaTime`.
- Trusting the client for game state, or firing remotes every frame.
- `_G`/`shared` globals, circular requires, yielding at module top level.
- Cloning maps into `Workspace` from the client (client-only copies never get server updates).
- Storing per-player data in the character (it's destroyed on death).

Library ecosystem (signals, cleanup, networking, UI, ECS, data): [references/ecosystem.md](references/ecosystem.md).

## Related skills

`roblox-networking`, `roblox-security`, `roblox-data-stores`, `roblox-tooling`, `roblox-performance`, `roblox-game-systems`.
