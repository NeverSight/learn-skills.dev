---
name: border-beam-react
description: Animated border beam/glow effect component for React applications
triggers:
  - add animated border beam effect
  - traveling glow animation around element
  - border beam react component
  - animated glow border card
  - border beam effect
  - add glow animation to card or button
  - animated border highlight react
  - border-beam component usage
---

# border-beam-react

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`border-beam` is a lightweight React component that renders an animated traveling glow/beam effect around any element — cards, buttons, inputs, search bars, or any container. It uses CSS `@property` for GPU-accelerated animations with no runtime animation libraries required.

## Installation

```bash
npm install border-beam
```

**Requirements:**
- React 18+
- Modern browser: Chrome 85+, Safari 15.4+, Firefox 128+

## Basic Usage

```tsx
import { BorderBeam } from 'border-beam';

function App() {
  return (
    <BorderBeam>
      <div style={{ padding: 32, borderRadius: 16, background: '#1d1d1d' }}>
        Your content here
      </div>
    </BorderBeam>
  );
}
```

`BorderBeam` wraps your content and auto-detects the `border-radius` of the first child element. All effect layers use `pointer-events: none` so they never block interaction.

## Size Presets

```tsx
// Full border glow (default) — for cards, panels
<BorderBeam size="md">
  <Card />
</BorderBeam>

// Compact glow — for small elements like icon buttons
<BorderBeam size="sm">
  <IconButton />
</BorderBeam>

// Bottom-only traveling glow — ideal for search bars, inputs
<BorderBeam size="line">
  <SearchBar />
</BorderBeam>
```

## Color Variants

```tsx
<BorderBeam colorVariant="colorful" /> {/* Rainbow spectrum (default), animates hue */}
<BorderBeam colorVariant="mono" />     {/* Grayscale, no hue animation */}
<BorderBeam colorVariant="ocean" />    {/* Blue-purple tones */}
<BorderBeam colorVariant="sunset" />   {/* Orange-yellow-red tones */}
```

All variants except `mono` animate through a hue-shift cycle by default.

## Theme (Dark / Light / Auto)

```tsx
<BorderBeam theme="dark" />  {/* Default — for dark backgrounds */}
<BorderBeam theme="light" /> {/* For light backgrounds */}
<BorderBeam theme="auto" />  {/* Detects system prefers-color-scheme */}
```

## Controlling Intensity

```tsx
// strength: 0 (invisible) to 1 (full, default) — only affects beam layers
<BorderBeam strength={0.6}>
  <Card />
</BorderBeam>

// brightness and saturation multipliers
<BorderBeam brightness={1.5} saturation={1.4}>
  <Card />
</BorderBeam>
```

## Play / Pause with Callbacks

```tsx
import { useState } from 'react';
import { BorderBeam } from 'border-beam';

function AnimatedCard() {
  const [active, setActive] = useState(true);

  return (
    <>
      <BorderBeam
        active={active}
        onActivate={() => console.log('Beam faded in')}
        onDeactivate={() => console.log('Beam faded out')}
      >
        <div style={{ padding: 32, borderRadius: 16, background: '#111' }}>
          Hover-activated beam
        </div>
      </BorderBeam>
      <button onClick={() => setActive(a => !a)}>Toggle Beam</button>
    </>
  );
}
```

## Custom Duration and Hue Range

```tsx
<BorderBeam
  duration={3.5}      // Animation cycle in seconds (default: 1.96 for md, 2.4 for line)
  hueRange={60}       // Hue rotation range in degrees (default: 30)
  staticColors={true} // Disable hue-shift entirely
>
  <Card />
</BorderBeam>
```

## Custom Border Radius

If auto-detection doesn't work (e.g., the radius is set via a CSS class), override it:

```tsx
<BorderBeam borderRadius={24}>
  <div className="my-card">Content</div>
</BorderBeam>
```

## Forwarded HTML Attributes

The wrapper `<div>` forwards all standard `HTMLDivElement` attributes:

```tsx
<BorderBeam
  className="my-wrapper"
  style={{ display: 'inline-block' }}
  data-testid="beam-card"
>
  <Card />
</BorderBeam>
```

