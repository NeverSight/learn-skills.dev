---
name: roblox-luau
description: Modern, type-safe Luau for Roblox, covering --!strict and the new type solver, generics, string interpolation, if-expressions, task library, require-by-string, module/OOP patterns, error handling with retries, buffer/vector, and legacy APIs to avoid. Use when writing, refactoring, or explaining any Roblox script, fixing type errors, or modernizing old Lua code.
---

# Modern Luau for Roblox

Luau is Roblox's gradually-typed Lua 5.1 derivative. Engine and language move fast; many
patterns from older tutorials (and older training data) are deprecated. Apply these defaults
to **every** script you write unless the project clearly uses another convention.

## Defaults for all generated code

1. `--!strict` at the top of new ModuleScripts (and Scripts when practical). Type public functions.
2. Get services with `game:GetService("Name")` at the top of the file, never `game.Name`.
3. Use the `task` library: `task.wait`, `task.spawn`, `task.defer`, `task.delay`, `task.cancel`.
   Never `wait`, `spawn`, `delay` (deprecated, throttled, imprecise).
4. Yielding engine calls that can fail (DataStore, HTTP, Marketplace, Teleport, `*Async`) go inside `pcall`.
5. Prefer the `*Async` variants of APIs; Roblox renamed most yielding methods
   (`LoadCharacterAsync`, `GetProductInfoAsync`, `UserHasBadgeAsync`, ...). See the table below.
6. Disconnect connections / destroy instances you create (see "Cleanup" below).
7. Naming: `PascalCase` for services, modules, classes, types, and instance names;
   `camelCase` for locals and functions; `SCREAMING_SNAKE_CASE` for constants.
8. Tabs for indentation (StyLua default in the Roblox ecosystem), double quotes.

## Modern syntax cheat sheet

```luau
local Players = game:GetService("Players")

local count = 0
count += 1 -- compound assignment: += -= *= /= //= %= ^= ..=

local label = if count > 1 then "many" else "one" -- if-expression (no `and/or` pitfalls)
print(`Player count: {#Players:GetPlayers()} ({label})`) -- string interpolation

for index, player in Players:GetPlayers() do -- generalized iteration: no pairs/ipairs needed
	if player.AccountAge < 1 then
		continue -- continue is a keyword
	end
	print(index, player.Name)
end

local half = 7 // 2 -- floor division → 3
local frozen = table.freeze({ Speed = 16 }) -- read-only table; writes throw
local list = table.create(100, 0) -- preallocated array
local copy = table.clone(frozen) -- shallow copy (unfrozen)
local mid = math.lerp(0, 10, 0.5) -- also: math.map, math.clamp, math.round, math.sign
print(half, list[1], copy.Speed, mid)
```

- `pairs`/`ipairs` still work; generalized iteration is preferred and iterates arrays in order.
- `#t` is only defined for arrays without holes. Setting `t[i] = nil` in the middle creates holes.
- Numbers are doubles: integers are exact to 2^53. Use `math.floor`/`//` for integer math.
- `tick()` is discouraged: use `os.clock()` for benchmarks, `workspace:GetServerTimeNow()` for
  synced time across clients/server, `os.time()`/`DateTime.now()` for wall-clock UTC.

## Types (new type solver)

Roblox's **new type solver** is generally available (Nov 2025) and `Workspace.UseNewLuauTypeSolver`
controls it; `Workspace.LuauTypeCheckMode` sets the default mode. Write code that checks cleanly
under `--!strict`.

```luau
--!strict
export type Item = {
	id: string,
	name: string,
	stack: number,
	tags: { string }?, -- optional field
}

type Rarity = "Common" | "Rare" | "Legendary" -- singleton (literal) union

local function totalStack(items: { Item }, filter: ((Item) -> boolean)?): number
	local total = 0
	for _, item in items do
		if filter == nil or filter(item) then
			total += item.stack
		end
	end
	return total
end

local function first<T>(list: { T }): T? -- generics
	return list[1]
end

local rarity: Rarity = "Rare"
local part = workspace:FindFirstChild("Door") :: BasePart? -- cast with ::
print(totalStack({}, nil), first({ 1, 2 }), rarity, part)
```

- Refine before use: `if part then ... end`, `if typeof(x) == "Instance" and x:IsA("BasePart") then`.
- `typeof(v)` knows Roblox types (`"Vector3"`, `"Instance"`, ...); `type(v)` only knows Lua types.
- Instance types come from `IsA` refinement or `FindFirstChildOfClass`/`FindFirstChildWhichIsA`.
- Avoid `any` except at trust boundaries (remote payloads, decoded JSON) — validate there, then narrow.

Details: generics, type packs, `read`/`write` properties, user-defined type functions, typing
OOP classes, and migrating legacy code to strict: [references/type-system.md](references/type-system.md).

## Modules and require

ModuleScripts run once per environment (server or each client) and return one value, cached for every
later `require`. A module in `ReplicatedStorage` required by both sides runs twice, once per side, with
separate state.

```luau
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Signal = require(ReplicatedStorage.Packages.Signal) -- instance path (always works)
local Config = require("./Config") -- require-by-string: sibling of this script (script.Parent)
local Utils = require("@self/Utils") -- child of this script
local Shared = require("@game/ReplicatedStorage/Shared") -- absolute from game
print(Signal, Config, Utils, Shared)
```

- String paths: `./` = `script.Parent`, `../` = `script.Parent.Parent`, `@self/` = `script`,
  `@game/` = `game`. They **do not wait** for instances to exist. Use instance paths with
  `WaitForChild` when the module may not have replicated yet.
- Never create circular requires; they deadlock/error. Break cycles with dependency injection or events.
- Don't yield at module top level (no `WaitForChild` chains on things that may never exist, no
  DataStore calls): every requirer blocks until the module returns.

