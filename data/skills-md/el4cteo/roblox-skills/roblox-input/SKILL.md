---
name: roblox-input
description: Player input and cameras across keyboard/mouse, touch, gamepad, VR - Input Action System (InputContext, InputAction, InputBinding), UserInputService (PreferredInput, gameProcessedEvent, mouse lock), ContextActionService, reserved keys, custom cameras with BindToRenderStep. Use when adding controls, keybinds, abilities, vehicles, on-screen buttons, or custom cameras.
---

# Roblox input and camera

## Choose an approach

| Approach | Use when |
| --- | --- |
| **Input Action System** (`InputContext` → `InputAction` → `InputBinding`) | New gameplay controls. Cross-device bindings configured as instances, contexts you enable/disable, built-in on-screen button binding, prompt display. Recommended. |
| `UserInputService` events | Raw input, text-free hotkeys, mouse position/delta, touch gestures, device detection. |
| `ContextActionService:BindAction` | Legacy/simple bind-with-mobile-button; existing code. |

All input handling is **client-side**. Send *intent* to the server via remotes; the server validates.

## Input Action System

Structure (typically in `ReplicatedStorage.Inputs`, or created from a client script):

```text
Inputs (Folder)
  PlayContext (InputContext, Priority 1000)      -- gameplay controls
    Sprint (InputAction, Type = Bool)
      Keyboard (InputBinding, KeyCode = LeftShift)
      Gamepad  (InputBinding, KeyCode = ButtonL3)
      Touch    (InputBinding, UIButton = <on-screen TextButton>)
  MenuContext (InputContext, Priority 2000, Sink = true, Enabled = false)
```

- `InputAction.Type`: `Bool` (press/release), `Direction1D` (triggers, zoom), `Direction2D` (move, camera),
  `Direction3D` (flying), `ViewportPosition` (pointer position).
- Events: `Pressed`, `Released` (Bool only), `StateChanged(value)` for every type. `action:GetState()` reads the current value.
- `InputBinding` fields: `KeyCode`; composite directions `Up/Down/Left/Right/Forward/Backward`; `Scale`
  (e.g. `0.01` for `MouseDelta`/`TouchDelta`); `PressedThreshold`/`ReleasedThreshold` for analog triggers;
  `PrimaryModifier`/`SecondaryModifier` for chords (Ctrl+S); `UIButton` to drive the action from a GUI button;
  `DisplayName`/`DisplayImage` for prompts.
- `InputContext.Enabled` switches whole control schemes (gameplay ↔ menu ↔ vehicle); `Priority` + `Sink`
  lets a higher context consume keys so lower contexts don't also fire.
- Set `Workspace.PlayerScriptsUseInputActionSystem = Enabled` to have Roblox's default player/camera
  scripts use the system too (required for server authority).

```luau
--!strict
-- Client: build a Sprint action in code and react to it.
local Players = game:GetService("Players")

local player = Players.LocalPlayer

local context = Instance.new("InputContext")
context.Name = "PlayContext"
context.Priority = 1000

local sprint = Instance.new("InputAction")
sprint.Name = "Sprint"
sprint.Type = Enum.InputActionType.Bool
sprint.Parent = context

local keyboard = Instance.new("InputBinding")
keyboard.KeyCode = Enum.KeyCode.LeftShift
keyboard.Parent = sprint

local gamepad = Instance.new("InputBinding")
gamepad.KeyCode = Enum.KeyCode.ButtonL3
gamepad.Parent = sprint

context.Parent = player:WaitForChild("PlayerScripts")

local function setSprinting(on: boolean)
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if humanoid then
		humanoid.WalkSpeed = if on then 24 else 16 -- server should validate/own real speed limits
	end
end

sprint.Pressed:Connect(function()
	setSprinting(true)
end)
sprint.Released:Connect(function()
	setSprinting(false)
end)
```

Show the right key/button: an `InputActionLabel` (beta) auto-renders the binding for the current device,
or read `action.PreferredBinding` (+ its `DisplayName`/`KeyCode`) and `UserInputService:GetStringForKeyCode`
/ `GetImageForKeyCode`, updating on `GetPropertyChangedSignal("PreferredBinding")`.

## UserInputService essentials

