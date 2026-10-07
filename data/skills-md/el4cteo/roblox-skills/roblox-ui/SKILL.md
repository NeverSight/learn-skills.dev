---
name: roblox-ui
description: Responsive cross-platform UI - ScreenGui and safe areas (ScreenInsets), Scale vs Offset, UIListLayout flex/UIFlexItem, constraints, StyleSheets/tokens/themes, RichText, gamepad/touch navigation, UIDragDetector, CanvasGroup, tweens, BillboardGui/SurfaceGui, React-lua/Fusion/Vide. Use when building HUDs, menus, shops, inventories, or fixing UI that breaks on mobile, console, or other screen sizes.
---

# Roblox UI

## Foundations

- Put UI in `StarterGui` as `ScreenGui`s (copied to each player's `PlayerGui`), or create it from a
  client controller. UI code is client-only; the server never touches `PlayerGui` in normal designs.
- `ScreenGui` defaults to set: `ResetOnSpawn = false` (keep UI across deaths), `ZIndexBehavior = Sibling`,
  `IgnoreGuiInset` per design, `ScreenInsets = CoreUISafeInsets` for interactive UI (clears notches and
  the Roblox top bar); `DeviceSafeInsets`/`None` only for full-bleed backgrounds.
- **Size and position with Scale** (`UDim2.fromScale`) plus constraints; use Offset only for fixed
  details (padding, strokes, icons). Pure-Offset UI breaks on phones and 4K screens.
- `AnchorPoint = Vector2.new(0.5, 0.5)` + `Position = UDim2.fromScale(0.5, 0.5)` centers an element.
- `UIAspectRatioConstraint` keeps shapes square/consistent; `UISizeConstraint` caps sizes;
  `UITextSizeConstraint` with `TextScaled` bounds text size (prefer fixed `TextSize` + `AutomaticSize`
  where possible — `TextScaled` produces inconsistent sizes).
- `AutomaticSize` lets frames grow with content (lists, tooltips, chat bubbles).
- Test every screen in the **Device Emulator** (phone portrait/landscape, tablet, console 10-foot, 4K).

## Layout

| Need | Use |
| --- | --- |
| Rows/columns that adapt | `UIListLayout` (`FillDirection`, `Padding`, `HorizontalFlex`/`VerticalFlex`, `Wraps`) |
| One item grows to fill space | `UIFlexItem` child with `FlexMode = Fill` (or `Grow`/`Shrink`/`Custom`) |
| Grids (inventory) | `UIGridLayout` inside a `ScrollingFrame` with `AutomaticCanvasSize` |
| Carousels/pages | `UIPageLayout` |
| Rounded corners, borders, padding | `UICorner`, `UIStroke`, `UIPadding` |
| Gradients, shadows | `UIGradient`, `UIShadow` |
| Scale a whole group | `UIScale` |

```luau
--!strict
local Players = game:GetService("Players")

local playerGui = Players.LocalPlayer:WaitForChild("PlayerGui")

local screenGui = Instance.new("ScreenGui")
screenGui.Name = "Hud"
screenGui.ResetOnSpawn = false
screenGui.ScreenInsets = Enum.ScreenInsets.CoreUISafeInsets

local bar = Instance.new("Frame")
bar.Name = "Toolbar"
bar.AnchorPoint = Vector2.new(0.5, 1)
bar.Position = UDim2.new(0.5, 0, 1, -16)
bar.Size = UDim2.fromScale(0.6, 0.1)
bar.BackgroundTransparency = 0.3
bar.Parent = screenGui

local list = Instance.new("UIListLayout")
list.FillDirection = Enum.FillDirection.Horizontal
list.HorizontalFlex = Enum.UIFlexAlignment.Fill -- slots share the width equally
list.Padding = UDim.new(0, 8)
list.Parent = bar

Instance.new("UICorner").Parent = bar
local padding = Instance.new("UIPadding")
padding.PaddingLeft, padding.PaddingRight = UDim.new(0, 8), UDim.new(0, 8)
padding.Parent = bar

for slot = 1, 5 do
	local button = Instance.new("TextButton")
	button.Name = `Slot{slot}`
	button.Text = tostring(slot)
	button.Size = UDim2.fromScale(0, 1)
	button.Parent = bar
	Instance.new("UIAspectRatioConstraint").Parent = button
end

screenGui.Parent = playerGui -- parent last: one layout pass, no flicker
```

## Styling: StyleSheets (CSS-like)

Roblox's engine-level styling replaces copy-pasted property values:
- `StyleSheet` with `StyleRule`s (`Selector` like `"TextButton"`, `".Primary"` (tag), `"#Close"` (name),
  `"TextButton:Hover"` (state), `"::UICorner"` (modifier pseudo-instance)) and `rule:SetProperties({...})`.
- **Tokens** are attributes on a token sheet (`$Primary`, `$Radius`); **themes** are sheets deriving tokens
  (`StyleDerive`); swap themes by retargeting the `StyleDerive`.
- A `StyleLink` under a `ScreenGui` applies one sheet to that tree. **Style queries** (`@Name`) switch
  styles by screen size, input type, or accessibility settings.
- Edit visually in Studio's **Style Editor**. Details and a code example: [references/styling-and-frameworks.md](references/styling-and-frameworks.md).

## Cross-platform input in UI

- Read `UserInputService.PreferredInput` (`KeyboardAndMouse`, `Touch`, `Gamepad`) and listen to
  `UserInputService:GetPropertyChangedSignal("PreferredInput")` to swap button prompts and layouts.
  Don't infer platform from `TouchEnabled`/`KeyboardEnabled` alone.
- Use `GuiButton.Activated` (works for mouse, touch, and gamepad) instead of `MouseButton1Click`.
- Gamepad/console: every interactive element `Selectable`, set `GuiService.SelectedObject` when a menu
  opens, group with `SelectionGroup`/`NextSelection*` for predictable D-pad navigation, support `ButtonB`
  to close. Minimum touch target ≈ 44×44 px; readable text ≥ 14 px on phones.
- Bind actions through the **Input Action System** (`InputBinding.UIButton` makes an on-screen button
  trigger an action) — see `roblox-input`.

## Text

- `RichText = true` enables `<b>`, `<i>`, `<font color="#FF0">`, `<stroke>`, etc. Escape user text.
- **Any text from one player shown to another must be filtered** with `TextService:FilterStringAsync`
  on the server (`roblox-text-chat`). That includes pet names, signs, guild names, trade notes.
- Use `FontFace = Font.new("rbxasset://fonts/families/GothamSSm.json", Enum.FontWeight.Bold)` for weights.
- Localize with `LocalizationTable`s and auto-translation; avoid baking text into images.

## Animation and feel

- Tween on the client: `TweenService:Create(frame, TweenInfo.new(0.2, Enum.EasingStyle.Quad), { Position = ... }):Play()`.
- Animate `UIScale.Scale` for pop effects rather than `Size` (keeps layout stable).
- `CanvasGroup` fades a whole subtree (`GroupTransparency`) but renders to a texture: use it for
  fading panels, not for large always-visible UI (memory/quality cost).
- Drag-and-drop: `UIDragDetector` (the deprecated `GuiObject.Draggable` no longer works for new work).

## World-space UI

- `BillboardGui` (faces camera: names, health bars) — set `MaxDistance`, `AlwaysOnTop` sparingly,
  use `Size` in Scale for distance scaling; `SurfaceGui` for screens/signs on parts. Prefer
  `Adornee` + keep them in `PlayerGui` for per-player content. They stop rendering when their part streams out.
- `ProximityPrompt` gives cross-platform interaction UI for free (validate on the server!).

## Frameworks

For more than a few screens, a declarative framework keeps state and UI in sync:
- **React** (`jsdotlua/react` + `react-roblox`) — components + hooks, familiar to web devs, scales to big apps.
- **Fusion** — reactive state objects and declarative instance creation.
- **Vide** — small, fast reactive library.
Match whatever the project already uses. Keep game state in controllers; UI only renders it and
emits user intents.

## Performance

- Avoid updating text/properties every frame when values haven't changed.
- Hide closed menus with `Visible = false` (or `Enabled = false` on the ScreenGui) instead of
  destroying/recreating them repeatedly; build large lists lazily or virtualize them.
- Too many `UIGradient`/`CanvasGroup`/`UIStroke` on dynamic UI costs frame time; check the MicroProfiler.

## Related skills

`roblox-input` (actions, gamepad), `roblox-text-chat` (filtering), `roblox-monetization` (shops),
`roblox-luau`, `roblox-performance`.
