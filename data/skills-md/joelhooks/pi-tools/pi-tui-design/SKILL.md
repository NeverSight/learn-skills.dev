---
name: pi-tui-design
description: "Create distinctive, crafted TUI components for pi using @mariozechner/pi-tui and @mariozechner/pi-coding-agent. Use when building interactive terminal UIs — custom components, overlays, dialogs, dashboards, widgets, data visualizations, animated elements, game-like interfaces, or any visual TUI work inside pi extensions or custom tools. Triggers on: 'build a TUI component', 'make a dashboard', 'create an overlay', 'interactive widget', 'terminal UI', 'custom component', 'pi-tui', or any request to create visual, interactive terminal interfaces. Also use when beautifying or redesigning existing TUI components."
---

# TUI Design for Pi

Build terminal interfaces that feel *crafted*, not generated. The terminal is constrained — fixed-width character grid, keyboard only, theme-dependent colors — and those constraints are a design feature.

## Design Thinking

Before coding, commit to a direction:

- **Tone**: Minimal and precise? Dense and information-rich? Playful? Industrial? The terminal has its own aesthetic vocabulary — box-drawing elegance, braille-pattern density, block-element weight, symbol clarity.
- **Scope**: Full-screen takeover (`ctx.ui.custom`)? Floating overlay? Persistent widget? Status line? Tool rendering? Match the delivery surface to the interaction weight.
- **Differentiation**: What detail makes this feel intentional? A progress bar with braille resolution. Aligned columns with accent headers. A dialog with breathing room.

## Terminal Aesthetic Vocabulary

### Unicode Repertoire — Your Typography

Terminal UIs have no font choices. Instead, the *character repertoire* is the typography:

| Category | Characters | Use |
|----------|-----------|-----|
| Box-drawing (light) | `─│┌┐└┘├┤┬┴┼` | Standard borders, tables |
| Box-drawing (rounded) | `╭╮╰╯` | Softer, modern feel |
| Box-drawing (heavy) | `━┃┏┓┗┛┣┫┳┻╋` | Emphasis, headers |
| Box-drawing (double) | `═║╔╗╚╝╠╣╦╩╬` | Formal, structured |
| Block elements | `█▓▒░▀▄▌▐` | Progress bars, density, fill |
| Braille | `⠀⠁⠂⠃...⣿` | High-resolution patterns, sparklines, charts |
| Symbols | `◆●○◉◎✓✗▸▹▶▷△▽★☆♦` | Status indicators, bullets, selections |
| Math/arrows | `→←↑↓↔↕⇒⟶⟵∙⋯` | Navigation hints, flow |
| Powerline | `░` | Segment separators (terminal-dependent) |

**Hierarchy through character weight**: `█` (heavy) → `▓` (medium) → `▒` (light) → `░` (subtle) → ` ` (empty). Use this for visual density gradients, not just fill.

**Aspect ratio**: Terminal cells are ~2:1 (twice as tall as wide). A `██` (two block chars) reads as roughly square. Account for this in any spatial layout — the snake.ts example uses `cellWidth = 2` for this reason.

### Color Discipline

**Always use pi's theme tokens.** Hardcoded ANSI escapes break when users switch themes.

