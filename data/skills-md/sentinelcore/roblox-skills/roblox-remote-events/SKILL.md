---
name: roblox-remote-events
description: Use when implementing client-server communication in Roblox, firing events between LocalScripts and Scripts, passing data across the network boundary, syncing game state, or defending against exploits that abuse RemoteEvents or RemoteFunctions.
---

# Roblox Remote Events & Functions

## RemoteEvent vs RemoteFunction

| Type | Direction | Returns value? | Use when |
|---|---|---|---|
| `RemoteEvent` | Any direction | No (fire-and-forget) | Notifying server of player action, broadcasting state |
| `RemoteFunction` | Client→Server | Yes (yields caller) | Client needs a result back (e.g. fetch inventory) |
| `UnreliableRemoteEvent` | Any direction | No | High-frequency updates where dropped packets are fine |

**Default to RemoteEvent.** Avoid server→client `RemoteFunction` — an exploiter's frozen callback stalls your server thread indefinitely.

---

## Where to Put Remotes

Always store Remotes in `ReplicatedStorage`. Create them from a server Script that runs before any LocalScript.

```
ReplicatedStorage/
  Remotes/
    DealDamage        (RemoteEvent)
    GetInventory      (RemoteFunction)
    SyncPosition      (UnreliableRemoteEvent)
```

```lua
-- Script in ServerScriptService
local folder = Instance.new("Folder")
folder.Name = "Remotes"
folder.Parent = game:GetService("ReplicatedStorage")

local function make(class, name)
    local r = Instance.new(class)
    r.Name = name
    r.Parent = folder
    return r
end

make("RemoteEvent",           "DealDamage")
make("RemoteFunction",        "GetInventory")
make("UnreliableRemoteEvent", "SyncPosition")
```

---

## Firing Patterns

### Client → Server (FireServer)

```lua
-- LocalScript
local DealDamage = game:GetService("ReplicatedStorage").Remotes:WaitForChild("DealDamage")
DealDamage:FireServer({ targetId = 12345, amount = 50 })
-- First arg on server is always the firing Player (injected automatically, cannot be spoofed)
```

```lua
-- Script (server) — VALIDATE everything in the payload
DealDamage.OnServerEvent:Connect(function(player, data)
    -- player identity is trustworthy; data contents are not
end)
```

### Server → One Client

```lua
local Notify = game:GetService("ReplicatedStorage").Remotes:WaitForChild("Notify")
Notify:FireClient(player, { message = "Welcome!" })
```

```lua
-- LocalScript
Notify.OnClientEvent:Connect(function(data)
    print(data.message)
end)
```

### Server → All Clients

```lua
AnnounceEvent:FireAllClients({ text = "Game starting in 10 seconds!" })
```

### RemoteFunction (Client Calls, Server Returns)

```lua
-- Script (server)
GetInventory.OnServerInvoke = function(player)
    return getPlayerInventory(player.UserId)
end
```

```lua
-- LocalScript
local inventory = GetInventory:InvokeServer()  -- yields until server returns
```

### UnreliableRemoteEvent (High-Frequency Sync)

```lua
-- LocalScript
RunService.Heartbeat:Connect(function()
    SyncPosition:FireServer(character.HumanoidRootPart.CFrame)
end)
```

```lua
-- Script (server) — still validate
SyncPosition.OnServerEvent:Connect(function(player, cframe)
    if typeof(cframe) ~= "CFrame" then return end
    -- apply with sanity bounds check
end)
```

---

## CRITICAL: Server-Side Security

**The client is hostile. Treat every argument as untrusted input.**

```lua
local MAX_DAMAGE = 100
local COOLDOWNS = {}
local COOLDOWN_SECONDS = 0.5

DealDamage.OnServerEvent:Connect(function(player, data)
    -- 1. Rate limit
    local now = tick()
    if COOLDOWNS[player.UserId] and now - COOLDOWNS[player.UserId] < COOLDOWN_SECONDS then
        return
    end
    COOLDOWNS[player.UserId] = now

    -- 2. Type checks
    if type(data) ~= "table" then return end
    if type(data.targetId) ~= "number" then return end
    if type(data.amount) ~= "number" then return end

    -- 3. Range clamp
    local amount = math.clamp(data.amount, 0, MAX_DAMAGE)

    -- 4. Server-side weapon lookup — never trust client-provided Instance
    local weapon = getEquippedWeapon(player)
    if not weapon then return end

    -- 5. Server-side target lookup
    local target = getPlayerByUserId(data.targetId)
    if not target then return end

    applyDamage(target, amount, player)
end)
```

---

## Exploit Patterns & Defenses

| Exploit | What the attacker does | Defense |
|---|---|---|
| Argument injection | Sends unexpected types to crash handler | Type-check all arguments |
| Damage amplification | Sends `amount = math.huge` | Clamp to sane maximum |
| Remote spam | Fires thousands of times per second | Per-player cooldown |
| Spoofed target | Sends another player's UserId | Server resolves from its own state |
| Infinite yield | Never returns from `OnClientEvent` callback | Avoid server→client RemoteFunction |
| Duplicate action | Replays a valid fire to buy twice | Check state / consume token before acting |

---

## Quick Reference

```
FireServer(args)            LocalScript → server
FireClient(player, args)    server → one client
FireAllClients(args)        server → every client
InvokeServer(args)          LocalScript → server, waits for return
OnServerEvent               server-side listener for FireServer
OnClientEvent               client-side listener for FireClient/FireAllClients
OnServerInvoke              server-side function assigned for InvokeServer
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| `OnServerEvent` in a LocalScript | Use `OnClientEvent` on client; `OnServerEvent` is server-only |
| Remotes in ServerStorage | Move to ReplicatedStorage |
| Trusting payload beyond player identity | Validate every field in the payload |
| Server→client RemoteFunction | Use RemoteEvent; frozen client stalls server thread |
| No `WaitForChild` in LocalScript | Remotes may not exist yet; always use `WaitForChild` |
| Multiple `OnServerInvoke` assignments | Only the last assignment wins; keep it in one place |
| Firing inside tight loop without throttle | Use `UnreliableRemoteEvent` or accumulate delta time |
