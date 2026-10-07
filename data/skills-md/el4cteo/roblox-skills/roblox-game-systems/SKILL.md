---
name: roblox-game-systems
description: Recipes for common systems built on server authority - currency service and leaderstats, XP/levels, round loops with intermission and teams, validated melee/ranged combat, inventory and tools, soft-currency shops, obby checkpoints, daily rewards, pets. Use when implementing or reviewing gameplay systems such as rounds, combat, weapons, inventories, shops, currencies, or progression.
---

# Game systems recipes

Every recipe follows the same contract:
1. **State lives on the server** in a service module; persistent parts go through the data layer
   (`roblox-data-stores`).
2. **Clients send intents** through validated, rate-limited remotes (`roblox-security`,
   `roblox-networking`) and render state they receive (attributes, snapshots/deltas).
3. **Config is data**: tunables in a shared/server config module (or live `ConfigService` configs).
4. **Lifecycle-safe**: handles late joiners, respawns, leaving mid-action, and server shutdown.

| System | Reference |
| --- | --- |
| Leaderstats, currency service, XP/levels, daily rewards, obby checkpoints | [references/progression.md](references/progression.md) |
| Round loop (intermission → match → results), teams, spawning | [references/round-system.md](references/round-system.md) |
| Melee and ranged combat with server validation, cooldowns, damage attribution | [references/combat.md](references/combat.md) |
| Inventory, equipping tools, shop purchases (soft currency), pets that follow | [references/inventory-shop.md](references/inventory-shop.md) |

## Currency service (the pattern every economy uses)

```luau
--!strict
-- ServerScriptService/Server/Services/CurrencyService.luau
local Players = game:GetService("Players")

type Balances = { [Player]: number }

local MAX_BALANCE = 1e12

local CurrencyService = {}
local balances: Balances = {}

local function publish(player: Player)
	player:SetAttribute("Coins", balances[player]) -- replicated to every client; UI listens
end

function CurrencyService.load(player: Player, saved: number?)
	balances[player] = math.clamp(saved or 0, 0, MAX_BALANCE)
	publish(player)
end

function CurrencyService.get(player: Player): number
	return balances[player] or 0
end

-- Positive amount only; returns the new balance.
function CurrencyService.add(player: Player, amount: number, _source: string): number?
	local balance = balances[player]
	if balance == nil or not math.isfinite(amount) or amount <= 0 then
		return nil
	end
	balances[player] = math.min(balance + math.floor(amount), MAX_BALANCE)
	publish(player)
	return balances[player]
end

-- Atomic check-and-spend; false if insufficient.
function CurrencyService.spend(player: Player, amount: number, _sink: string): boolean
	local balance = balances[player]
	if balance == nil or not math.isfinite(amount) or amount <= 0 or balance < amount then
		return false
	end
	balances[player] = balance - math.floor(amount)
	publish(player)
	return true
end

Players.PlayerRemoving:Connect(function(player)
	balances[player] = nil -- after the data layer has saved it
end)

return CurrencyService
```

- One module owns each resource; nothing else writes it. Log sources/sinks to analytics
  (`roblox-analytics-liveops`).
- The in-memory balance is saved by the data layer (ProfileStore `profile.Data.coins`) — or make the
  profile table the balance store directly.
- For display, clients read `player:GetAttribute("Coins")` and `GetAttributeChangedSignal("Coins")`.
  `leaderstats` (a Folder with `IntValue`s under the player) shows values in the player list.

## Design checklist for any new system

- [ ] Where does authoritative state live, and how is it persisted?
- [ ] What can the client request, and how is each request validated and rate-limited?
- [ ] What happens on join mid-session, respawn, leave, teleport, and server shutdown?
- [ ] How is it tuned (config) and measured (analytics)?
- [ ] How does it behave with 1 player, full servers, and high latency?
- [ ] Is it streaming-safe on the client?

## Related skills

`roblox-architecture`, `roblox-security`, `roblox-data-stores`, `roblox-networking`,
`roblox-characters-animation`, `roblox-monetization`, `roblox-ui`.