### Module / class pattern

```luau
--!strict
local Counter = {}
Counter.__index = Counter

export type Counter = typeof(setmetatable({} :: { value: number, step: number }, Counter))

function Counter.new(step: number?): Counter
	return setmetatable({ value = 0, step = step or 1 }, Counter)
end

function Counter.increment(self: Counter): number
	self.value += self.step
	return self.value
end

return Counter
```

Prefer plain modules of functions + data tables over deep inheritance. Use composition.

## Errors and retries

```luau
local DataStoreService = game:GetService("DataStoreService")
local store = DataStoreService:GetDataStore("PlayerData")

local function retry<T...>(attempts: number, fn: () -> T...): (boolean, T...)
	local delaySeconds = 1
	for attempt = 1, attempts do
		local result = table.pack(pcall(fn))
		if result[1] then
			return table.unpack(result, 1, result.n)
		end
		if attempt < attempts then
			warn(`attempt {attempt} failed: {result[2]}`)
			task.wait(delaySeconds)
			delaySeconds *= 2 -- exponential backoff
		end
	end
	return false
end

local ok, data = retry(3, function()
	return store:GetAsync("Player_1")
end)
print(ok, data)
```

- `error("message", 2)` blames the caller; `error({ code = "X" })` throws a table for structured errors.
- `xpcall(fn, debug.traceback)` keeps the stack trace.
- Don't wrap everything in `pcall` — only calls that can fail for reasons outside your code.

## Concurrency: the task library

| Call | Behavior |
| --- | --- |
| `task.spawn(fn, ...)` | Run now (until first yield) on a new thread. |
| `task.defer(fn, ...)` | Run at the end of the current resumption cycle. Good for "after this finishes". |
| `task.delay(t, fn, ...)` | Run after `t` seconds. Returns a thread you can `task.cancel`. |
| `task.wait(t?)` | Yield ≥ `t` seconds (one frame if omitted); returns elapsed time. |
| `task.cancel(thread)` | Stop a spawned/delayed thread. |
| `task.desynchronize()` / `task.synchronize()` | Parallel Luau (inside Actors) — see `roblox-performance`. |

- Per-frame work: `RunService.Heartbeat` (after physics), `RunService.PreSimulation`/`PostSimulation`,
  `RunService:BindToRenderStep` (client, before render, ordered). Don't `while true do task.wait() end` for
  per-frame logic; connect to an event and use its `deltaTime`.
