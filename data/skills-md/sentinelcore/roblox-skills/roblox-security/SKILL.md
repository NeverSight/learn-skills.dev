---
name: roblox-security
description: "Use when writing Roblox game scripts that handle player actions, currencies, stats, damage, or any RemoteEvent/RemoteFunction communication. Use when reviewing code for exploitable patterns, implementing anti-cheat logic, validating client requests on the server, or setting up rate limiting."
---

# Roblox Security: Anti-Exploit & Server-Side Validation

## Core Principle

**Never trust the client.** Every LocalScript runs on the player's machine and can be modified. All authoritative logic — damage, currency, stats, position changes — must live on the server.

FilteringEnabled is always on in modern Roblox. Client-side changes do not replicate to the server or other clients unless the server explicitly applies them.

---

## Secure vs Insecure Patterns

| Pattern | Insecure | Secure |
|---|---|---|
| Dealing damage | LocalScript sets `Humanoid.Health` | Server reduces health after validation |
| Awarding currency | LocalScript increments leaderstats | Server validates action, then increments |
| Leaderstats ownership | LocalScript owns the IntValue | Server creates and owns all leaderstats |
| Position changes | LocalScript teleports character | Server validates and moves character |
| Tool use | Client fires damage on hit | Server raycasts and applies damage |
| Cooldowns | Client tracks cooldown locally | Server tracks cooldown per player |

---

## Secure Leaderstats Setup

```lua
-- Script in ServerScriptService — never LocalScript
game.Players.PlayerAdded:Connect(function(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = leaderstats
end)
```

---

## Server-Side Sanity Checks

### Distance Check

```lua
local MAX_INTERACT_DISTANCE = 10

InteractRemote.OnServerEvent:Connect(function(player, targetPart)
    if typeof(targetPart) ~= "Instance" or not targetPart:IsA("BasePart") then return end

    local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
    if not root then return end

    if (root.Position - targetPart.Position).Magnitude > MAX_INTERACT_DISTANCE then
        warn(player.Name .. " sent interaction from invalid distance")
        return
    end

    processInteraction(player, targetPart)
end)
```

### Cooldown Validation

```lua
local ABILITY_COOLDOWN = 5
local lastUsed = {}

UseAbilityRemote.OnServerEvent:Connect(function(player)
    local now = os.clock()
    if now - (lastUsed[player] or 0) < ABILITY_COOLDOWN then return end
    lastUsed[player] = now
    applyAbility(player)
end)

game.Players.PlayerRemoving:Connect(function(player)
    lastUsed[player] = nil
end)
```

### Stat Bounds Check

```lua
local MAX_QUANTITY = 99
local ITEM_COST = 50

BuyItemRemote.OnServerEvent:Connect(function(player, quantity)
    if type(quantity) ~= "number" then return end
    quantity = math.clamp(math.floor(quantity), 1, MAX_QUANTITY)

    local coins = player.leaderstats.Coins
    if coins.Value < ITEM_COST * quantity then return end

    coins.Value = coins.Value - (ITEM_COST * quantity)
    -- award items server-side
end)
```

---

## Rate Limiting

```lua
local RATE_LIMIT = 10   -- max calls
local RATE_WINDOW = 1   -- per second
local callLog = {}

local function isRateLimited(player)
    local now = os.clock()
    local log = callLog[player] or {}
    local pruned = {}
    for _, t in ipairs(log) do
        if now - t < RATE_WINDOW then table.insert(pruned, t) end
    end
    if #pruned >= RATE_LIMIT then
        callLog[player] = pruned
        return true
    end
    table.insert(pruned, now)
    callLog[player] = pruned
    return false
end

ActionRemote.OnServerEvent:Connect(function(player)
    if isRateLimited(player) then return end
    handleAction(player)
end)

game.Players.PlayerRemoving:Connect(function(player)
    callLog[player] = nil
end)
```

---

## Argument Validation Utility

```lua
-- ServerScriptService/Modules/Validate.lua
local Validate = {}

function Validate.number(value, min, max)
    if type(value) ~= "number" then return false end
    if value ~= value then return false end -- NaN check
    if min and value < min then return false end
    if max and value > max then return false end
    return true
end

function Validate.instance(value, className)
    if typeof(value) ~= "Instance" then return false end
    if className and not value:IsA(className) then return false end
    return true
end

function Validate.string(value, maxLength)
    if type(value) ~= "string" then return false end
    if maxLength and #value > maxLength then return false end
    return true
end

return Validate
```

```lua
-- Usage
local Validate = require(script.Parent.Modules.Validate)

remote.OnServerEvent:Connect(function(player, amount, targetPart)
    if not Validate.number(amount, 1, 100) then return end
    if not Validate.instance(targetPart, "BasePart") then return end
    -- safe to proceed
end)
```

---

## Speed / Anti-Cheat Detection

```lua
local SPEED_LIMIT = 32
local violations = {}

task.spawn(function()
    while true do
        task.wait(2)
        for _, player in ipairs(game.Players:GetPlayers()) do
            local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
            if root and root.AssemblyLinearVelocity.Magnitude > SPEED_LIMIT then
                violations[player] = (violations[player] or 0) + 1
                if violations[player] >= 3 then
                    player:Kick("Cheating detected.")
                end
            else
                violations[player] = math.max(0, (violations[player] or 0) - 1)
            end
        end
    end
end)
```

---

## ModuleScript Placement

```
ServerScriptService/
  Modules/
    DamageCalculator.lua   -- server-only, never exposed to client
    EconomyManager.lua     -- server-only

ReplicatedStorage/
  Remotes/                 -- RemoteEvent/RemoteFunction instances only
  SharedModules/           -- non-sensitive utilities only
```

Never put currency, damage, or DataStore logic in `ReplicatedStorage` modules — clients can `require()` them.

---

## Common Mistakes

| Mistake | Why It's Exploitable | Fix |
|---|---|---|
| `FireServer(damage)` with server trusting it | Client sends any value | Server calculates damage from its own tool data |
| Currency in LocalScript variable | Client can modify memory | Server-owned only |
| Client-side distance check before firing | Check is bypassable | Server re-checks after receiving event |
| No cooldown on RemoteEvent handlers | Spam = infinite resources | Per-player cooldown on server |
| Trusting `WalkSpeed` set by client | Client sets arbitrarily high | Server owns and caps WalkSpeed |
| Sensitive logic in ReplicatedStorage module | Clients can require it | Move to ServerScriptService |
