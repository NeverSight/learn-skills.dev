---
name: equinor-design-system
description: 'Authoritative, machine-readable EDS design rules for color tokens, typography, spacing, elevation, icons, and page layout zones. USE FOR: looking up correct EDS CSS custom properties, typography variant names, spacing tokens, shadow/elevation tokens, icon usage rules, and Fusion Portal page layout conventions. This is a lookup reference consumed by other skills and agents — it has no standalone workflow. DO NOT USE FOR: React component props or usage examples (use fusion-research + mcp_fusion_search_eds), general Copilot coding tasks, or Fusion Framework API questions.'
license: MIT
metadata:
  version: "0.1.0"
  status: experimental
  owner: "@equinor/fusion-core"
  role: subordinate
  tags:
    - eds
    - design-system
    - design-tokens
    - color
    - typography
    - spacing
    - elevation
    - icons
    - layout
    - equinor-brand
    - system-skill
---

# Equinor Design System — Design Rules

Compact reference for EDS design tokens and Equinor brand constraints. All rules are sourced from [eds.equinor.com](https://eds.equinor.com) and the [Equinor Communication Toolbox](https://communicationtoolbox.equinor.com).

This file is a **subordinate lookup reference**. There are no workflow steps. Consuming agents should look up the relevant section and apply the rule directly.

---

## Color tokens

Use **EDS CSS custom properties** (`--eds-color-*`) for all color values. Never use raw hex, rgb(), or named CSS colors in Fusion app code. All tokens below are from `@equinor/eds-tokens` v2.x (the version Fusion apps depend on).

> Token naming pattern: `--eds-color-<layer>-<semantic>-<variant>`
> - `bg` = background fill
> - `text` = foreground text / icon
> - `border` = stroke / divider

### Background tokens

| Purpose | EDS token |
|---|---|
| Page / app canvas | `--eds-color-bg-canvas` |
| Surface (card, panel) | `--eds-color-bg-surface` |
| Input field background | `--eds-color-bg-input` |
| Floating surface (dropdown, tooltip) | `--eds-color-bg-floating` |
| Backdrop / modal scrim | `--eds-color-bg-backdrop` |
| Primary action fill (default) | `--eds-color-bg-fill-emphasis-default` |
| Primary action fill (hover) | `--eds-color-bg-fill-emphasis-hover` |
| Primary action fill (active) | `--eds-color-bg-fill-emphasis-active` |
| Muted fill (default) | `--eds-color-bg-fill-muted-default` |
| Muted fill (hover) | `--eds-color-bg-fill-muted-hover` |
| Disabled surface | `--eds-color-bg-disabled` |
| Success surface (subtle bg) | `--eds-color-bg-success-surface` |
| Success fill (emphasis) | `--eds-color-bg-success-fill-emphasis-default` |
| Warning surface | `--eds-color-bg-warning-surface` |
| Warning fill (emphasis) | `--eds-color-bg-warning-fill-emphasis-default` |
| Danger / error surface | `--eds-color-bg-danger-surface` |
| Danger fill (emphasis) | `--eds-color-bg-danger-fill-emphasis-default` |
| Info surface | `--eds-color-bg-info-surface` |
| Info fill (emphasis) | `--eds-color-bg-info-fill-emphasis-default` |
| Accent surface | `--eds-color-bg-accent-surface` |
| Accent fill (emphasis) | `--eds-color-bg-accent-fill-emphasis-default` |

### Text tokens

| Purpose | EDS token |
|---|---|
| Primary body text | `--eds-color-text-strong` |
| Text on emphasis/filled backgrounds | `--eds-color-text-strong-on-emphasis` |
| Subtle / secondary text | `--eds-color-text-subtle` |
| Disabled text | `--eds-color-text-disabled` |
| Link | `--eds-color-text-link` |
| Success text | `--eds-color-text-success-strong` |
| Success text (subtle) | `--eds-color-text-success-subtle` |
| Warning text | `--eds-color-text-warning-strong` |
| Danger / error text | `--eds-color-text-danger-strong` |
| Info text | `--eds-color-text-info-strong` |
| Accent text | `--eds-color-text-accent-strong` |

### Border tokens

| Purpose | EDS token |
|---|---|
| Default divider / border | `--eds-color-border-medium` |
| Subtle border | `--eds-color-border-subtle` |
| Strong border | `--eds-color-border-strong` |
| Focus ring | `--eds-color-border-focus` |
| Disabled border | `--eds-color-border-disabled` |
| Success border | `--eds-color-border-success-medium` |
| Warning border | `--eds-color-border-warning-medium` |
| Danger border | `--eds-color-border-danger-medium` |
| Info border | `--eds-color-border-info-medium` |
| Accent border | `--eds-color-border-accent-medium` |

> **Brand constraint**: Equinor red (`#FF1243`) is used in the primary logo only — never as a UI action or semantic color. Use EDS color tokens for all clickable and semantic surfaces.

### Token access in code

Prefer EDS CSS custom properties in styled-components over the `@equinor/eds-tokens` JS object when possible — they respect system dark/light mode automatically.

```typescript
import styled from 'styled-components';

const Card = styled.div`
  background: var(--eds-color-bg-surface);
  border: 1px solid var(--eds-color-border-medium);
  color: var(--eds-color-text-strong);
`;

const PrimaryButton = styled.button`
  background: var(--eds-color-bg-fill-emphasis-default);
  color: var(--eds-color-text-strong-on-emphasis);

  &:hover {
    background: var(--eds-color-bg-fill-emphasis-hover);
  }

  &:disabled {
    background: var(--eds-color-bg-disabled);
    color: var(--eds-color-text-disabled);
  }
`;
```

---

## Typography

Use `Typography` from `@equinor/eds-core-react` for all text rendering. Never set raw `font-size`, `font-family`, or `line-height` manually — use the EDS `variant` prop.

### Variant hierarchy

| Level | `variant` | Usage |
|---|---|---|
| Display | `h1` | Hero headings (rarely used in apps) |
| Page title | `h2` | Top-level page heading |
| Section heading | `h3` | Section title, card header |
| Sub-heading | `h4` | Sub-section, panel title |
| Overline | `overline` | Category labels, breadcrumb-level text |
| Body | `body_long` | Multi-line body text |
| Body short | `body_short` | Single-line body, table cells |
| Caption | `caption` | Metadata, timestamps, helper text |
| Label | `label` | Form field labels |

```typescript
import { Typography } from '@equinor/eds-core-react';

// Correct
<Typography variant="h3">Section heading</Typography>
<Typography variant="body_short">Table cell value</Typography>
<Typography variant="caption">Last updated 2 hours ago</Typography>

// Wrong — never do this
<p style={{ fontSize: '14px' }}>…</p>
```

### Brand constraint

Equinor brand typeface is **Equinor** (used in marketing). Fusion apps must use the EDS system typeface defined by `@equinor/eds-core-react` — do not import or override the Equinor brand font in app CSS.

---

## Spacing tokens

Use `--eds-spacing-horizontal-<size>` and `--eds-spacing-vertical-<size>` from `@equinor/eds-tokens` v2 for margin, padding, and gap. Do not use arbitrary pixel values.

The horizontal and vertical scales share the same size steps but may differ by a few pixels at each step; use the axis-appropriate token (horizontal for left/right, vertical for top/bottom).

| Size | Horizontal value | Vertical value | Use for |
|---|---|---|---|
| `4xs` | 2 px | 2 px | Micro gap, tight icon padding |
| `3xs` | 4 px | 4 px | XS gap |
| `2xs` | 6 px | 6 px | Small inset padding |
| `xs` | 8 px | 8 px | SM gap, compact list spacing |
| `sm` | 12 px | 12 px | Inner padding (chips, badges) |
| `md` | 16 px | 16 px | Standard content padding |
| `lg` | 20 px | 20 px | LG gap, section spacing |
| `xl` | 24 px | 24 px | XL gap, card separation |
| `2xl` | 28 px | 28 px | Major section break |
| `3xl` | 32 px | 32 px | Section-level whitespace |

```typescript
const Section = styled.section`
  padding-inline: var(--eds-spacing-horizontal-md);
  padding-block: var(--eds-spacing-vertical-lg);
  gap: var(--eds-spacing-vertical-sm);
`;
```

### Border radius

| Token / value | Use for |
|---|---|
| `--eds-shape-corners-border-radius` | Standard rounded corners (cards, buttons) |
| `border-radius: 0` | Sharp / square corners |
| `border-radius: 9999px` | Full pill (tags, chips) |

---

## Elevation and shadow

EDS v2 (`@equinor/eds-tokens` ^2) does not expose elevation as CSS custom properties. For elevated surfaces use the EDS `Paper` component which applies the correct shadow for its variant, or use EDS `Elevation` tokens via the JS object import from `@equinor/eds-tokens` when you need raw values in styled-components.

```typescript
import { Paper } from '@equinor/eds-core-react';

// Prefer Paper for cards/panels — elevation is handled automatically
<Paper elevation="raised">
  <CardContent />
</Paper>
```

If you need raw `box-shadow` values from JS (rare): import from `@equinor/eds-tokens`, not hardcoded values.

---

## Icon usage

Use `@equinor/eds-icons` with the EDS `Icon` component. Do not import SVGs directly or use third-party icon sets. Always pass icon data via the `data` prop — do not use the `name` string prop. Icon names from `@equinor/eds-icons` are in `snake_case`.

```typescript
import { Icon } from '@equinor/eds-core-react';
import { add, close, settings } from '@equinor/eds-icons';

// Pass icon data object via the `data` prop; provide `title` for accessibility
<Icon data={add} title="Add" />
<Icon data={close} title="Close" size={16} />
<Icon data={settings} title="Settings" />
```

Icon sizes follow a fixed scale: `16`, `24` (default), `32`, `40`, `48`. Do not set arbitrary sizes.

---

## Page layout zones

Fusion Portal apps run inside the Fusion Portal shell, which owns the top navigation, left rail, and outer margins. Apps must **not** replicate or conflict with these zones.

### Three-zone app shell

| Zone | Component | Notes |
|---|---|---|
| Top bar / header | Provided by Fusion Portal shell | Apps do not render a global header |
| Main content area | `<main>` or top-level app `<div>` | Full available width and height |
| Side panel / detail | `@equinor/fusion-react-side-sheet` | Slides in from the right; do not use custom positioned overlays |

### Layout constraints

- **Do not** add outer `margin` or `padding` to the root app component — the portal shell provides the content inset.
- Use `--eds-spacing-horizontal-<size>` / `--eds-spacing-vertical-<size>` tokens for internal section spacing.
- **Do not** use fixed `height` on the root container — allow content to stretch to the available viewport height.
- **Do not** create custom scrollable containers that wrap the full page — the browser scroll is the standard scroll surface.
- Nested scrollable regions are acceptable for fixed-height grid/table areas, but must be deliberate and clearly bounded.

### Empty and loading states

| State | Pattern |
|---|---|
| Loading | EDS `CircularProgress` or `@equinor/fusion-react-progress-indicator` `ProgressIndicator` centered in content area |
| Empty (no data) | EDS `Typography` + optional EDS `Button` for a primary action; centered or top-aligned |
| Error | EDS `Typography variant="body_short"` colored with `--eds-color-text-danger-strong` + retry action |

---

## Sources

- EDS design resources: https://eds.equinor.com/docs/resources/
- EDS component library: https://eds.equinor.com/components/
- Equinor brand color: https://communicationtoolbox.equinor.com/point/en/equinor/component/default/100056
- Equinor brand typography: https://communicationtoolbox.equinor.com/point/en/equinor/component/default/100059
- Equinor brand layout: https://communicationtoolbox.equinor.com/point/en/equinor/component/default/100061