- Write handlers that work under **deferred** signal behavior (`Workspace.SignalBehavior`): handlers run
  later in the frame, not inline. New template places use `Deferred`, `Default` will switch to it, and
  server authority requires it. Don't rely on handler side effects being visible right after `:Fire()`.
- Never yield inside metamethods or `Changed`-style callbacks that must be synchronous.

## Cleanup (memory leaks are the #1 Roblox bug)

```luau
local Players = game:GetService("Players")

local connections: { RBXScriptConnection } = {}

table.insert(
	connections,
	Players.PlayerRemoving:Connect(function(player)
		print(`{player.Name} left`)
	end)
)

local function cleanup()
	for _, connection in connections do
		connection:Disconnect()
	end
	table.clear(connections)
end

cleanup()
```

- `Instance:Destroy()` disconnects that instance's connections and locks `Parent`; it does **not**
  clear your Lua references — nil out tables that hold players/instances on `PlayerRemoving`.
- Use `:Once()` for one-shot connections. Use a Trove/Janitor/Maid-style helper for groups.
- Keys that are Player/Instance objects in long-lived tables leak unless removed on leave/destroy.

## Buffers and vectors (performance-sensitive data)

```luau
local packet = buffer.create(10)
buffer.writeu16(packet, 0, 513) -- item id
buffer.writef32(packet, 2, 12.5) -- amount
buffer.writei32(packet, 6, -4)
print(buffer.readu16(packet, 0), buffer.readf32(packet, 2), buffer.len(packet))

local v = vector.create(1, 2, 3) -- native 3-float vector (same type as Vector3 at runtime)
print(vector.magnitude(v), vector.normalize(v), vector.dot(v, vector.one))
```

`buffer` is the right tool for compact network payloads, large grids, and binary serialization.
Standard-library quick reference: [references/stdlib-cheatsheet.md](references/stdlib-cheatsheet.md).

## Legacy → current (most common mistakes)

| Don't write | Write instead |
| --- | --- |
| `wait()`, `spawn()`, `delay()` | `task.wait()`, `task.spawn()`, `task.delay()` |
| `game.Workspace`, `game.Players` | `workspace`, `game:GetService("Players")` |
| `Instance.new("Part", parent)` | create, set properties, **then** set `.Parent` last |
| `Humanoid:LoadAnimation()` | `Animator:LoadAnimation()` |
| `Model:SetPrimaryPartCFrame()` | `Model:PivotTo()` / `Model:GetPivot()` |
| `workspace:FindPartOnRay(Ray.new(...))` | `workspace:Raycast(origin, direction, params)` |
| `BodyVelocity`, `BodyPosition`, `BodyGyro` | `LinearVelocity`, `AlignPosition`, `AlignOrientation` |
| `player:LoadCharacter()` | `player:LoadCharacterAsync()` |
| `MarketplaceService:GetProductInfo()` | `:GetProductInfoAsync()` |
| `BadgeService:AwardBadge()` | `:AwardBadgeAsync()` |
| `player:GetRankInGroup()` | `GroupService:GetRolesInGroupAsync()` / `player:IsInGroupAsync()` |
| `TeleportService:Teleport*()` variants | `TeleportService:TeleportAsync()` |
| `Chat` service / `ChatService` modules | `TextChatService` |
| `GuiObject.Draggable` | `UIDragDetector` |
| `table.getn`, `table.foreach`, `getfenv` | `#t`, `for ... in`, nothing |

The full deprecation map lives in the `roblox-code-review` skill.

## Performance idioms (only where it matters)

- Measure first (`debug.profilebegin/profileend`, MicroProfiler, Script Profiler).
- `--!native` at the top of a script, or `@native` on a function, compiles hot numeric code natively.
  Use it on math-heavy modules, not everywhere (compile time + memory limits). Type annotations help it.
- Cache `Instance` lookups and service references outside loops; avoid `FindFirstChild` chains per frame.
- Build large strings with `table.concat` or `buffer`, not repeated `..` in loops.
- Reuse `RaycastParams`/`OverlapParams` objects instead of creating them per call.

## Related skills

`roblox-architecture` (project structure, client/server), `roblox-networking` (remotes),
`roblox-performance` (profiling, Parallel Luau), `roblox-code-review` (review checklist, full deprecation map).
