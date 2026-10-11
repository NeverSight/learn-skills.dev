---
name: roblox-security
description: Anti-exploit design - never trust the client, validate every remote argument (NaN, spoofed instances, strings), rate limiting, ProximityPrompt/ClickDetector abuse, network ownership, movement and hit validation, economy/trade duplication, code confidentiality, secure teleports, heuristics, Ban API. Use when writing server handlers for client input, combat/economy/trading, or reviewing for exploits.
---

# Roblox security

**Exploiters fully control their client**: they can run any Luau, read every replicated script
(decompiled), fire any remote with any arguments at any rate, edit any local property (WalkSpeed,
prompt `Enabled`, `MaxActivationDistance`), and move anything they have network ownership of.
Client-side anti-cheat is at best a speed bump. Security comes from server design.

## Core rules

1. **The server decides.** Clients send *intent* ("I pressed attack aiming here"), never *results*
   ("I dealt 50 damage", "give me 100 coins").
2. **Validate every argument** of every `OnServerEvent`/`OnServerInvoke`: type, structure, range, finiteness.
3. **Validate context**: is the player alive, in range, not on cooldown, owns the item, allowed to act?
4. **Rate limit** everything a client can trigger (remotes, prompts, touches, clicks).
5. **Keep secrets server-side**: server code in `ServerScriptService`/`ServerStorage`; API keys via
   `HttpService:GetSecret()`; never ship unreleased content to production places.
6. **Prefer silent mitigation** (drop, clamp, correct state) over instant kicks; escalate on repeated signals.

## Argument validation toolkit

```luau
--!strict
-- ServerScriptService/Server/Validate.luau
local Validate = {}

function Validate.number(value: unknown, min: number, max: number): number?
	if typeof(value) ~= "number" or not math.isfinite(value) then
		return nil -- rejects NaN and ±inf (NaN fails every comparison, so range checks alone don't catch it)
	end
	if value < min or value > max then
		return nil
	end
	return value
end

function Validate.integer(value: unknown, min: number, max: number): number?
	local n = Validate.number(value, min, max)
	return if n and n == math.floor(n) then n else nil
end

function Validate.string(value: unknown, maxLength: number): string?
	if typeof(value) ~= "string" or #value > maxLength or utf8.len(value) == nil then
		return nil -- also rejects invalid UTF-8 (which DataStores refuse)
	end
	return value
end

function Validate.vector3(value: unknown, maxMagnitude: number): Vector3?
	if typeof(value) ~= "Vector3" then
		return nil
	end
	if not (math.isfinite(value.X) and math.isfinite(value.Y) and math.isfinite(value.Z)) then
		return nil
	end
	return if value.Magnitude <= maxMagnitude then value else nil
end

-- Accept only a real instance of the expected class that lives under a trusted container.
-- Exploiters can send tables shaped like instances ({ ClassName = "Part", ... }).
function Validate.instanceIn(value: unknown, className: string, container: Instance): Instance?
	if typeof(value) ~= "Instance" or not value:IsA(className) or not value:IsDescendantOf(container) then
		return nil
	end
	return value
end

function Validate.enum<T>(value: unknown, allowed: { [T]: boolean }): T?
	if allowed[value :: any] then
		return value :: any
	end
	return nil
end

return Validate
```

- Treat every handler parameter after `player` as `unknown` and narrow it with these helpers.
- Look items up by ID in **server** tables (`ITEMS[itemId]`); never read prices/stats from client data
  or from replicated `NumberValue`s the client could reference.
- Cap table sizes and iterate client tables defensively (keys may be NaN-like, nested, huge).

## Rate limiting (token bucket)

```luau
--!strict
local Players = game:GetService("Players")

type Bucket = { tokens: number, last: number }

local function newLimiter(capacity: number, windowSeconds: number)
	local refillRate = capacity / windowSeconds
	local buckets: { [Player]: Bucket } = {}

	Players.PlayerRemoving:Connect(function(player)
		buckets[player] = nil
	end)

	return function(player: Player): boolean
		local now = os.clock()
		local bucket = buckets[player]
		if not bucket then
			bucket = { tokens = capacity, last = now }
			buckets[player] = bucket
		else
			bucket.tokens = math.min(capacity, bucket.tokens + (now - bucket.last) * refillRate)
			bucket.last = now
		end
		if bucket.tokens >= 1 then
			bucket.tokens -= 1
			return true
		end
		return false
	end
end

local allowAttack = newLimiter(5, 1) -- bursts of 5, refills 5/second
print(allowAttack)
```

Rate-limit expensive or exploitable operations especially: DataStore/Badge/HTTP calls (they have
their own budgets), cloning large models, teleports, currency grants, anything broadcast to all clients.

