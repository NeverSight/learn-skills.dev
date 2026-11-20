---
name: premium-layer
description: The "gatekept" techniques that separate premium UI from AI slop. Grain textures, inner glow borders, surface elevation, desaturated accents, micro-interaction timing. Apply AFTER layout and components are working. Use when a build "looks like a template" or needs to feel expensive.
allowed-tools: Read, Write, Edit
---

# Premium Layer

## TL;DR (5 rules)
1. **Grain texture on every card surface** — SVG feTurbulence at 2-3% opacity (dark mode) or 3-5% (light mode)
2. **Inner glow on elevated elements** — `box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.04)` on dark, `rgba(255,255,255,0.5)` on light
3. **Never use pure white (#FFF) or pure black (#000)** — use #FAFAFA / #09090B (reduces halation and eye strain)
4. **Surface elevation via lightness steps, not borders** — each layer 6-8 lightness points apart
5. **Desaturate accent colors to 70-80% on dark backgrounds** — vibrant hues look neon on dark

## When To Use
- After components work but look "template-y"
- Dashboard or data-heavy UI that feels generic
- Dark mode implementation
- Client says "make it look premium" or "it looks AI-generated"

## Checklist
- [ ] Grain texture applied to card surfaces
- [ ] Inner glow on elevated cards/panels
- [ ] No pure white or pure black anywhere
- [ ] Surface elevation system defined (base → raised → overlay)
- [ ] Borders use rgba opacity (5-10%), not solid colors
- [ ] Accent colors desaturated for dark backgrounds
- [ ] Asymmetric spacing (8px scale: 8/16/24/32/48/64)
- [ ] Micro-interaction timing: 150ms fast, 250ms normal, 350ms slow
- [ ] Scrollbar styled to match theme
- [ ] Financial/data numbers in monospace font

---

## Technique 1: Grain Texture

Adds tactile depth to flat surfaces. The single biggest premium differentiator.

### CSS Utility Class
```css
.grain::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'%3E%3Cfilter id='a'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23a)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 182px;
  pointer-events: none;
  border-radius: inherit;
}

/* Dark mode: subtle */
.grain::before { opacity: 0.025; }

/* Light mode: slightly more visible */
.light .grain::before { opacity: 0.04; }
```

### React Component
```tsx
function GrainOverlay({ opacity = 0.025 }: { opacity?: number }) {
  return (
    <div
      className="absolute inset-0 pointer-events-none rounded-[inherit]"
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'%3E%3Cfilter id='a'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23a)'/%3E%3C/svg%3E")`,
        backgroundRepeat: 'repeat',
        backgroundSize: '182px',
        opacity,
      }}
    />
  );
}
```

**Parameters:**
- `baseFrequency: .65` — grain scale (lower = larger grain)
- `numOctaves: 3` — complexity
- Dark mode opacity: 0.02-0.03
- Light mode opacity: 0.03-0.05
- ALWAYS add `pointer-events: none` and `border-radius: inherit`

---

## Technique 2: Surface Elevation System

Replace visible borders with lightness-step separation. Each layer is 6-8 lightness points above the previous.

### Dark Mode (Recommended)
```css
:root {
  --bg-base: #09090B;      /* Page background — zinc-950 */
  --bg-raised: #18181B;    /* Cards, panels — zinc-900 */
  --bg-overlay: #27272A;   /* Modals, dropdowns, hover states — zinc-800 */

  --border-subtle: rgba(255, 255, 255, 0.06);   /* Barely visible */
  --border-default: rgba(255, 255, 255, 0.10);  /* Standard dividers */
  --border-strong: rgba(255, 255, 255, 0.16);   /* Emphasized borders */
}
```

### Light Mode
```css
:root {
  --bg-base: #F8F9FA;       /* Page background */
  --bg-raised: #FFFFFF;     /* Cards, panels */
  --bg-overlay: #F1F3F5;   /* Hover states, secondary surfaces */

  --border-subtle: rgba(0, 0, 0, 0.06);
  --border-default: rgba(0, 0, 0, 0.10);
  --border-strong: rgba(0, 0, 0, 0.16);
}
```

---

## Technique 3: Inner Glow

Simulates a top-edge light source on cards. Subtle but immediately premium.

```css
/* Dark mode */
.card {
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.04),  /* top edge glow */
    0 1px 3px 0 rgba(0, 0, 0, 0.3);               /* drop shadow */
}

