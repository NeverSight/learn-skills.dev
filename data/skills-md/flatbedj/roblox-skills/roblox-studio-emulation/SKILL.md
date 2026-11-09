---
name: roblox-studio-emulation
description: Use when you need to test a Roblox game under conditions a solo Studio playtest can't reach — mobile/tablet/phone (device emulation, TouchEnabled), multiplayer features (parties, co-op, trading, anything needing a 2nd player), or any client state that normally requires another person. Covers driving Studio's Test menu via AppleScript and simulating multiplayer by firing real remotes from the Server VM. Load this INSTEAD of telling the user "I can't test that myself".
---

# Emulating conditions a solo playtest can't reach

Two whole classes of testing look impossible from the MCP tools alone, so it's tempting to punt them
to the user. Both are self-serviceable. **Check here before claiming you need the user to test
something.**

For the normal dev loop see `roblox-studio-workflow`; for the MCP toolbox see `roblox-studio-mcp`.

---

## 1. Device emulation (mobile / tablet / touch) — via Studio's menu bar

Studio exposes **no windows** to macOS Accessibility (`count windows` → 0), so you can't resize it.
But it exposes its **entire menu bar**, which is enough to drive the Test menu.

```bash
# one-time: the user must grant Terminal (or your host app) Accessibility permission
#   System Settings → Privacy & Security → Accessibility
# symptom if missing: "osascript is not allowed assistive access. (-1719)"

osascript -e 'tell application "Roblox Studio" to activate'
osascript -e 'tell application "System Events" to tell process "RobloxStudio" \
  to click menu item "Device Emulator" of menu 1 of menu bar item "Test" of menu bar 1'
```

Process name is **`RobloxStudio`** (not "Roblox Studio", not "RobloxStudioBeta").

**Verify it took**, don't assume — start Play and read the real values:

```lua
local cam = workspace.CurrentCamera
local UIS = game:GetService("UserInputService")
-- desktop: ~1920x1080, TouchEnabled=false
-- emulated: device-sized viewport, TouchEnabled=TRUE
return cam.ViewportSize, UIS.TouchEnabled
```

`TouchEnabled = true` is the signal that touch-only code paths (thumbstick clearance, touch layout
branches, `POS_SHOWN` offsets) are now live.

The full Test menu (useful items):

| Item | Notes |
|---|---|
| `Device Emulator` | toggles emulation |
| `Controller Emulator` / `Player Emulator` | gamepad / player-state emulation |
| `Start Test Session` | required before `Add Clients` |
| `Add Clients` | **disabled in Play Solo**; enabled inside a Test Session |
| `Toggle Client View`, `Pause Client`, `End Session` | multi-client session control |

Enumerate + check enabled state before clicking:

```bash
osascript -e 'tell application "System Events" to tell process "RobloxStudio" \
  to get name of every menu item of menu 1 of menu bar item "Test" of menu bar 1'
osascript -e 'tell application "System Events" to tell process "RobloxStudio" \
  to get enabled of menu item "Add Clients" of menu 1 of menu bar item "Test" of menu bar 1'
```

### Limits
- **Picking a specific device** (iPhone vs iPad vs …) uses an in-window dropdown that is NOT
  AX-exposed. You get whatever device is currently selected. Ask the user to set it once if you need
  a particular width — narrow phones are where layout actually breaks.
- Toggling the emulator **ends the current Play session** and can drop the MCP link. Re-point with
  `list_roblox_studios` → `set_active_studio`, then `start_stop_play`.
- Toggle it back OFF when done, or every later screenshot is a touch device.

---

## 2. Multiplayer features WITHOUT a second client — fire the real remotes

**This is usually faster and more precise than launching a multi-client session.** The Server and
Client VMs share the DataModel, so a `FireClient` from the Server VM reaches the *real* client
modules and drives everything downstream — signal handlers, cached state, UI refreshes.

```lua
-- datamodel_type = "Server"
local Remotes = require(game:GetService("ReplicatedStorage"):WaitForChild("Shared").Remotes)
local plr = game.Players:GetPlayers()[1]

-- pretend the server told us we joined someone's party
Remotes.event("PartyUpdated"):FireClient(plr, {
    ownerUserId = 99999999, ownerName = "TestHost",
    members = { { userId = plr.UserId, name = plr.DisplayName } },
})
```

Then assert on **observable instance state** from the Client VM (never module internals — separate
VM, `require` gives a phantom copy):

```lua
-- datamodel_type = "Client"
local on = 0
for _, p in game:GetService("CollectionService"):GetTagged("Plot") do
    for _, d in p:GetDescendants() do
        if d:IsA("ProximityPrompt") and d.Name == "PartyPrompt" and d.Enabled then on += 1 end
    end
end
return on
```

**Always test the round trip** — fire the "joined" state, assert, then fire the "left" state
(`FireClient(plr, nil)`) and assert it reverts. A one-way test hides stuck state, which is the
scarier bug (a prompt stuck hidden = the feature is dead for that player).

### Faking the preconditions
Client-side attribute writes are enough to set up a scenario, because client code reads the same
attributes and `GetAttributeChangedSignal` fires locally:

```lua
-- datamodel_type = "Client" — pretend another player owns this plot
workspace.Map.Plots.Plot1:SetAttribute("OwnerUserId", 99999999)
-- ... run the test ...
workspace.Map.Plots.Plot1:SetAttribute("OwnerUserId", nil)  -- ALWAYS clean up
```

### When this does NOT work
Code that requires the faked user to be a **real online `Player`** can't be faked this way. Example:
a poll loop that does `Players:GetPlayerByUserId(owner)` and tears down anything failing that check
will immediately undo your setup. Symptom: the thing you created vanishes within a second.

Fall back to either:
- **`Test ▸ Start Test Session ▸ Add Clients`** for a genuine second player, or
- **unit-test the pure logic** with synthetic inputs in the Client VM — mirror the shipped
  guard/branch verbatim and table-test it:

```lua
local cases = {
    { "nil payload",     nil,                 true  },
    { "empty string",    "",                  true  },
    { "garbage base64",  "!!!not-base64!!!",  true  },
    { "short buffer",    Base64.encode(short),true  },
    { "valid buffer",    Base64.encode(full), false },
}
-- assert blocked == expected for each; report N/N
```

That's a real, reportable result — just be explicit that it verifies the *logic*, not the full
render path.

---

## Reporting honestly
Distinguish these three, every time:
- **Verified live** — drove it and observed the effect.
- **Logic-verified** — table-tested the branch with synthetic inputs; full path untested.
- **Untested** — say so, and say exactly what it needs.

Never let "it compiles and looks right" be reported as verified.

Current MCP device tools (`set_device_simulator`, `capture_device_matrix`) and the phone checklist: **roblox-studio-verification** and **roblox-cross-device-ui**. Try those before the AppleScript menu route.