## Client-triggered instances are not safe

| Object | What exploiters can do | Server must |
| --- | --- | --- |
| `ProximityPrompt` | Fire events while disabled; change distance/line-of-sight/`HoldDuration` locally. Only `Triggered` gets a distance check. | Re-check enabled state, distance from character, alive, cooldown. |
| `ClickDetector` | Fire from any distance even when disabled. No server checks at all. | Same as above. |
| `DragDetector` | Inherited click events unchecked; drag respects only `Enabled` and `PermissionPolicy`. | Validate drag results on the server. |
| `Touched` on client-owned parts | Fake or suppress touches. | Validate with server-side distance/overlap queries. |

If these objects sit in **unanchored** parts the client can own, an exploiter can pull the part to
themselves: anchor them, or `part:SetNetworkOwner(nil)` for server ownership.

## Network ownership and movement

Clients own their character's physics, so they can teleport, fly, noclip, speed hack, fling other
players (NaN/huge velocities), and suppress `Touched`. Options, strongest first:

1. **Server authority** (Workspace `AuthorityMode = Server`; rolling out in 2026 — check current status): the
   server simulates movement with client prediction and rollback, eliminating movement exploits.
   See `roblox-physics`.
2. Server-side movement checks: compare horizontal (XZ) displacement per interval against max speed
   plus latency tolerance; exempt legitimate teleports (set a flag server-side when *you* move them);
   rubber-band to the last valid position instead of kicking.
3. Keep gameplay-critical unanchored parts server-owned: `part:SetNetworkOwner(nil)`.

## Combat validation (hit reports)

Client sends origin, direction/target part, and timestamp. Server checks:
- Origin is near the character's **server** position (tolerance scaled by `player:GetNetworkPing()`).
- Target is alive, an enemy, and within weapon range; claimed hit point is near the target's server position.
- A server raycast against **static** geometry finds no wall between origin and target.
- Fire rate, ammo, reload/sprint state tracked on the server.

## Economy, trading, purchases

- Currency, inventory, and prices exist only on the server. Clients request; the server checks balance
  and applies changes atomically.
- Trades: validate both sides fully, then commit both, then save both; on any failure revert everything.
  Beware "trade then leave before save" duplication: lock items during trades and save immediately after.
- Robux purchases: grant only in `MarketplaceService.ProcessReceipt` (developer products) or after a server
  ownership check (passes). Never trust `PromptProductPurchaseFinished` from the client. See `roblox-monetization`.

## Confidentiality

- Any `LocalScript`, client `Script`, or `ModuleScript` that replicates can be decompiled — even if
  disabled or never required. Don't mix server-only branches into shared modules.
- Anything replicated (models, UI, attributes) can be data-mined. Keep unreleased content in separate
  private universes, not hidden in production.
- Clients can teleport to **any place in the universe**: set **Access Control for Places → Secure within
  universe only** in Creator Dashboard, and verify eligibility on join in restricted places (default deny).
- Never put API keys in scripts or attributes; use the in-experience Secrets store (`HttpService:GetSecret`).

## Detection and consequences

Layer server-side heuristics on top of validation: fastest-possible completion time, rate of resource
gain, inhumanly regular action cadence, honeypot remotes no legit client fires. Accumulate a
suspicion score; act on multiple signals. Ladder: silent logging → quiet mitigation → restrict
features → kick/ban. Delay visible consequences so exploiters can't bisect your checks.

```luau
--!strict
local Players = game:GetService("Players")

local function banForExploiting(player: Player, evidence: string)
	local ok, err = pcall(function()
		Players:BanAsync({
			UserIds = { player.UserId },
			Duration = 7 * 24 * 60 * 60, -- seconds; -1 = permanent
			DisplayReason = "Exploiting detected.", -- shown to the user (max 400 chars, filtered)
			PrivateReason = evidence, -- visible to you only
			ExcludeAltAccounts = false, -- also ban detected alt accounts
			ApplyToUniverse = true,
		})
	end)
	if not ok then
		warn("BanAsync failed:", err)
		player:Kick("Exploiting detected.")
	end
end

return banForExploiting
```

Enable `Players.BanningEnabled` for the Ban API. Prefer reversible, time-limited bans (check
`Players:GetBanHistoryAsync` to escalate); version detection rules and monitor false-positive rates.

Security review checklist and common vulnerable-code patterns: [references/checklist.md](references/checklist.md).

## Related skills

`roblox-networking`, `roblox-physics` (ownership, server authority), `roblox-data-stores`,
`roblox-monetization`, `roblox-code-review`.