/* Light mode */
.card {
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.5),
    0 1px 3px 0 rgba(0, 0, 0, 0.08);
}
```

---

## Technique 4: Text Color Rules

```
Dark mode:
  --text-primary: #FAFAFA      (not #FFFFFF — reduces halation)
  --text-secondary: #A1A1AA    (zinc-400 — comfortable contrast)
  --text-muted: #71717A        (zinc-500 — labels, timestamps)

Light mode:
  --text-primary: #111827      (not #000000)
  --text-secondary: #4B5563    (gray-600)
  --text-muted: #9CA3AF        (gray-400)
```

**Why not pure white?** On dark backgrounds, pure white (#FFF) creates halation — a glow bleed around letterforms, especially for users with astigmatism (~40% of the population). #FAFAFA or #E0E0E0 is equally readable but gentler.

---

## Technique 5: Accent Color Handling

On dark backgrounds, desaturate accents to 70-80% saturation. Full saturation looks neon.

```css
/* Too vibrant on dark: */
--accent: #22C55E;    /* green-500, 80% saturation — looks neon */

/* Better: */
--accent: #10B981;    /* emerald-500, 70% saturation — sophisticated */
```

**Rule:** When everything is emphasized, nothing is. Limit accent color to:
- Primary CTAs
- Active state indicators
- Critical status badges
- Nothing else.

---

## Technique 6: Border Treatments

### Subtle borders (default)
```css
border: 1px solid rgba(255, 255, 255, 0.06);  /* dark */
border: 1px solid rgba(0, 0, 0, 0.06);        /* light */
```

### Accent-left indicator
```css
border-left: 3px solid var(--accent);  /* sidebar nav, activity items */
```

### Inner top highlight
```css
box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.04);  /* simulates light source */
```

---

## Technique 7: Micro-Interaction Timing

```
Fast (state changes):     150ms, cubic-bezier(0.4, 0, 0.2, 1)
Normal (reveals):         250ms, cubic-bezier(0.4, 0, 0.2, 1)
Slow (page transitions):  350ms, cubic-bezier(0.16, 1, 0.3, 1)

Hover scale:              scale(0.98) on press (NOT 0.95 — too aggressive)
Hover lift:               translateY(-1px) + shadow elevation (NOT -2px)
Spring indicators:        stiffness: 500, damping: 35 (Framer Motion)
```

---

## Technique 8: Scrollbar Styling

```css
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);  /* dark */
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}
```

---

## Technique 9: Status Badge Patterns

### On Dark Backgrounds (tinted transparent)
```css
/* Better than solid pills on dark — creates depth */
.badge-success { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.25); }
.badge-warning { background: rgba(245, 158, 11, 0.15); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.25); }
.badge-danger  { background: rgba(239, 68, 68, 0.15);  color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.25); }
.badge-info    { background: rgba(59, 130, 246, 0.15); color: #93C5FD; border: 1px solid rgba(59, 130, 246, 0.25); }
```

### On Light Backgrounds (solid pills)
```css
.badge-success { background: #059669; color: white; }
.badge-warning { background: #D97706; color: white; }
.badge-danger  { background: #DC2626; color: white; }
```

---

## Component Libraries for Premium Effects

| Library | Install | Key Components for Dashboards |
|---------|---------|-------------------------------|
| **Magic UI** | Copy from magicui.design | Number Ticker, Animated List, Border Beam, Blur Fade, Dot Pattern |
| **Tremor** | `npm i @tremor/react` | Spark Charts, KPI Cards, Progress Circles, Bar Lists, Trackers |
| **shadcn/ui** | `npx shadcn@latest init` | Data Tables, Cards, Badges, Sheets, Command Palette |
