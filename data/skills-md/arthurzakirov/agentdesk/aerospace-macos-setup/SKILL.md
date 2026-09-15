---
name: aerospace-macos-setup
description: Install, configure, and debug AeroSpace on macOS. Use when Codex needs to set up AeroSpace with Homebrew, create or repair ~/.aerospace.toml, configure window movement hotkeys for multi-monitor workflows, diagnose Accessibility or server/config problems, or automate binding tests with the AeroSpace CLI.
---

# AeroSpace macOS Setup

## Core Workflow

Use this skill for hands-on AeroSpace setup and debugging on macOS. Prefer direct verification with the installed `aerospace` CLI over guessing from docs or memory.

1. Verify installation and runtime:

```bash
command -v brew
brew list --cask nikitabobko/tap/aerospace
aerospace --version
```

If `aerospace --version` says `AeroSpace.app server version: Unknown`, the app server is unreachable from the current command context. Try running the same command outside the sandbox with escalation before concluding AeroSpace is stopped.

2. Launch AeroSpace:

```bash
open -a AeroSpace
open -b bobko.aerospace
```

Use the bundle id form when app-name launch looks suspicious.

3. Check Accessibility if the app starts and immediately exits:

```bash
open 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
```

The user must enable `/Applications/AeroSpace.app` manually. Logs commonly show `TCCAccessRequest for kTCCServiceAccessibility` around this failure mode.

4. Confirm the active config path:

```bash
aerospace config --config-path
```

Do not assume `~/.aerospace.toml` is active. AeroSpace may still be running with `/Applications/AeroSpace.app/Contents/Resources/default-config.toml` until `aerospace reload-config` succeeds.

5. Confirm active bindings:

```bash
aerospace config --get mode.main.binding --json
```

If expected bindings are missing, reload:

```bash
aerospace reload-config
```

## User Config

If no user config exists, create one from the bundled default:

```bash
cp /Applications/AeroSpace.app/Contents/Resources/default-config.toml ~/.aerospace.toml
```

Edit `~/.aerospace.toml`, usually under `[mode.main.binding]`. Use `apply_patch` for manual edits.

For moving a full app/workspace between monitors, prefer workspace movement rather than window movement:

```toml
ctrl-alt-shift-up = 'move-workspace-to-monitor --wrap-around up'
ctrl-alt-shift-down = 'move-workspace-to-monitor --wrap-around down'
```

For horizontally arranged monitors:

```toml
ctrl-alt-shift-left = 'move-workspace-to-monitor --wrap-around left'
ctrl-alt-shift-right = 'move-workspace-to-monitor --wrap-around right'
```

Use `move-node-to-monitor` only when the user explicitly wants a single window to join the target monitor's currently visible workspace. If the target workspace already has another window, this will tile the moved window at half/third/etc. size. For users expecting "throw this app to the other screen and keep it full size", `move-workspace-to-monitor` matches the mental model better.

Avoid `alt-shift-left/right/up/down` for global bindings. macOS and text apps often use `Option + Shift + Arrow` for text selection or special-character input, so users may see text selected in Google Docs or odd characters typed in terminals.
Avoid plain `ctrl-alt-up/down` if terminal tab switching behaves strangely; some terminal/app shortcut paths can collide with less explicit global bindings.

## Automated Testing

Prefer AeroSpace's own test path first:

```bash
aerospace trigger-binding --mode main ctrl-alt-shift-down
aerospace trigger-binding --mode main ctrl-alt-shift-up
```

Then verify state before and after:

```bash
aerospace list-monitors
aerospace list-monitors --focused
aerospace list-windows --focused --format '%{window-id} | %{app-name} | %{window-title} | %{monitor-id}'
```

This tests the configured binding without relying on macOS delivering a physical keypress. Use real keystroke synthesis only when specifically debugging OS-level hotkey interception after `trigger-binding` passes.

For direct command testing without a binding:

```bash
aerospace move-workspace-to-monitor --wrap-around down
aerospace move-workspace-to-monitor --wrap-around up
```

## App Launcher Hotkeys

Use AeroSpace `exec-and-forget` for simple app launch/focus shortcuts. `open -a` activates an existing app instance or launches it if it is not running.

For frequently used apps, prefer low-friction one-hand bindings and repurpose unused AeroSpace workspace letters:

```toml
alt-g = 'exec-and-forget open -a Ghostty'
alt-c = 'exec-and-forget open -a "Google Chrome"'
```

For safer but less ergonomic bindings:

```toml
ctrl-alt-cmd-g = 'exec-and-forget open -a Ghostty'
ctrl-alt-cmd-c = 'exec-and-forget open -a "Google Chrome"'
```

Avoid plain `cmd-c` and `cmd-g` for launchers. `cmd-c` is Copy and `cmd-g` is commonly Find Next. `alt-c` and `alt-g` are acceptable only if the user is willing to give up AeroSpace workspace bindings for `C` and `G`.

Test launcher bindings without pressing physical keys:

```bash
aerospace trigger-binding --mode main ctrl-alt-cmd-g
aerospace trigger-binding --mode main ctrl-alt-cmd-c
aerospace trigger-binding --mode main alt-g
aerospace trigger-binding --mode main alt-c
```

## Ghostty Native Tabs

Do not spend repeated cycles trying to make Ghostty native macOS tabs behave like one real AeroSpace window. Ghostty native tabs are exposed to macOS window-manager APIs as separate windows, so AeroSpace cannot reliably distinguish "new tab" from "new window".

For the detailed failure history, partial workarounds, and known bad fixes, read `references/ghostty-native-tabs-aerospace.md`.

Stable recommendation: avoid Ghostty native tabs under AeroSpace. Use separate AeroSpace workspaces/windows, Ghostty splits, or a terminal multiplexer such as `tmux` inside one Ghostty OS window. For the tmux migration path, read `references/tmux-in-ghostty.md`.

## Debugging Checklist

- Run `aerospace --version` outside the sandbox if sandboxed CLI calls cannot connect.
- Use `ps -ax` outside the sandbox to confirm `AeroSpace` is running.
- Read recent logs when startup or Accessibility behavior is unclear:

```bash
/usr/bin/log show --last 10m --predicate 'process == "AeroSpace" OR eventMessage CONTAINS "AeroSpace"'
```

- Check `aerospace config --config-path` after every config creation or reload.
- Check `aerospace config --get mode.main.binding --json` to prove the active server sees the binding.
- Use `trigger-binding --mode main <binding>` and compare focused window `monitor-id` before and after.
- If the user says a shortcut types characters or selects text, choose a different binding rather than continuing to debug AeroSpace movement.
- If terminal or browser tab switching is broken, remove default tab-based AeroSpace bindings such as `alt-tab` and `alt-shift-tab`.
- If focus or tab changes feel like they drag the pointer across monitors, set `on-focused-monitor-changed = []`.
- If clicking a terminal tab appears to jump monitors, inspect all terminal windows with `aerospace list-windows --all`; the app may already have separate windows/tabs spread across monitors.

## Helper Script

Use `scripts/aerospace_diagnose.sh` for a compact diagnostic snapshot. Run it outside the sandbox when socket access or process listing is blocked:

```bash
/Users/zakirov/.codex/skills/aerospace-macos-setup/scripts/aerospace_diagnose.sh
```
