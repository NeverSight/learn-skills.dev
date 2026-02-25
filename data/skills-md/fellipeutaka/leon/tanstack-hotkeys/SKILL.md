---
name: tanstack-hotkeys
description: Guide for implementing keyboard shortcuts in React using @tanstack/react-hotkeys. Use when building hotkey/shortcut features, registering keyboard shortcuts, handling key sequences, recording custom shortcuts, tracking held keys, or formatting hotkeys for display in React applications.
---

# TanStack Hotkeys (React)

Type-safe keyboard shortcut management for React. Package: `@tanstack/react-hotkeys`.

All framework packages re-export everything from `@tanstack/hotkeys` core — no separate install needed.

## Quick Start

```tsx
import { useHotkey } from '@tanstack/react-hotkeys'

function App() {
  useHotkey('Mod+S', () => saveDocument())
  return <div>Press Cmd+S (Mac) or Ctrl+S (Windows) to save</div>
}
```

`Mod` resolves to `Meta` (Cmd) on macOS, `Control` on Windows/Linux.

## Core Hooks

### `useHotkey(hotkey, callback, options?)`

Primary hook. Accepts string (`'Mod+S'`) or `RawHotkey` object (`{ key: 'S', mod: true }`).

Callback receives `(event: KeyboardEvent, context: { hotkey, parsedHotkey })`.

Auto-syncs callback every render (no stale closures). Auto-cleans up on unmount.

```tsx
// String form
useHotkey('Mod+S', () => save())

// Object form
useHotkey({ key: 'S', mod: true }, () => save())

// Conditional
useHotkey('Escape', () => onClose(), { enabled: isOpen })

// Scoped to element (must be focusable — add tabIndex)
const ref = useRef<HTMLDivElement>(null)
useHotkey('Escape', () => close(), { target: ref })
```

**Default options:**

| Option | Default | Notes |
|---|---|---|
| `enabled` | `true` | |
| `preventDefault` | `true` | Overrides browser defaults like Cmd+S |
| `stopPropagation` | `true` | |
| `eventType` | `'keydown'` | Also supports `'keyup'` |
| `requireReset` | `false` | When true, fires once until all keys released |
| `ignoreInputs` | smart | `false` for Ctrl/Meta combos & Escape; `true` for single keys & Shift/Alt combos |
| `target` | `document` | Accepts DOM element, `window`, or React ref |
| `conflictBehavior` | `'warn'` | `'error'`, `'replace'`, `'allow'` |

### `useHotkeySequence(sequence, callback, options?)`

Vim-style multi-key sequences. Keys pressed in order within timeout.

```tsx
useHotkeySequence(['G', 'G'], () => scrollToTop())
useHotkeySequence(['D', 'I', 'W'], () => deleteInnerWord(), { timeout: 500 })

// With modifiers
useHotkeySequence(['Mod+K', 'Mod+C'], () => commentSelection())
```

Options: `timeout` (default 1000ms), `enabled` (default true).

Overlapping prefixes work — manager tracks each independently.

### `useHotkeyRecorder(options)`

Record custom shortcuts. Returns `{ isRecording, recordedHotkey, startRecording, stopRecording, cancelRecording }`.

- Escape cancels recording
- Backspace/Delete clears recorded hotkey
- Auto-converts to portable `Mod` format (Meta+S becomes Mod+S)

```tsx
const recorder = useHotkeyRecorder({
  onRecord: (hotkey) => setShortcut(hotkey),
  onCancel: () => console.log('cancelled'),
  onClear: () => console.log('cleared'),
})
```

### Key State Tracking

```tsx
// All held keys
const heldKeys = useHeldKeys() // string[]

// Single key check (optimized — only re-renders when this key changes)
const isShiftHeld = useKeyHold('Shift') // boolean

// Key-to-code mapping (distinguish left/right modifiers)
const codes = useHeldKeyCodes() // Record<string, string>
```

## Display Formatting

```tsx
import { formatForDisplay, formatWithLabels } from '@tanstack/react-hotkeys'

// Platform-aware symbols
formatForDisplay('Mod+S')        // Mac: "⌘S" | Windows: "Ctrl+S"
formatForDisplay('Mod+Shift+Z')  // Mac: "⇧⌘Z" | Windows: "Ctrl+Shift+Z"

// Text labels
formatWithLabels('Mod+S')        // Mac: "Cmd+S" | Windows: "Ctrl+S"
```

Use in UI:

```tsx
<button>Save <kbd>{formatForDisplay('Mod+S')}</kbd></button>
```

## `HotkeysProvider`

Set global defaults for all hooks. Per-hook options override.

```tsx
import { HotkeysProvider } from '@tanstack/react-hotkeys'

<HotkeysProvider defaultOptions={{
  hotkey: { preventDefault: true },
  hotkeySequence: { timeout: 1500 },
  hotkeyRecorder: { onCancel: () => console.log('cancelled') },
}}>
  <App />
</HotkeysProvider>
```

## Devtools

```sh
npm install @tanstack/react-devtools @tanstack/react-hotkeys-devtools
```

```tsx
import { TanStackDevtools } from '@tanstack/react-devtools'
import { hotkeysDevtoolsPlugin } from '@tanstack/react-hotkeys-devtools'

<TanStackDevtools plugins={[hotkeysDevtoolsPlugin()]} />
```

Auto-excluded from production builds. Use `@tanstack/react-hotkeys-devtools/production` import to include in prod.

## Key Patterns

- **Scoped hotkeys**: Pass `target: ref` + ensure element has `tabIndex`
- **Conditional**: Use `enabled` option tied to state
- **Multiple hotkeys**: Each `useHotkey` call is independent
- **Shortcut settings UI**: Combine `useHotkeyRecorder` + `useHotkey` with dynamic bindings + `formatForDisplay`
- **Hold-to-reveal UI**: Use `useKeyHold` to conditionally render elements
- **Shortcut hints overlay**: Show overlay when modifier held via `useKeyHold`

## API Reference

For complete API details including all interfaces, types, utility functions, and core classes, see [references/react-api.md](references/react-api.md).
