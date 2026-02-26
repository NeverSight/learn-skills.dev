---
name: roblox-datastores
description: "Use when implementing player data persistence in Roblox, saving/loading player stats or inventory, building leaderboards with ordered datastores, handling data migration between versions, diagnosing data loss issues, or adding auto-save and shutdown-safe data handling with DataStoreService."
---

# roblox-datastores

Reference for Roblox `DataStoreService` — saving, loading, and managing player data on the server.

## Quick Reference

| Method | Signature | Notes |
|---|---|---|
| `GetDataStore` | `DSS:GetDataStore(name, scope?)` | Returns a `GlobalDataStore` |
| `GetOrderedDataStore` | `DSS:GetOrderedDataStore(name, scope?)` | For leaderboards |
| `GetAsync` | `store:GetAsync(key)` | Returns value or nil |
| `SetAsync` | `store:SetAsync(key, value)` | No return value needed |
| `UpdateAsync` | `store:UpdateAsync(key, fn)` | Atomic read-modify-write |
| `RemoveAsync` | `store:RemoveAsync(key)` | Deletes key, returns old value |
| `GetSortedAsync` | `orderedStore:GetSortedAsync(asc, pageSize)` | Returns `DataStorePages` |

---

## Basic Setup

```lua
-- Server Script (ServerScriptService)
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local playerStore = DataStoreService:GetDataStore("PlayerData_v1")

local DEFAULT_DATA = {
    coins = 0,
    level = 1,
    xp = 0,
}
```

---

## Loading Data (GetAsync + pcall)

Always wrap datastore calls in `pcall`. They can fail due to network issues or rate limits.

```lua
local function loadData(player)
    local key = "player_" .. player.UserId
    local success, data = pcall(function()
        return playerStore:GetAsync(key)
    end)

    if success then
        local result = {}
        for k, v in pairs(DEFAULT_DATA) do result[k] = v end
        if data then
            for k, v in pairs(data) do result[k] = v end
        end
        return result
    else
        warn("Failed to load data for", player.Name, ":", data)
        return nil -- signal failure; do not give default data silently
    end
end
```

---

## Saving Data (SetAsync vs UpdateAsync)

Use `SetAsync` for simple overwrites. Use `UpdateAsync` when the value must be based on the current stored value (e.g., incrementing a counter safely across servers).

```lua
-- Simple save
local function saveData(player, data)
    local key = "player_" .. player.UserId
    local success, err = pcall(function()
        playerStore:SetAsync(key, data)
    end)
    if not success then
        warn("Failed to save data for", player.Name, ":", err)
    end
end

-- Atomic increment with UpdateAsync
local function addCoinsAtomic(userId, amount)
    local key = "player_" .. userId
    pcall(function()
        playerStore:UpdateAsync(key, function(current)
            current = current or { coins = 0 }
            current.coins = current.coins + amount
            return current
        end)
    end)
end
```

---

## Retry Logic

```lua
local MAX_RETRIES = 3
local RETRY_DELAY = 2

local function safeGet(store, key)
    for attempt = 1, MAX_RETRIES do
        local success, result = pcall(function()
            return store:GetAsync(key)
        end)
        if success then return true, result end
        warn(string.format("GetAsync attempt %d/%d failed: %s", attempt, MAX_RETRIES, result))
        if attempt < MAX_RETRIES then task.wait(RETRY_DELAY) end
    end
    return false, nil
end
```

---

## Auto-Save: PlayerRemoving + BindToClose

Server shutdown without `BindToClose` silently discards unsaved data.

```lua
local sessionData = {} -- [userId] = data table

Players.PlayerAdded:Connect(function(player)
    local data = loadData(player)
    if data then
        sessionData[player.UserId] = data
    else
        player:Kick("Could not load your data. Please rejoin.")
    end
end)

Players.PlayerRemoving:Connect(function(player)
    local data = sessionData[player.UserId]
    if data then
        saveData(player, data)
        sessionData[player.UserId] = nil
    end
end)

-- Flush all sessions on server shutdown
game:BindToClose(function()
    for userId, data in pairs(sessionData) do
        local key = "player_" .. userId
        pcall(function()
            playerStore:SetAsync(key, data)
        end)
    end
end)
```

---

## Ordered DataStores (Leaderboards)

Values must be positive integers.

```lua
local coinsLeaderboard = DataStoreService:GetOrderedDataStore("Coins_v1")

local function setLeaderboardScore(userId, coins)
    pcall(function()
        coinsLeaderboard:SetAsync("player_" .. userId, math.floor(coins))
    end)
end

local function getTopPlayers(count)
    local success, pages = pcall(function()
        return coinsLeaderboard:GetSortedAsync(false, count) -- false = descending
    end)
    if not success then return {} end

    local results = {}
    for rank, entry in ipairs(pages:GetCurrentPage()) do
        table.insert(results, { rank = rank, userId = entry.key, score = entry.value })
    end
    return results
end
```

---

## Data Versioning / Migration

Include a `_version` field and migrate in the load path.

```lua
local CURRENT_VERSION = 2

local function migrateData(data)
    local version = data._version or 1
    if version < 2 then
        data.coins = data.gold or 0  -- renamed field
        data.gold = nil
        data._version = 2
    end
    return data
end
```

Use a versioned datastore name (`PlayerData_v2`) for breaking schema changes.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| No `pcall` around datastore calls | Unhandled error crashes the script | Always wrap in `pcall` |
| Saving on every `Changed` event | Hits rate limits (60 + numPlayers×10 writes/min) | Throttle; save on remove + periodic interval |
| No `BindToClose` handler | Data lost on server shutdown | Always flush all sessions in `BindToClose` |
| Giving default data on load failure | Player silently loses progress | Return `nil` on failure; kick or retry |
| `SetAsync` for atomic counters | Race condition across servers | Use `UpdateAsync` for read-modify-write |
| Storing Instances or functions | Data silently drops | Store only strings, numbers, booleans, plain tables |
| Reusing datastore name after schema change | Old shape clashes with new code | Append `_v2`, `_v3` to name on breaking changes |
