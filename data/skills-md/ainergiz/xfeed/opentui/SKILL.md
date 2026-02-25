---
name: opentui
description: Build terminal UIs with OpenTUI/React. Use when creating screens, components, handling keyboard input, managing scroll, or navigating between views. Covers JSX intrinsics, useKeyboard, scrollbox patterns, and state preservation.
---

# OpenTUI/React Quick Reference

OpenTUI is a React renderer for terminal UIs using Yoga layout (like React Native). **NOT React DOM or Ink.**

## Version Info

- **Current:** 0.1.69 (updated), **Latest:** 0.1.69
- **Context repo:** `.context/repos/opentui` (run `bun run sync-context` if missing)

## Core Imports

```typescript
import { useKeyboard, useRenderer, useTerminalDimensions } from "@opentui/react";
import type { ScrollBoxRenderable, KeyEvent } from "@opentui/core";
```

## JSX Elements (Lowercase!)

```tsx
// CORRECT - OpenTUI intrinsics
<box style={{ flexDirection: "column" }}>
  <text fg="#ffffff">Hello</text>
  <scrollbox ref={scrollRef} focused />
</box>

// WRONG - Not OpenTUI
<div>, <span>, <Box>, <Text>
```

| Element | Purpose | Key Props |
|---------|---------|-----------|
| `<box>` | Container/layout | `style`, `id`, `onMouse` |
| `<text>` | Text content (strings only!) | `fg`, `bg`, `selectable` |
| `<scrollbox>` | Scrollable container | `ref`, `focused` |
| `<a>` | Hyperlink (OSC8) | `href`, `fg` |
| `<input>` | Text input | `focused`, `onInput`, `onSubmit` |
| `<textarea>` | Multi-line input | `ref`, `focused`, `placeholder` |

## Critical Rules

### 1. Text Only Accepts Strings

```tsx
// WRONG - Cannot nest elements in <text>
<text>Hello <text fg="red">world</text></text>

// CORRECT - Use row box for inline styling
<box style={{ flexDirection: "row" }}>
  <text>Hello </text>
  <text fg="red">world</text>
</box>
```

### 2. Always Check `focused` in Keyboard Handlers

```tsx
useKeyboard((key) => {
  if (!focused) return;  // MUST check first!
  if (key.name === "j") moveDown();
});
```

### 3. Save Scroll Position Synchronously

```tsx
// WRONG - useEffect runs after render, scroll already reset
useEffect(() => { if (!focused) savedScroll.current = scrollRef.current?.scrollTop; }, [focused]);

// CORRECT - Save before state change
const handleSelect = () => {
  savedScroll.current = scrollRef.current?.scrollTop;  // Save first!
  onSelect(item);
};
```

## Hyperlinks (New in 0.1.64+)

```tsx
<text>
  Visit <a href="https://example.com">example.com</a> for more
</text>
```

Renders clickable links in terminals supporting OSC8 (iTerm2, Kitty, etc.).

## Key Names

| Key | `key.name` | | Key | `key.name` |
|-----|------------|--|-----|------------|
| Enter | `"return"` | | Arrows | `"up"`, `"down"`, `"left"`, `"right"` |
| Escape | `"escape"` | | Letters | `"a"`, `"b"`, `"j"`, `"k"` |
| Tab | `"tab"` | | Shift+Letter | `"A"`, `"B"`, `"G"` |

## Scrollbox API

```typescript
const scrollbox = scrollRef.current;
scrollbox.scrollTop           // Current position
scrollbox.scrollHeight        // Total content height
scrollbox.viewport.height     // Visible area
scrollbox.scrollTo(pos)       // Absolute scroll
scrollbox.scrollBy(delta)     // Relative scroll
scrollbox.getChildren()       // Find elements by ID
```

## Common Layout Patterns

```tsx
// Full-height with fixed header/footer
<box style={{ flexDirection: "column", height: "100%" }}>
  <box style={{ flexShrink: 0 }}>{/* Header */}</box>
  <scrollbox style={{ flexGrow: 1 }}>{/* Content */}</scrollbox>
  <box style={{ flexShrink: 0 }}>{/* Footer */}</box>
</box>

// Prevent unwanted spacing (Yoga quirk)
<box style={{ justifyContent: "flex-start", marginBottom: 0, paddingBottom: 0 }}>
```

## React DevTools (Optional)

```bash
bun add --dev react-devtools-core@7
npx react-devtools@7  # Start standalone devtools
DEV=true bun run start  # Run app with devtools enabled
```

## Detailed References

- [COMPONENTS.md](COMPONENTS.md) - JSX elements, styling, text nesting
- [KEYBOARD.md](KEYBOARD.md) - Keyboard handling, key names, focus patterns
- [SCROLLBOX.md](SCROLLBOX.md) - Scrollbox API, scroll preservation, windowed lists
- [LAYOUT.md](LAYOUT.md) - Flex layout, Yoga engine, spacing issues
- [PATTERNS.md](PATTERNS.md) - Screen navigation, state preservation, library compatibility

## xfeed Reference Files

- `src/app.tsx` - Screen routing, navigation history
- `src/components/PostList.tsx` - Scrollbox with preservation
- `src/components/PostCard.tsx` - Component styling, mouse handling
- `src/modals/FolderPicker.tsx` - Windowed list pattern
- `src/hooks/useListNavigation.ts` - Vim-style navigation
