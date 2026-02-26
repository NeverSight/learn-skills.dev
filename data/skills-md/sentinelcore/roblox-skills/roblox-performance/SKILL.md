---
name: roblox-performance
description: Use when optimizing a Roblox game for better frame rates, reducing lag, improving server or client performance, diagnosing FPS drops, handling large worlds, or when asked about streaming, draw calls, object pooling, LOD, MicroProfiler, or expensive loop operations.
---

# Roblox Performance Optimization

## Quick Reference

| Technique | Impact | When to Use |
|---|---|---|
| StreamingEnabled | High | Large open worlds |
| Object pooling | High | Frequent spawn/destroy |
| Cache references outside loops | High | Heartbeat/RenderStepped |
| `task.wait()` over `wait()` | Medium | All scripts |
| MeshParts over Unions | Medium | Many unique shapes |
| LOD (hide at distance) | Medium | Complex models |
| Anchor static parts | Medium | Reduce physics budget |
| Limit PointLights | High | Any scene with many lights |

---

## StreamingEnabled

Enable for large worlds — engine sends only nearby parts to the client.

```lua
-- Studio: Workspace > StreamingEnabled = true
workspace.StreamingEnabled = true
workspace.StreamingMinRadius = 64
workspace.StreamingTargetRadius = 128
```

- Parts outside the radius are `nil` on the client — always guard with `if part then`.
- Set `Model.LevelOfDetail = Disabled` on models that must always be present.
- Pre-stream an area before a cutscene or teleport:

```lua
workspace:RequestStreamAroundAsync(targetPosition, 5) -- 5s timeout
```

---

## Hot-Path Loop Optimization

`RunService.Heartbeat` and `RenderStepped` fire every frame (~60×/sec). Keep them lean.

### Bad — searching the hierarchy every frame

```lua
RunService.Heartbeat:Connect(function()
    local char = workspace:FindFirstChild(player.Name)
    local humanoid = char and char:FindFirstChild("Humanoid")
    if humanoid then humanoid.WalkSpeed = 16 end
end)
```

### Good — cache references once, do work only when needed

```lua
local humanoid = nil

Players.LocalPlayer.CharacterAdded:Connect(function(char)
    humanoid = char:WaitForChild("Humanoid")
end)

RunService.Heartbeat:Connect(function(dt)
    if not humanoid then return end
    humanoid.WalkSpeed = 16  -- cached reference, no search
end)
```

**Rules:**
- Cache `game:GetService()` and part references outside the loop.
- Never call `FindFirstChild`, `GetChildren`, or `GetDescendants` inside Heartbeat.
- Throttle work that doesn't need every frame:

```lua
local TICK_INTERVAL = 0.5
local elapsed = 0

RunService.Heartbeat:Connect(function(dt)
    elapsed += dt
    if elapsed < TICK_INTERVAL then return end
    elapsed = 0
    -- expensive work here, runs 2×/sec instead of 60×/sec
end)
```

---

## task Library vs Legacy Scheduler

Always use `task` — `wait()` and `spawn()` throttle under load and are deprecated.

| Legacy | Modern |
|---|---|
| `wait(n)` | `task.wait(n)` |
| `spawn(fn)` | `task.spawn(fn)` |
| `delay(n, fn)` | `task.delay(n, fn)` |
| `coroutine.wrap(fn)()` | `task.spawn(fn)` |

---

## Object Pooling

Reuse instances instead of creating and destroying them every frame.

```lua
-- ObjectPool ModuleScript
local ObjectPool = {}
ObjectPool.__index = ObjectPool

function ObjectPool.new(template, initialSize)
    local self = setmetatable({ _template = template, _available = {} }, ObjectPool)
    for i = 1, initialSize do
        local obj = template:Clone()
        obj.Parent = nil
        table.insert(self._available, obj)
    end
    return self
end

function ObjectPool:Get(parent)
    local obj = table.remove(self._available) or self._template:Clone()
    obj.Parent = parent
    return obj
end

function ObjectPool:Return(obj)
    obj.Parent = nil
    table.insert(self._available, obj)
end

return ObjectPool
```

```lua
-- Usage
local pool = ObjectPool.new(ReplicatedStorage.Bullet, 20)

local function fireBullet(origin)
    local bullet = pool:Get(workspace)
    bullet.CFrame = CFrame.new(origin)
    task.delay(3, function() pool:Return(bullet) end)
end
```

---

## Level of Detail (LOD)

**Built-in:** Set `Model.LevelOfDetail = Automatic` — engine merges distant parts into an imposter mesh automatically.

**Manual distance-based LOD:**

```lua
-- LocalScript
local INTERVAL = 0.2
local LOD_DISTANCE = 150
local elapsed = 0

RunService.Heartbeat:Connect(function(dt)
    elapsed += dt
    if elapsed < INTERVAL then return end
    elapsed = 0

    local dist = (workspace.CurrentCamera.CFrame.Position - model.PrimaryPart.Position).Magnitude
    local visible = dist < LOD_DISTANCE
    for _, v in model:GetDescendants() do
        if v:IsA("BasePart") then
            v.LocalTransparencyModifier = visible and 0 or 1
        end
    end
end)
```

---

## Reducing Draw Calls

- Merge parts that share a material into one MeshPart (export from Blender as `.fbx`).
- **MeshParts** batch better than CSG Unions (Unions re-triangulate at runtime).
- Reuse materials — 10 parts sharing `SmoothPlastic` costs far less than 10 unique textures.
- Use `TextureId` on a single MeshPart instead of stacking Decals on many parts.

---

## Profiling with MicroProfiler

1. Press `Ctrl+F6` in-game to open MicroProfiler.
2. Press `Ctrl+P` to pause and inspect a single frame.
3. Look for wide bars in `heartbeatSignal` (Lua), `physicsStepped` (physics), or `render` (GPU).
4. Label your own code:

```lua
RunService.Heartbeat:Connect(function()
    debug.profilebegin("MySystem")
    -- your code
    debug.profileend()
end)
```

---

## Common FPS Killers

| Cause | Fix |
|---|---|
| Thousands of individual parts | Merge into MeshParts |
| Unanchored static geometry | `Anchored = true` on anything that never moves |
| Many `PointLight` / `SpotLight` instances | Limit to ~10–20 dynamic lights per area |
| High-rate ParticleEmitters | Lower `Rate` and `Lifetime`; disable when off-screen |
| `wait()` under heavy load | Replace with `task.wait()` |
| `FindFirstChild` chains inside Heartbeat | Cache on load |
| StreamingEnabled off on large maps | Enable it |
| `Model.LevelOfDetail = Disabled` everywhere | Use `Automatic` where safe |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| `workspace:FindFirstChild` every frame | Cache reference on character/model load |
| Destroying and re-creating bullets/effects | Use an object pool |
| `wait()` in tight loops | `task.wait()` |
| All parts with unique materials | Standardize to a small set of shared materials |
| ParticleEmitters enabled off-screen | Disable `Enabled` when particle source is not visible |
| Physics on decorative parts | `Anchored = true` |
