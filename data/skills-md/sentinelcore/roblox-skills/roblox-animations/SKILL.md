---
name: roblox-animations
description: Use when working with Roblox animation systems including playing, stopping, or blending animations on Humanoid characters or non-Humanoid models, handling AnimationTrack events, replacing default character animations, or debugging animation priority and blending issues.
---

# Roblox Animations Reference

## Core Objects

| Object | Purpose |
|---|---|
| `Animation` | Asset reference — holds `AnimationId` |
| `Animator` | Lives inside Humanoid or AnimationController; loads and drives tracks |
| `AnimationController` | Replaces Humanoid for non-character rigs |
| `AnimationTrack` | Returned by `LoadAnimation`; controls playback |

---

## Where to Run Animation Code

| Scenario | Script Type | Location |
|---|---|---|
| Local player character | `LocalScript` | `StarterCharacterScripts` |
| NPC / server-owned model | `Script` | Inside model or `ServerScriptService` |

> Never play player character animations from a `Script` — they will not replicate correctly to the local client.

---

## Loading and Playing Animations

```lua
-- LocalScript in StarterCharacterScripts
local character = script.Parent
local animator = character:WaitForChild("Humanoid"):WaitForChild("Animator")

local animation = Instance.new("Animation")
animation.AnimationId = "rbxassetid://1234567890"

local track = animator:LoadAnimation(animation)

track:Play()                      -- default fade-in (0.1s), weight 1, speed 1
track:Play(0.1, 1, 0.5)          -- fadeTime, weight, speed

track:AdjustSpeed(1.5)           -- change speed while playing
track:AdjustWeight(0.5, 0.2)     -- weight 0.5, fade over 0.2s

track:Stop()                      -- default fade-out (0.1s)
track:Stop(0.5)                   -- fade out over 0.5s
```

---

## AnimationTrack Events

```lua
-- Fires after fade-out completes
track.Stopped:Connect(function()
    print("Animation finished")
end)

-- Use :Once for one-shot cleanup
track.Stopped:Once(function()
    cleanup()
end)

-- Fires when a named keyframe marker is reached
-- Marker names are set in the Roblox Animation Editor
track:GetMarkerReachedSignal("FootStep"):Connect(function(paramString)
    playFootstepSound()
end)
```

---

## Looped vs One-Shot

| Property | Looped | One-Shot |
|---|---|---|
| `track.Looped` | `true` | `false` |
| Set in | Animation Editor (loop toggle) | Animation Editor |
| Override at runtime | `track.Looped = false` | `track.Looped = true` |
| Stops automatically | No — must call `track:Stop()` | Yes — after one cycle |

```lua
-- Force a looped animation to play once
track.Looped = false
track:Play()
track.Stopped:Once(function() print("Done") end)
```

---

## Animation Priority and Blending

Priority controls which tracks win on contested joints. Higher priority overrides lower.

```
Idle < Movement < Action < Action2 < Action3 < Action4 < Core
```

```lua
idleTrack.Priority   = Enum.AnimationPriority.Idle
runTrack.Priority    = Enum.AnimationPriority.Movement
attackTrack.Priority = Enum.AnimationPriority.Action

idleTrack:Play()
runTrack:Play()     -- overrides idle on shared joints
attackTrack:Play()  -- blends on top for joints it owns
```

Weight adjusts influence when two tracks share the same priority:

```lua
trackA:Play(0, 0.6)  -- weight 0.6
trackB:Play(0, 0.4)  -- weight 0.4 — blended on shared joints
```

---

## Humanoid vs AnimationController

### Humanoid (characters and humanoid NPCs)

```lua
local animator = character:FindFirstChildOfClass("Humanoid"):FindFirstChildOfClass("Animator")
local track = animator:LoadAnimation(animation)
track:Play()
```

### AnimationController (props, vehicles, creatures)

```lua
local controller = model:FindFirstChildOfClass("AnimationController")
local animator = controller:FindFirstChildOfClass("Animator")
if not animator then
    animator = Instance.new("Animator")
    animator.Parent = controller
end
local track = animator:LoadAnimation(animation)
track:Play()
```

---

## Replacing Default Character Animations

The `Animate` LocalScript in the character holds animation references. Modify its `AnimationId` values on CharacterAdded.

```lua
-- LocalScript in StarterCharacterScripts
local animate = script.Parent:WaitForChild("Animate")

local function replaceAnim(slotName, newId)
    local slot = animate:FindFirstChild(slotName)
    if slot then
        local animObj = slot:FindFirstChildOfClass("Animation")
        if animObj then animObj.AnimationId = newId end
    end
end

replaceAnim("idle",  "rbxassetid://111111111")
replaceAnim("run",   "rbxassetid://222222222")
replaceAnim("jump",  "rbxassetid://333333333")
replaceAnim("fall",  "rbxassetid://444444444")
replaceAnim("climb", "rbxassetid://555555555")
```

Available slots: `idle`, `walk`, `run`, `jump`, `fall`, `climb`, `swim`, `swimidle`, `toolnone`, `toolslash`, `toollunge`.

---

## Stop All Playing Animations

```lua
local function stopAll(animator, fadeTime)
    for _, track in animator:GetPlayingAnimationTracks() do
        track:Stop(fadeTime or 0.1)
    end
end
```

---

## Quick Playback Reference

```lua
track:Play(fadeTime, weight, speed)
-- fadeTime  default 0.1   — blend-in seconds
-- weight    default 1.0   — joint influence (0–1)
-- speed     default 1.0   — playback rate

track.TimePosition   -- current position in seconds (read/write)
track.Length         -- total duration in seconds
track.IsPlaying      -- bool
track.Looped         -- bool (override allowed at runtime)
track.Priority       -- Enum.AnimationPriority
track.WeightCurrent  -- actual blended weight right now
track.WeightTarget   -- target weight after fade
```

---

## Upper-Body Only Animations

Priority blending affects **all joints** an animation touches. To play a wave only on the arms while legs animate from run/idle, the animation itself must be authored to only key upper-body bones (leave lower-body joints unkeyed in the Animation Editor). There is no runtime API to mask joints — the solution is in the animation asset, not the script.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Playing character animations in a `Script` | Use `LocalScript` in `StarterCharacterScripts` |
| `LoadAnimation` called on `Humanoid` (deprecated) | Call on `Animator` instead |
| Two animations fighting on same joints | Assign different `Priority` values |
| `Stopped` fires immediately | Animation has zero length or wrong `Looped` setting |
| `GetMarkerReachedSignal` never fires | Marker name misspelled, or animation not re-uploaded after adding markers |
| NPC animation not visible to other clients | Play from a `Script` (server), not `LocalScript` |
| `AnimationController` track won't play | Missing `Animator` child inside `AnimationController` |
