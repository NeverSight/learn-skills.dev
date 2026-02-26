---
name: roblox-gui
description: "Use when building, animating, or debugging Roblox GUI elements including HUDs, menus, world-space UI, and player labels. Triggers on: ScreenGui setup, SurfaceGui or BillboardGui placement, UDim2 sizing questions, TweenService UI animations, responsive scaling, LocalScript GUI logic, ResetOnSpawn issues, or any Frame/TextLabel/ImageButton layout work."
---

# Roblox GUI Reference

## GUI Container Types

| Container | Parent | Use Case |
|---|---|---|
| `ScreenGui` | `PlayerGui` | HUDs, menus, overlays — always faces screen |
| `SurfaceGui` | `BasePart` | World-space UI on a part surface (signs, screens) |
| `BillboardGui` | `BasePart` or `Model` | Floats above a part in 3D space (name tags, health bars) |

### ScreenGui

```lua
-- LocalScript in StarterGui or StarterPlayerScripts
local player = game:GetService("Players").LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "HUD"
screenGui.ResetOnSpawn = false   -- keep GUI across respawns
screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
screenGui.Parent = playerGui
```

### SurfaceGui

```lua
local surfaceGui = Instance.new("SurfaceGui")
surfaceGui.Face = Enum.NormalId.Front
surfaceGui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
surfaceGui.PixelsPerStud = 50
surfaceGui.Parent = workspace.ScreenPart

local label = Instance.new("TextLabel")
label.Size = UDim2.fromScale(1, 1)
label.Text = "Hello World"
label.Parent = surfaceGui
```

### BillboardGui

```lua
local billboard = Instance.new("BillboardGui")
billboard.Size = UDim2.fromOffset(200, 50)
billboard.StudsOffset = Vector3.new(0, 2.5, 0)  -- float above head
billboard.AlwaysOnTop = false
billboard.Parent = character:WaitForChild("Head")

local nameLabel = Instance.new("TextLabel")
nameLabel.Size = UDim2.fromScale(1, 1)
nameLabel.BackgroundTransparency = 1
nameLabel.Text = player.DisplayName
nameLabel.Parent = billboard
```

---

## UDim2 Sizing and Positioning

`UDim2.new(xScale, xOffset, yScale, yOffset)` — scale is 0–1 relative to parent, offset is pixels.

```lua
frame.Size     = UDim2.new(1, 0, 0, 50)       -- full width, 50px tall
frame.Position = UDim2.new(0, 0, 0, 0)         -- top-left corner

frame.Size     = UDim2.fromScale(0.6, 0.4)     -- 60% wide, 40% tall
frame.Position = UDim2.new(0.2, 0, 0.3, 0)    -- centered (0.2 = (1-0.6)/2)

UDim2.fromScale(0.5, 0.5)    -- scale only
UDim2.fromOffset(300, 150)   -- pixels only
```

**AnchorPoint** shifts the element's pivot (0–1 on each axis):

```lua
frame.AnchorPoint = Vector2.new(0.5, 0.5)   -- pivot at center
frame.Position    = UDim2.fromScale(0.5, 0.5)  -- truly centered on screen
```

---

## Responsive Design

Prefer scale over offset so UI adapts to all screen sizes.

```lua
button.Size     = UDim2.fromScale(0.2, 0.07)
button.Position = UDim2.new(0.4, 0, 0.85, 0)

-- Prevent distortion with UIAspectRatioConstraint
local arc = Instance.new("UIAspectRatioConstraint")
arc.AspectRatio = 4   -- width:height = 4:1
arc.Parent = button
```

---

## TweenService Animations

```lua
local TweenService = game:GetService("TweenService")
local tweenInfo = TweenInfo.new(0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)

local menuFrame = script.Parent

local function openMenu()
    TweenService:Create(menuFrame, tweenInfo, {
        Position = UDim2.new(0.05, 0, 0.1, 0)
    }):Play()
end

local function closeMenu()
    TweenService:Create(menuFrame, tweenInfo, {
        Position = UDim2.new(-0.5, 0, 0.1, 0)
    }):Play()
end

-- Animated progress bar
local function setProgress(bar, pct)
    TweenService:Create(bar, TweenInfo.new(0.2), {
        Size = UDim2.new(pct, 0, 1, 0)
    }):Play()
end
```

---

## LocalScript Placement

| Location | Notes |
|---|---|
| `StarterGui` | Cloned into `PlayerGui` on join; use `ResetOnSpawn = false` to persist |
| `StarterPlayerScripts` | Runs once, not reset on respawn; good for persistent managers |
| `StarterCharacterScripts` | Re-runs each spawn; suited for character-dependent UI |

```lua
-- Safe pattern: wait for character
local player = game:GetService("Players").LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")

humanoid.HealthChanged:Connect(function(health)
    -- update health bar
end)
```

---

## ResetOnSpawn

```lua
screenGui.ResetOnSpawn = false  -- persist across respawns (inventory, settings)
screenGui.ResetOnSpawn = true   -- re-create on respawn (respawn timer) — default
```

---

## Common Patterns Quick Reference

| Pattern | Key Setup |
|---|---|
| Full-screen overlay | `Size = UDim2.fromScale(1,1)`, `Position = UDim2.fromScale(0,0)` |
| Bottom-center HUD bar | `AnchorPoint = (0.5,1)`, `Position = UDim2.new(0.5,0,1,-10)` |
| Padded list | `UIPadding` + `UIListLayout` inside a Frame |
| Scrollable list | `ScrollingFrame` + `UIListLayout`; set `CanvasSize` from `UIListLayout.AbsoluteContentSize` |
| Rounded corners | `UICorner` with `CornerRadius = UDim.new(0, 8)` |
| Scaled text | `TextScaled = true` on TextLabel/TextButton so font grows with container |
| Dynamic frame height | `AutomaticSize = Enum.AutomaticSize.Y` so frame expands to fit children |
| Health bar | Nested frames: outer = background, inner tweened by `Size.X.Scale` |
| Name tag | `BillboardGui` on Head, `StudsOffset = Vector3.new(0, 2.5, 0)` |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| GUI disappears on respawn | Set `ResetOnSpawn = false` or use `StarterPlayerScripts` |
| UI looks wrong on mobile | Use `UDim2.fromScale` + `UIAspectRatioConstraint` |
| Script can't find `PlayerGui` | Use `player:WaitForChild("PlayerGui")` |
| Tween doesn't run | Ensure the property is tweenable; `Text` is not, `Position` and `Size` are |
| BillboardGui visible through walls | Verify `AlwaysOnTop = false` |
| `AbsoluteSize` is zero on first frame | Read it inside `task.defer` or after first render step |
| Clicks pass through overlapping frames | Add a transparent input-blocking Frame or set `Modal = true` |
| SurfaceGui flickers | Set `LightInfluence = 0`; ensure part isn't too thin |
| Text tiny on mobile | Set `TextScaled = true` — fixed `TextSize` doesn't adapt to screen size |
| UI hard to test on mobile | Use Studio's **Device Emulator** (Test tab → Device) to preview layouts |