```typescript
// ✗ Hardcoded — breaks on theme change
const red = (s: string) => `\x1b[31m${s}\x1b[0m`;

// ✓ Theme-aware — adapts to dark/light, custom themes
const header = theme.fg("accent", theme.bold("Title"));
const status = theme.fg("success", "✓ OK");
const muted = theme.fg("muted", "secondary info");
```

**Color hierarchy** (from the 51-token theme system):
- `accent` — primary attention, selections, active elements
- `text` — default body content (usually `""` = terminal default)
- `muted` — secondary, de-emphasized
- `dim` — tertiary, barely visible
- `success` / `error` / `warning` — semantic status
- `border` / `borderAccent` / `borderMuted` — structural elements
- `toolTitle` — headers in tool-like contexts

**Background colors** for regions: `selectedBg`, `userMessageBg`, `customMessageBg`, `toolPendingBg`, `toolSuccessBg`, `toolErrorBg`.

**Rule**: One accent color dominates. Use `muted`/`dim` for everything secondary. Overusing color flattens the hierarchy — a wall of green is worse than no color at all.

### Spatial Composition

The `width` parameter is your canvas edge. Every line from `render()` must not exceed it.

**Padding rhythm**: Consistent horizontal padding creates visual breathing room. `paddingX=1` (one space each side) is the baseline. Headers may deserve `paddingX=2`. Cramped UIs feel hostile.

**Alignment**: Right-align numbers, left-align labels. Use `visibleWidth()` to calculate ANSI-aware column widths. Pad with spaces, not tabs.

**Negative space**: An empty `Spacer(1)` between sections does more than a separator line. Let content breathe.

**Box nesting**: `Container > Box > [children]` gives you padding + background + vertical stacking. Don't flatten everything into one render function — compose components.

### Motion and Animation

No CSS transitions. Timer-based updates via `setInterval` + `tui.requestRender()`.

```typescript
// Spinner pattern (see Loader component)
const frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
this.interval = setInterval(() => {
  this.frame = (this.frame + 1) % frames.length;
  this.invalidate();
  tui.requestRender();
}, 80);
```

**Patterns**: Braille spinners, block-element progress bars, staggered list reveals (render items one by one with delay), typewriter text, pulsing indicators.

**Cleanup is mandatory**: Clear intervals in `dispose()`. Leaked timers cause rendering after component removal.

### Keyboard Interaction Design

Keyboard is the only input. Make it discoverable and consistent.

**Standard conventions** (users expect these):
- `↑↓` or `j/k` — navigate lists
- `Enter` — confirm/select
- `Escape` — cancel/back
- `Tab` — next field
- `/` or start typing — search/filter

**Always show hints**: Footer line with available keys. Use `keyHint()` for theme-aware formatting.

```typescript
const help = theme.fg("dim", "↑↓ navigate • enter select • esc cancel");
```

**Use `matchesKey()` from pi-tui** — handles terminal escape sequence differences:

```typescript
import { matchesKey, Key } from "@mariozechner/pi-tui";

handleInput(data: string) {
  if (matchesKey(data, Key.up)) { /* ... */ }
  else if (matchesKey(data, Key.enter)) { /* ... */ }
  else if (matchesKey(data, Key.escape)) { /* ... */ }
  else if (matchesKey(data, Key.ctrl("c"))) { /* ... */ }
}
```

## The Component Contract

Every pi-tui component implements:

```typescript
interface Component {
  render(width: number): string[];   // Lines of output, each ≤ width
  handleInput?(data: string): void;  // Keyboard input when focused
  wantsKeyRelease?: boolean;         // Kitty protocol key release events
  invalidate(): void;                // Clear cached render state
}
```

**Critical rules**:
1. Each line from `render()` must not exceed `width` — use `truncateToWidth()`
2. Call `invalidate()` when state changes, then `tui.requestRender()` to trigger re-render
3. Cache rendered output (`cachedLines`/`cachedWidth`) — re-compute only when state or width changes
4. Reapply styles per line — ANSI resets at line boundaries

### Caching Pattern

```typescript
private cachedWidth?: number;
private cachedLines?: string[];
private version = 0;
private cachedVersion = -1;

render(width: number): string[] {
  if (this.cachedLines && this.cachedWidth === width && this.cachedVersion === this.version) {
    return this.cachedLines;
  }
  // ... compute lines ...
  this.cachedWidth = width;
  this.cachedLines = lines;
  this.cachedVersion = this.version;
  return lines;
}

invalidate(): void {
  this.cachedWidth = undefined;
  this.cachedLines = undefined;
}
```

Increment `this.version` on state changes. Theme changes call `invalidate()` automatically.

### Theme Invalidation

If you pre-bake theme colors into child components, rebuild them on `invalidate()`:

```typescript
override invalidate(): void {
  super.invalidate();      // Clear child render caches
  this.rebuildContent();   // Re-apply current theme colors
}
```

## Available Components

### From `@mariozechner/pi-tui`

| Component | Purpose | Key API |
|-----------|---------|---------|
| `Text` | Multi-line word-wrapped text | `new Text(content, paddingX, paddingY, bgFn?)`, `.setText()` |
| `TruncatedText` | Single-line truncated text | `new TruncatedText(text, paddingX, paddingY)` |
| `Box` | Padded container with background | `new Box(paddingX, paddingY, bgFn)`, `.addChild()`, `.setBgFn()` |
| `Container` | Vertical stack of children | `.addChild()`, `.removeChild()`, `.clear()` |
| `Spacer` | Empty vertical space | `new Spacer(lines)` |
| `Markdown` | Rendered markdown with syntax highlighting | `new Markdown(content, paddingX, paddingY, mdTheme)` |
| `Image` | Terminal image (Kitty/iTerm2/Ghostty/WezTerm) | `new Image(base64, mimeType, theme, options)` |
| `SelectList` | Interactive list with filter/scroll | items, maxVisible, theme; `.onSelect`, `.onCancel` |
| `SettingsList` | Toggle settings with values | items, maxVisible, theme, onChange, onClose |
| `Loader` | Braille spinner with message | `new Loader(tui, spinnerColor, messageColor, message)` |
| `CancellableLoader` | Loader with escape-to-cancel | wraps Loader with abort signal |
| `Input` | Single-line text input | implements `Focusable` for IME cursor positioning |
| `Editor` | Multi-line text editor | full editing with undo, kill-ring, keybindings |

### From `@mariozechner/pi-coding-agent`

| Component | Purpose | Key API |
|-----------|---------|---------|
| `DynamicBorder` | Width-adaptive horizontal border | `new DynamicBorder((s: string) => theme.fg("accent", s))` |
| `BorderedLoader` | Loader with borders + cancel | `new BorderedLoader(tui, theme, message)`, `.signal`, `.onAbort` |
| `CustomEditor` | Editor with app keybindings baked in | Extend for modal editing (vim), custom shortcuts |

### Utilities

```typescript
import { visibleWidth, truncateToWidth, wrapTextWithAnsi } from "@mariozechner/pi-tui";
import { matchesKey, Key } from "@mariozechner/pi-tui";
import { DynamicBorder, getMarkdownTheme, keyHint } from "@mariozechner/pi-coding-agent";
```

- `visibleWidth(str)` — display width ignoring ANSI escape codes
- `truncateToWidth(str, width, ellipsis?)` — truncate with optional ellipsis
- `wrapTextWithAnsi(str, width)` — word wrap preserving ANSI codes
- `matchesKey(data, key)` — compare keyboard input against key identifiers
- `getMarkdownTheme()` — theme object for `Markdown` component
- `keyHint(action, description)` — theme-aware keybinding hint text

## Delivery Surfaces

Choose the right surface for the interaction:

### Full-screen takeover — `ctx.ui.custom(component)`

For complex interactions: dashboards, games, multi-step wizards.

```typescript
await ctx.ui.custom((tui, theme, keybindings, done) => {
  return new MyComponent(tui, theme, () => done(result));
});
```

### Overlay — `ctx.ui.custom(factory, { overlay: true })`

Floats on top of existing content. For quick selections, confirmations, panels.

```typescript
const result = await ctx.ui.custom<string | null>(
  (tui, theme, kb, done) => new MyDialog(theme, done),
  {
    overlay: true,
    overlayOptions: {
      anchor: "center",        // 9 positions: center, top-left, top-center, etc.
      width: "50%",            // number or percentage string
      minWidth: 40,
      maxHeight: "80%",
      offsetX: -2, offsetY: 0,
      margin: 2,               // or { top, right, bottom, left }
      visible: (w, h) => w >= 80,  // responsive hide
    },
  }
);
```

### Widget — `ctx.ui.setWidget(id, lines|factory, options?)`

Persistent display above or below the editor. For status, progress, lists.

```typescript
ctx.ui.setWidget("my-widget", (tui, theme) => ({
  render: () => [theme.fg("accent", "● Active") + " — 3 items pending"],
  invalidate: () => {},
}));
// placement: "belowEditor" for below
// Clear: ctx.ui.setWidget("my-widget", undefined)
```

### Status line — `ctx.ui.setStatus(id, content)`

Single-line persistent indicator in footer.

```typescript
ctx.ui.setStatus("mode", theme.fg("accent", "● DESIGN"));
// Clear: ctx.ui.setStatus("mode", undefined)
```

### Tool rendering — `renderCall`/`renderResult`

Custom display for tool calls in the conversation. Return `Text` components with `(0, 0)` padding — the wrapping `Box` handles padding.

```typescript
renderCall(args, theme) {
  return new Text(theme.fg("toolTitle", theme.bold("my_tool ")) + theme.fg("muted", args.action), 0, 0);
},
renderResult(result, { expanded, isPartial }, theme) {
  if (isPartial) return new Text(theme.fg("warning", "Working..."), 0, 0);
  let text = theme.fg("success", "✓ Done");
  if (expanded) text += "\n" + theme.fg("dim", JSON.stringify(result.details, null, 2));
  return new Text(text, 0, 0);
}
```

### Footer — `ctx.ui.setFooter(factory)`

Replace the entire footer bar. Access git branch, extension statuses, token stats.

```typescript
ctx.ui.setFooter((tui, theme, footerData) => ({
  render: (width) => [truncateToWidth(`${model} (${footerData.getGitBranch() || "no git"})`, width)],
  invalidate: () => {},
  dispose: footerData.onBranchChange(() => tui.requestRender()),
}));
```

## TUI Anti-Patterns

**The equivalent of "AI slop" in terminal UIs:**

| Don't | Do |
|-------|-----|
| Hardcoded ANSI colors (`\x1b[31m`) | Theme tokens (`theme.fg("error", ...)`) |
| Lines exceeding `width` parameter | `truncateToWidth()` on every line |
| No `invalidate()` (stale cached renders) | Full cache-clearing on state change |
| Ignoring cell aspect ratio (2:1) | Double-width chars for "square" elements |
| Wall of unstructured text | Sections with Spacer, borders, alignment |
| Missing keyboard hints | Footer line showing available keys |
| Leaked intervals/timers | `dispose()` with cleanup |
| Pre-baked theme colors without rebuild | Override `invalidate()` to rebuild themed content |
| Flat render functions with no composition | Container → Box → children hierarchy |
| Same visual treatment for every component | Intentional aesthetic direction per component |
| Generic spinner for all loading states | Context-appropriate progress (bar, percentage, step count) |
| Fixed-width layouts | Responsive to `width` param, `minWidth` guards |

## Copy-Paste Examples

See [references/examples.md](references/examples.md) for complete, self-contained component implementations:

- **Selection dialog** — SelectList + DynamicBorder + keyboard hints
- **Status dashboard** — Multi-section box-drawing layout, aligned columns, semantic color
- **Progress tracker** — Animated braille bar, timer lifecycle, dispose cleanup
- **Data table** — Scrollable rows, column alignment, row highlighting
- **Persistent widget** — Above-editor health indicator, single-line compact
- **Tool renderer** — renderCall/renderResult with expandable detail
- **Overlay panel** — Side panel, responsive visibility, anchor positioning

## Upstream Examples

The pi repo extension examples demonstrate more patterns:

- **snake.ts**: Full game loop, box-drawing borders, session persistence via `pi.appendEntry()`
- **space-invaders.ts**: Kitty key release events (`wantsKeyRelease`), multi-entity rendering
- **overlay-qa-tests.ts**: All 9 anchor positions, responsive visibility, animation at ~30 FPS
- **preset.ts**: SelectList with DynamicBorder — the standard dialog pattern
- **plan-mode**: setStatus + setWidget for persistent mode indicators
- **todo.ts**: Custom tool rendering with renderCall/renderResult
