---
name: hammerspoon-macos-setup
description: Install, configure, repair, and verify Hammerspoon on macOS for keyboard-driven multi-monitor window placement, Spaces controls, Chrome search scopes, and Claude desktop controls. Use when reproducing this setup, fixing silent Hammerspoon hotkeys, or testing window movement without relying on AeroSpace.
---

# Hammerspoon macOS setup

Use the bundled modular configuration as the source of truth. It separates display movement, window layout, Spaces, the window picker, Chrome, and Claude desktop behavior under `assets/hammerspoon/modules/`.

## Install or refresh

Run:

```bash
scripts/install-hammerspoon-config.sh
```

The installer:

- requires macOS and Homebrew;
- installs Hammerspoon when absent;
- backs up existing managed configuration before changing it;
- symlinks `~/.hammerspoon/init.lua` and `~/.hammerspoon/modules` to this skill's bundled assets while preserving unrelated entries such as `Spoons/`;
- launches Hammerspoon and enables launch at login through the config.

The symlinks make the installed AgentDesk skill the live source of truth. A repository checkout update or SkillPort refresh updates the files behind those stable paths; reload Hammerspoon with `ctrl+alt+cmd+r` to apply the new version. Re-running the installer is idempotent when the links already target this skill version.

Do not copy credentials, private machine inventories, monitor serials, or account data into this public configuration. Displays are numbered dynamically by virtual-desktop position.

## Permissions

Hammerspoon needs macOS Accessibility access. Open **System Settings → Privacy & Security → Accessibility** when access is disabled. Enabling that setting through Computer Use requires action-time confirmation.

Restart Hammerspoon after the permission changes. A checked permission row is not sufficient proof: verify `hs.accessibilityState()` and a real window action.

## Essential bindings

- `ctrl+alt+left`, `ctrl+alt+right`, `ctrl+alt+return`: left half, right half, maximize.
- `ctrl+alt+cmd+j/k/l/ö`: send and maximize on displays 1–4, ordered left-to-right and then top-to-bottom.
- `ctrl+alt+cmd+u/i/o/p`: focus displays 1–4.
- `ctrl+alt+cmd+h`: identify numbered displays.
- `ctrl+alt+cmd+/`: searchable window picker.
- `ctrl+alt+cmd+r`: reload the configuration.

The display module first uses the standard macOS **Window → Move to …** menu. This avoids a macOS Tahoe failure mode where Accessibility reports zero-sized `AXApplication` placeholders instead of usable window objects. Direct `hs.window` movement remains a fallback for applications without the standard menu.

## Verification

Check runtime state:

```bash
/opt/homebrew/bin/hs -c 'return tostring(hs.accessibilityState()) .. "|" .. tostring(hs.autoLaunch()) .. "|" .. tostring(#hs.hotkey.getHotkeys())'
```

Then send the actual shortcuts to a disposable visible window and verify the observable result after every key:

1. Confirm left half, right half, and maximize visually.
2. Confirm each connected display key by checking that the target display disappears from the app's **Move to …** menu after the move.
3. Treat an unconnected fourth display as untested; do not claim it moved successfully.
4. Confirm AltTab and any requested launcher remain running after troubleshooting.

Do not report success merely because hotkeys registered or a function returned without error.