## Common Patterns

### Hover-activated beam

```tsx
import { useState } from 'react';
import { BorderBeam } from 'border-beam';

function HoverCard() {
  const [hovered, setHovered] = useState(false);

  return (
    <BorderBeam active={hovered} strength={0.85} colorVariant="ocean">
      <div
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
        style={{ padding: 24, borderRadius: 12, background: '#0f0f0f' }}
      >
        Hover me
      </div>
    </BorderBeam>
  );
}
```

### Search bar with line beam

```tsx
import { BorderBeam } from 'border-beam';

function SearchInput() {
  return (
    <BorderBeam size="line" colorVariant="sunset" theme="dark">
      <input
        type="text"
        placeholder="Search..."
        style={{
          padding: '12px 16px',
          borderRadius: 8,
          background: '#1a1a1a',
          border: '1px solid #333',
          color: '#fff',
          width: 320,
        }}
      />
    </BorderBeam>
  );
}
```

### Light theme card

```tsx
import { BorderBeam } from 'border-beam';

function LightCard() {
  return (
    <BorderBeam theme="light" colorVariant="colorful" strength={0.8}>
      <div style={{ padding: 32, borderRadius: 16, background: '#f5f5f5' }}>
        Light mode card
      </div>
    </BorderBeam>
  );
}
```

### Reduced motion accessibility

The component itself does not automatically respond to `prefers-reduced-motion`. Handle it in the consumer:

```tsx
import { useReducedMotion } from 'framer-motion'; // or your own hook
import { BorderBeam } from 'border-beam';

function AccessibleCard() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  return (
    <BorderBeam active={!reduceMotion}>
      <Card />
    </BorderBeam>
  );
}
```

## Full Props Reference

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Content to wrap |
| `size` | `'sm' \| 'md' \| 'line'` | `'md'` | Size/type preset |
| `colorVariant` | `'colorful' \| 'mono' \| 'ocean' \| 'sunset'` | `'colorful'` | Color palette |
| `theme` | `'dark' \| 'light' \| 'auto'` | `'dark'` | Background adaptation |
| `strength` | `number` | `1` | Beam opacity 0–1, does not affect children |
| `duration` | `number` | `1.96` / `2.4` | Animation cycle in seconds |
| `active` | `boolean` | `true` | Play/pause with fade transition |
| `borderRadius` | `number` | auto-detected | Override border radius in px |
| `brightness` | `number` | `1.3` | Glow brightness multiplier |
| `saturation` | `number` | `1.2` | Glow saturation multiplier |
| `hueRange` | `number` | `30` | Hue rotation range in degrees |
| `staticColors` | `boolean` | `false` | Disable hue-shift animation |
| `className` | `string` | — | Class on wrapper div |
| `style` | `CSSProperties` | — | Inline styles on wrapper div |
| `onActivate` | `() => void` | — | Called when fade-in completes |
| `onDeactivate` | `() => void` | — | Called when fade-out completes |

## How It Works

`BorderBeam` renders a wrapper `<div>` with three effect layers — all `pointer-events: none`, absolutely positioned, never affecting layout or interaction:

- **`::after`** — beam stroke (conic gradient masked to the border edge)
- **`::before`** — inner glow layer
- **`[data-beam-bloom]`** — outer bloom/glow child `<div>`

Animations use CSS `@property` for smooth, GPU-accelerated hue cycling.

## Troubleshooting

**Beam not visible:**
- Ensure the child element has a visible `background` and `border-radius`
- Check `strength` is not `0`
- Verify `active` is `true`

**Border radius not matching:**
- Pass `borderRadius` prop explicitly if the radius comes from a CSS class rather than inline style

**Effect covers content / blocks clicks:**
- All layers are `pointer-events: none` by default — if this is happening, check for CSS conflicts in your wrapper

**Animation not working in browser:**
- Requires CSS `@property` support: Chrome 85+, Safari 15.4+, Firefox 128+. Check [caniuse.com/@property](https://caniuse.com/css-at-property)

**SSR / Next.js:**
- The component uses DOM APIs for border-radius detection; wrap in a client component (`'use client'`) in Next.js App Router
