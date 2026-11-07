---
name: pi-computer-use
description: Control macOS applications with Pi agents using semantic Accessibility API targets and optional screenshots
triggers:
  - control mac apps with pi agent
  - computer use with pi coding agent
  - automate macos gui with accessibility api
  - pi computer use setup
  - click elements with pi agent
  - use pi to control windows and apps
  - pi agent screen automation
  - pi-computer-use install and usage
---

# pi-computer-use

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`pi-computer-use` gives Pi agents a semantic computer-use surface for visible macOS windows. It prefers Accessibility (AX) targets (like `@e1`) over raw coordinates, returns semantic state after every action, and attaches screenshots only when AX coverage is too weak.

---

## Installation

### Via Pi (recommended)

```bash
pi install git:github.com/injaneity/pi-computer-use#v0.2.1
```

Pin to a specific version:

```bash
pi install -l git:github.com/injaneity/pi-computer-use#v0.2.1
```

### Via npm

```bash
npm install @injaneity/pi-computer-use
# or pin a version
npm install @injaneity/pi-computer-use@0.2.1
```

### Remove

```bash
pi remove git:github.com/injaneity/pi-computer-use#v0.2.1
npm remove @injaneity/pi-computer-use
```

---

## First-Run Permissions

On first session, macOS will prompt for permissions for:

```
~/.pi/agent/helpers/pi-computer-use/bridge
```

Grant both:
- **Accessibility** — required for AX ref targeting
- **Screen Recording** — required for screenshots

---

## How It Works

Three components:

1. **Pi extension** (`extensions/computer-use.ts`) — registers public tools and `/computer-use` command
2. **TypeScript bridge** (`src/bridge.ts`) — manages window state, AX refs, fallback policy, batching, execution metadata
3. **Native Swift helper** (`native/macos/bridge.swift`) — talks to macOS Accessibility, ScreenCaptureKit, AppKit, CoreGraphics

---

## Available Tools

| Tool | Purpose |
|------|---------|
| `list_apps` | List running apps |
| `list_windows` | List windows for an app |
| `screenshot` | Capture window + return AX state |
| `click` | Click element or coordinate |
| `double_click` | Double-click element or coordinate |
| `move_mouse` | Move cursor |
| `drag` | Drag from point to point |
| `scroll` | Scroll element or coordinate |
| `keypress` | Press key combination |
| `type_text` | Type raw text |
| `set_text` | Replace element value via AX |
| `wait` | Pause execution |
| `arrange_window` | Position/resize window |
| `computer_actions` | Batch multiple actions |

---

## Core Workflow

Always start a session with `screenshot` to select the controlled window and obtain AX refs:

```ts
// 1. Discover apps and windows if target is ambiguous
list_apps()
list_windows({ app: "Safari" })

// 2. Select the window and get AX state
screenshot({ window: "@w1" })

// 3. Act on AX refs returned from screenshot
click({ window: "@w1", ref: "@e1" })
set_text({ ref: "@e2", text: "https://example.com" })
keypress({ keys: ["Enter"] })
```

---

## AX Ref Targeting (Preferred)

AX refs like `@e1`, `@e2` are returned by `screenshot` and carry capability metadata:

- `canSetValue` — supports `set_text`
- `canPress` — supports `click`
- `canFocus` — can receive focus
- `canScroll` — supports `scroll`
- `adjust` — supports value adjustment

```ts
// Click by AX ref — no coordinates needed
click({ ref: "@e1" })

// Scroll a specific element
scroll({ ref: "@e3", scrollY: 600 })

// Replace text field value atomically
set_text({ ref: "@e2", text: "hello world" })
```

---

## Coordinate Fallback

Use coordinates **only** when no suitable AX target exists. Always include `stateId` from the latest screenshot to guard against stale state:

```ts
click({ x: 320, y: 180, stateId: "abc123" })
```

---

## Batching Actions

Use `computer_actions` to batch obvious sequential steps. One semantic state update is returned after all actions:

```ts
computer_actions({
  stateId: "abc123",
  actions: [
    { type: "click", ref: "@e1" },
    { type: "set_text", ref: "@e2", text: "https://example.com" },
    { type: "keypress", keys: ["Enter"] }
  ]
})
```

Each action in the result includes execution metadata:
- `stealth` — background-safe AX path (no focus takeover)
- `default` — required focus or raw event fallback

---

## Window Management

```ts
// List windows for a specific app
list_windows({ app: "Finder" })

// Target a specific window in all subsequent calls
screenshot({ window: "@w2" })

// Arrange window by preset
arrange_window({ window: "@w1", preset: "left-half" })

// Arrange window with explicit frame
arrange_window({ window: "@w1", frame: { x: 0, y: 0, width: 1280, height: 800 } })
```

---

## Screenshot Modes