```luau
--!strict
local UserInputService = game:GetService("UserInputService")

UserInputService.InputBegan:Connect(function(input: InputObject, gameProcessedEvent: boolean)
	if gameProcessedEvent then
		return -- typing in a TextBox, clicking UI, or a core-script action consumed it
	end
	if input.KeyCode == Enum.KeyCode.E then
		print("interact")
	elseif input.UserInputType == Enum.UserInputType.MouseButton1 then
		print("click at", input.Position)
	end
end)

local function onPreferredInputChanged()
	local preferred = UserInputService.PreferredInput -- KeyboardAndMouse | Touch | Gamepad
	print("show prompts for", preferred)
end
UserInputService:GetPropertyChangedSignal("PreferredInput"):Connect(onPreferredInputChanged)
onPreferredInputChanged()
```

- **Always honor `gameProcessedEvent`** or players trigger abilities while typing in chat.
- `PreferredInput` reflects what the player is actually using (phone + Bluetooth gamepad → `Gamepad`);
  don't branch on `TouchEnabled`/`KeyboardEnabled` alone.
- Mouse: `UserInputService.MouseBehavior = Enum.MouseBehavior.LockCenter` for FPS (set every frame while
  in first person if other scripts may reset it), `GetMouseLocation()` (includes top-bar inset),
  `MouseDeltaSensitivity`, `MouseIconEnabled`.
- Gamepad: `GetConnectedGamepads`, `GamepadConnected/Disconnected`, thumbstick `input.Position` in
  `InputChanged` (apply a dead zone ≈ 0.15). Haptics: `HapticService` / `HapticEffect`.
- Touch: `TouchTap`, `TouchLongPress`, `TouchPinch`, `TouchSwipe`; hide default controls only if you
  replace them (`GuiService.TouchControlsEnabled`).
- Reserved keys you can't override: Esc/Start (menu), F9 (console), F11, F12, PrintScreen; chat `/`,
  Tab (player list), backpack and tool-number keys unless you disable those core features.

## ContextActionService (legacy-compatible)

`ContextActionService:BindAction(name, handler, createTouchButton, ...inputs)` with handler
`(actionName, inputState, inputObject) -> Enum.ContextActionResult?`; return `Pass` to let other
bindings see the input. Use `BindActionAtPriority` for ordering and `UnbindAction` when the context
ends (e.g. tool unequipped). Prefer the Input Action System for new work.

## Custom cameras

```luau
--!strict
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local camera = workspace.CurrentCamera
local OFFSET = Vector3.new(0, 30, 20)

camera.CameraType = Enum.CameraType.Scriptable

RunService:BindToRenderStep("TopDownCamera", Enum.RenderPriority.Camera.Value + 1, function()
	local character = Players.LocalPlayer.Character
	local root = character and character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root then
		local target = root.Position
		camera.CFrame = CFrame.lookAt(target + OFFSET, target)
	end
end)

-- Restore: RunService:UnbindFromRenderStep("TopDownCamera"); camera.CameraType = Enum.CameraType.Custom
```

- Update cameras in `BindToRenderStep` (runs before render, ordered), not `Heartbeat`/`task.wait` loops.
- Smooth with `camera.CFrame:Lerp(goal, 1 - math.exp(-speed * deltaTime))` (frame-rate independent).
- First person: `player.CameraMode = Enum.CameraMode.LockFirstPerson`; zoom limits with
  `player.CameraMinZoomDistance`/`CameraMaxZoomDistance`. Shake: offset the CFrame, don't move parts.
- Screen → world: `camera:ViewportPointToRay(x, y)` / `ScreenPointToRay` + `workspace:Raycast`.

## Cross-platform checklist

- Every action has keyboard, gamepad, **and** touch bindings (touch via `UIButton` or on-screen buttons).
- Prompts/hints update when `PreferredInput` changes. Console UI is navigable with D-pad and closes with B.
- No hover-only interactions (touch has no hover). Hold-to-confirm for destructive actions.
- Test in Studio's Device Emulator and Controller Emulator.

## Related skills

`roblox-ui` (buttons, gamepad selection), `roblox-characters-animation` (movement, abilities),
`roblox-networking` (sending intents), `roblox-physics` (vehicles).
