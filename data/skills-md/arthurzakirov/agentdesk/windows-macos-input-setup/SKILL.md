---
name: windows-macos-input-setup
description: Configure and verify a Windows 11 PC for macOS-like Logitech keyboard shortcuts, virtual-desktop switching, cross-monitor window movement, and natural scrolling. Use for reproducing or repairing this specific setup without stacking conflicting remappers.
---

# Windows macOS Input Setup

Set up a Logitech keyboard in Windows layout so the physical Mac legends behave consistently:

- `cmd | alt` (left of Space) acts as Command for common shortcuts.
- `option | start` acts as Option and `Option+Tab` opens Windows app switching.
- Physical Control remains Control.
- `Control+Tab` remains native `Control+Tab` for switching browser/editor tabs;
  it must not duplicate `Option+Tab`.
- `Control+Up` opens Windows Task View (`Win+Tab`) with all windows and virtual
  desktops, matching macOS Mission Control muscle memory.
- `Control+Left/Right` switches virtual desktops.
- `Control+Option+Left/Right` moves the focused window between monitors.
- Native `Option+Up` maximizes the focused window because the physical Option
  key is Windows `Left Win`. Do not use
  `Control+Option+Enter`; Windows reserves its physical `Win+Control+Enter`
  chord for Narrator and may consume it despite the Narrator toggle being off.
- `Option+Left/Right` can be mapped explicitly to Windows `Control+Left/Right`
  for word navigation without taking the physical `Control+Left/Right` desktop
  shortcuts away.
- Windows natural scrolling is enabled when requested.

Read [references/setup-and-validation.md](references/setup-and-validation.md) before changing the machine. It contains the exact profile, conflict cleanup, current PowerToys caveats, restart procedure, and automatic verification workflow.

## Invariants

- Keep only the one-way modifier remap `Left Alt -> Left Ctrl`. Never add the
  reverse `Left Ctrl -> Left Alt`: it turns physical `Control+Tab` into
  `Alt+Tab` and duplicates `Option+Tab`. Use a small set of explicit,
  non-overlapping shortcut remaps. PowerToys can keep physical
  `Control+Left/Right` mapped to desktop switching while separately mapping
  physical `Option+Left/Right` to text navigation.
- Keep `162;38 -> 91;9` for `Control+Up` Task View. Do not remove
  `91;9 -> 164;9`; that separate rule preserves physical `Option+Tab` as
  Windows `Alt+Tab`.
- For virtual-desktop arrows, use physical Left Control as the source but Right
  Control in the generated Windows shortcut: `162;37 -> 91;163;37` and
  `162;39 -> 91;163;39`. Reusing Left Control in the target can fail after the
  source modifier is suppressed by Keyboard Manager.
- Do not run Kinto, `mac-keyboard-behavior-in-windows`, or a custom AutoHotkey profile concurrently with this PowerToys profile.
- Do not add another remapper to reproduce macOS `Option+Left/Right`; use direct
  PowerToys shortcut rules. `Control+Shift+Arrow`, then a plain arrow, remains a
  fallback rather than the preferred configuration.
- Back up existing PowerToys configuration before mutation and preserve unrelated settings.
- Restart the full PowerToys runner after profile changes; verify the Keyboard Manager engine is its child process.
- Test observable behavior automatically. Never infer success only from valid JSON or a running process.
- Never configure `Control+Option+L` for monitor 3 on this layout: it contains protected Windows `Win+L` and can lock the PC. Use a safe numeric alternative only when explicitly requested and independently testable.
- Never map physical `Control+Option+Enter`. Keep Narrator and its keyboard
  shortcut disabled, and leave native `Option+Up -> Win+Up` unremapped for
  maximizing. Do not invent a third shortcut scheme.