Control when screenshots are attached with the `image` option:

```ts
screenshot({ window: "@w1", image: "auto" })   // default: attach when AX coverage is weak
screenshot({ window: "@w1", image: "always" }) // always attach
screenshot({ window: "@w1", image: "never" })  // never attach, AX state only
```

---

## Common Patterns

### Open URL in Safari

```ts
list_windows({ app: "Safari" })
screenshot({ window: "@w1" })
// @e1 = address bar (from AX state)
set_text({ ref: "@e1", text: "https://example.com" })
keypress({ keys: ["Enter"] })
```

### Fill a Form

```ts
screenshot({ window: "@w1" })
// Use refs from AX state
set_text({ ref: "@e3", text: "Jane Doe" })
set_text({ ref: "@e4", text: "jane@example.com" })
click({ ref: "@e5" }) // Submit button
```

### Keyboard Shortcut

```ts
keypress({ keys: ["Cmd", "T"] })       // New tab
keypress({ keys: ["Cmd", "Shift", "N"] }) // New incognito window
keypress({ keys: ["Escape"] })
```

### Scroll a Page

```ts
scroll({ ref: "@e2", scrollY: 800 })   // Scroll element down
scroll({ ref: "@e2", scrollY: -400 })  // Scroll up
```

### Drag and Drop

```ts
drag({ fromX: 100, fromY: 200, toX: 400, toY: 200 })
```

---

## Strict AX Mode (Stealth / Background-Safe)

Enable strict AX mode to prevent focus changes, raw pointer events, raw keyboard events, and cursor takeover. All actions must succeed via background-safe AX paths:

```ts
// Via config (see Configuration section)
// Actions will report `stealth` in execution metadata when successful
```

Strict mode errors will surface if an action requires foreground focus and strict mode is active.

---

## Configuration

Inspect effective config in Pi:

```
/computer-use
```

Config can be set via config files or environment variable overrides. Key options:

| Option | Description |
|--------|-------------|
| `image` | `"auto"` \| `"always"` \| `"never"` — screenshot attachment mode |
| `strictAX` | Enable background-safe strict AX mode |
| `browser` | Browser-aware targeting preference |

See [`docs/configuration.md`](https://github.com/injaneity/pi-computer-use/blob/main/docs/configuration.md) for full config file format and environment variable overrides.

---

## Development

```bash
# Install dependencies
npm install

# Run checks
npm test

# Run local checkout without loading installed copy
pi --no-extensions -e .
```

### Benchmarks

```bash
# Default QA benchmark
npm run benchmark:qa

# Full benchmark (may open apps)
npm run benchmark:qa:full
```

See [`benchmarks/README.md`](https://github.com/injaneity/pi-computer-use/blob/main/benchmarks/README.md) for metrics, regression policy, and comparison workflow.

---

## Troubleshooting

### Permissions not granted

Re-run and grant both Accessibility and Screen Recording to:
```
~/.pi/agent/helpers/pi-computer-use/bridge
```
On macOS, go to **System Settings → Privacy & Security → Accessibility** and **Screen Recording**.

### AX refs are stale

Take a fresh `screenshot` to get updated `stateId` and new refs before acting. Stale-action detection uses `stateId` to reject outdated coordinates or refs.

### Browser window not targeted correctly

Use `list_windows({ app: "Safari" })` (or Chrome/Firefox) first, then explicitly pass `window: "@wN"` to `screenshot` and subsequent actions.

### Strict AX mode errors

An action failed to complete via background-safe AX path. Either disable strict mode or identify an AX ref with `canPress`/`canSetValue` that supports the background path.

### Helper not found

Ensure Pi installed the native helper:
```bash
ls ~/.pi/agent/helpers/pi-computer-use/bridge
```
If missing, reinstall: `pi install git:github.com/injaneity/pi-computer-use#v0.2.1`

---

## Key Concepts

- **AX refs** (`@e1`, `@e2`, …) — semantic element handles from macOS Accessibility API, stable within a state
- **Window refs** (`@w1`, `@w2`, …) — stable handles from `list_windows`
- **stateId** — opaque ID from the latest screenshot; attach to coordinate-based actions to detect stale state
- **stealth execution** — action completed via AX without foregrounding the app or moving the real cursor
- **semantic state** — structured AX tree returned after every action, used instead of screenshots when coverage is sufficient

---

## References

- [Usage guide](https://github.com/injaneity/pi-computer-use/blob/main/docs/usage.md)
- [Configuration](https://github.com/injaneity/pi-computer-use/blob/main/docs/configuration.md)
- [Troubleshooting](https://github.com/injaneity/pi-computer-use/blob/main/docs/troubleshooting.md)
- [Benchmarks](https://github.com/injaneity/pi-computer-use/blob/main/benchmarks/README.md)
- [Pi](https://pi.dev/)
