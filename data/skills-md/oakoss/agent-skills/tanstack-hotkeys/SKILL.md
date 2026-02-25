---
name: tanstack-hotkeys
description: 'TanStack Hotkeys for type-safe keyboard shortcuts with React hooks. Use when adding keyboard shortcuts, hotkey sequences, shortcut recording, key hold detection, or platform-aware shortcut display. Use for hotkeys, keyboard-shortcuts, shortcuts, key-binding, Mod key, hotkey-recorder, key-sequences.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://tanstack.com/hotkeys/latest'
user-invocable: false
---

# TanStack Hotkeys

## Overview

TanStack Hotkeys is a type-safe keyboard shortcuts library for React with template-string bindings, cross-platform `Mod` key abstraction (Cmd on macOS, Ctrl on Windows/Linux), and SSR-friendly utilities. It provides hooks for single hotkeys, multi-key sequences, shortcut recording, and real-time key state tracking, plus platform-aware display formatting.

**When to use:** Adding keyboard shortcuts to React apps, recording user-defined hotkeys, detecting held modifier keys, displaying platform-specific shortcut labels, implementing Vim-style key sequences.

**When NOT to use:** Non-React apps without a wrapper (core package exists but React is the primary target), complex input handling that needs full keymap management (consider a dedicated keymap library).

## Quick Reference

| Pattern              | API                   | Key Points                                                  |
| -------------------- | --------------------- | ----------------------------------------------------------- |
| Single hotkey        | `useHotkey`           | `Mod` abstracts Cmd/Ctrl; auto-prevents default on combos   |
| Multi-key sequence   | `useHotkeySequence`   | Vim-style sequences like `g g`; configurable timeout        |
| Record shortcuts     | `useHotkeyRecorder`   | User-defined shortcuts; start/stop/cancel recording         |
| Detect key held      | `useKeyHold`          | Boolean for specific key; optimized re-renders              |
| Track all held keys  | `useHeldKeys`         | Array of currently pressed key names                        |
| Track held key codes | `useHeldKeyCodes`     | Map of key names to physical `event.code` values            |
| Global defaults      | `HotkeysProvider`     | Set default options for all hooks; per-hook overrides apply |
| Format for display   | `formatForDisplay`    | Platform-aware: macOS symbols vs Windows/Linux text         |
| Scope to element     | `target` option + ref | Requires `tabIndex` on target element for focus             |
| Conditional hotkeys  | `enabled` option      | Dynamically enable/disable without unmounting               |

## Common Mistakes

| Mistake                                       | Correct Pattern                                                            |
| --------------------------------------------- | -------------------------------------------------------------------------- |
| Missing `tabIndex` on scoped target element   | Add `tabIndex={-1}` (or `0`) to elements using `target` ref for focus      |
| Using `Ctrl` instead of `Mod`                 | Use `Mod` for cross-platform; it maps to Cmd (Mac) or Ctrl (Win/Linux)     |
| Assuming hotkeys fire inside inputs           | `ignoreInputs` defaults to smart detection; set `false` to force firing    |
| Duplicate hotkey registrations without config | Set `conflictBehavior: 'replace'` to override, or `'error'` to catch       |
| Forgetting `preventDefault` is auto-enabled   | Modifier combos auto-prevent; set `preventDefault: false` to allow default |
| Using `keyup` without `requireReset`          | Combine `eventType: 'keyup'` with `requireReset: true` to fire once        |

## Delegation

> If the `tanstack-pacer` skill is available, delegate throttling and debouncing tasks to it. TanStack Pacer is useful for rate-limiting hotkey callbacks.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-pacer -a claude-code -y`
>
> If the `tanstack-devtools` skill is available, delegate devtools setup to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-devtools -a claude-code -y`

- **Keyboard shortcuts and hotkeys**: Use this skill
- **Throttling/debouncing hotkey callbacks**: Delegate to `tanstack-pacer`
- **DevTools integration**: Delegate to `tanstack-devtools`

## References

- [React hooks and configuration](references/react-hooks.md)
- [Sequences and recording](references/sequences-and-recording.md)
- [Formatting and display](references/formatting-and-display.md)
