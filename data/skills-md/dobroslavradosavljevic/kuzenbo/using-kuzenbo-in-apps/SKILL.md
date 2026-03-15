---
name: using-kuzenbo-in-apps
description: Use this skill whenever the AI is implementing, configuring, documenting, or troubleshooting Kuzenbo usage in an application, including installation, Tailwind CSS v4 setup, CSS variable theming, dark mode, Base UI providers, and component integration patterns.
---

# Using Kuzenbo in Apps

## Purpose

Use this skill to integrate Kuzenbo correctly in consumer applications,
with reliable setup, correct Tailwind v4 wiring, robust theming, and
component usage that matches the library's intended patterns.

## Apply This Skill Automatically

Apply this skill whenever work involves any of the following:

- Installing or upgrading `kuzenbo`
- Setting up Tailwind CSS v4 for Kuzenbo styles
- Rendering or composing Kuzenbo components in an app
- Customizing colors, radii, or light/dark theme behavior
- Debugging unstyled components or missing classes
- Documenting how to use Kuzenbo in product codebases

## Source of Truth Inside This Repository

When details conflict, use these files in order:

1. `src/index.tsx` (public exports)
2. `src/styles.css` (theme tokens and dark-mode contract)
3. `README.md` (consumer usage and setup instructions)
4. `package.json` (peer dependencies)

## Quick Integration Workflow

1. Install `kuzenbo` and needed peer dependencies.
2. Add required global CSS imports and `@source` scan path.
3. Render a smoke-test component (`Button`, `Card`, or `Input`).
4. Add a minimal theme override (`--primary`, `--radius`).
5. Verify both light and dark mode.
6. Add optional providers (`CSPProvider`, `DirectionProvider`) when needed.
7. Resolve any missing peers only for components that are actually used.

## Requirements

- React 18+ or 19+
- Node.js 22+
- Tailwind CSS v4

## Installation

```bash
npm install kuzenbo
# or
pnpm add kuzenbo
# or
yarn add kuzenbo
# or
bun add kuzenbo
```

## Peer Dependency Map

Install only what your chosen components require.

| Kuzenbo Feature/Component | Peer Dependency                          |
| ------------------------- | ---------------------------------------- |
| `Calendar`                | `react-day-picker`                       |
| `Carousel`                | `embla-carousel`, `embla-carousel-react` |
| `Chart`                   | `recharts`                               |
| `Command`                 | `cmdk`                                   |
| `CountryFlag`             | `country-flag-icons`                     |
| `Drawer`                  | `vaul`                                   |
| `Dropzone`                | `react-dropzone`                         |
| `EmojiPicker`             | `frimousse`                              |
| `InputOTP`                | `input-otp`                              |
| `Marquee`                 | `react-fast-marquee`                     |
| `QRCode`                  | `qrcode`, `culori`                       |
| `Resizable*`              | `react-resizable-panels`                 |
| `Textarea`                | `react-textarea-autosize`                |
| `VideoPlayer`             | `media-chrome`                           |

If an app reports runtime/module errors, verify this table first.

## Required Tailwind v4 Setup

Add this to your main global CSS file:

```css
@import "tailwindcss";
@import "kuzenbo/styles.css";
@source "../node_modules/kuzenbo/dist";
```

`@source` must be relative to the CSS file location, not project root.

Common path patterns:

- `src/app.css` -> `../node_modules/kuzenbo/dist`
- `app/globals.css` -> `../node_modules/kuzenbo/dist`
- `styles/index.css` -> `../../node_modules/kuzenbo/dist`

With pnpm, prefer the explicit `.../kuzenbo/dist` path.

## Framework Wiring Patterns

### Next.js App Router

- Put imports in `app/globals.css`
- Ensure `globals.css` is imported from `app/layout.tsx`

### Vite / SPA

- Put imports in `src/index.css` or `src/app.css`
- Ensure the CSS file is imported once in `src/main.tsx`

## Usage Patterns

### Simple Component

```tsx
import { Button } from "kuzenbo";

export function Example() {
  return <Button variant="default">Click me</Button>;
}
```

### Compound Component Pattern

```tsx
import { Dialog } from "kuzenbo";

export function ExampleDialog() {
  return (
    <Dialog>
      <Dialog.Trigger>Open</Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay />
        <Dialog.Content>
          <Dialog.Header>
            <Dialog.Title>Title</Dialog.Title>
            <Dialog.Description>Description</Dialog.Description>
          </Dialog.Header>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog>
  );
}
```

### Generic Components (Type-Safe Values)

`Select`, `Combobox`, and `Autocomplete` are generic-first APIs.
Keep options/value types explicit in app code when possible.

```tsx
import { Select } from "kuzenbo";

type Fruit = "apple" | "orange" | "banana";

export function FruitSelect() {
  return (
    <Select<Fruit> defaultValue="apple">
      <Select.Trigger>
        <Select.Value placeholder="Pick a fruit" />
      </Select.Trigger>
      <Select.Content>
        <Select.Item value="apple">Apple</Select.Item>
        <Select.Item value="orange">Orange</Select.Item>
        <Select.Item value="banana">Banana</Select.Item>
      </Select.Content>
    </Select>
  );
}
```

## Optional Providers and Utilities

Use these only when needed:

- `CSPProvider` for strict CSP nonces
- `DirectionProvider` for RTL/LTR context
- `mergeProps` for prop merging behavior
- `useRender` for render-prop based composition

```tsx
import { CSPProvider, DirectionProvider } from "kuzenbo";

export function AppProviders({
  children,
  nonce,
}: {
  children: React.ReactNode;
  nonce?: string;
}) {
  return (
    <CSPProvider nonce={nonce}>
      <DirectionProvider direction="ltr">{children}</DirectionProvider>
    </CSPProvider>
  );
}
```

## Theming In Depth

### Theme Architecture

Kuzenbo theming is based on semantic CSS variables in `src/styles.css`:

1. `:root` defines light-theme semantic tokens (`--primary`, `--background`, ...)
2. `.dark` defines dark-theme semantic tokens for the same keys
3. `@theme inline` maps these tokens into Tailwind-consumable variables
4. Components consume semantic utility classes (`bg-background`,
   `text-foreground`, `border-border`, etc.)

### Dark-Mode Contract

Dark utilities are class-based through:

```css
@custom-variant dark (&:is(.dark *));
```

This means a `.dark` ancestor must exist for dark styles to apply.

### Token Groups and Meanings

#### Core Surface/Text Tokens

- `--background`: app/page background
- `--foreground`: default text color
- `--card`, `--card-foreground`: card surfaces/text
- `--popover`, `--popover-foreground`: popovers, menus, floating surfaces

#### Brand/Action Tokens

- `--primary`, `--primary-foreground`: primary CTA surface/text
- `--secondary`, `--secondary-foreground`: secondary surfaces/text
- `--accent`, `--accent-foreground`: highlighted interactive states
- `--muted`, `--muted-foreground`: subtle containers and helper text

#### Border/Input/Focus Tokens

- `--border`: default border color
- `--input`: input border/background token
- `--ring`: focus ring color
- `--radius`: base radius value

#### Status Tokens

- `--success`, `--success-foreground`, `--success-border`
- `--warning`, `--warning-foreground`, `--warning-border`
- `--danger`, `--danger-foreground`, `--danger-border`
- `--info`, `--info-foreground`, `--info-border`

#### Data Display Tokens

- `--chart-1` ... `--chart-5`: chart palette
- `--surface-1` ... `--surface-4`: neutral elevation steps
- `--sidebar`, `--sidebar-foreground`, `--sidebar-primary`,
  `--sidebar-primary-foreground`, `--sidebar-accent`,
  `--sidebar-accent-foreground`, `--sidebar-border`, `--sidebar-ring`

### Complete Semantic Token List (Exact Keys)

Use these exact keys for overrides:

- `--radius`
- `--background`
- `--foreground`
- `--card`
- `--card-foreground`
- `--popover`
- `--popover-foreground`
- `--primary`
- `--primary-foreground`
- `--secondary`
- `--secondary-foreground`
- `--muted`
- `--muted-foreground`
- `--accent`
- `--accent-foreground`
- `--border`
- `--input`
- `--ring`
- `--chart-1`
- `--chart-2`
- `--chart-3`
- `--chart-4`
- `--chart-5`
- `--sidebar`
- `--sidebar-foreground`
- `--sidebar-primary`
- `--sidebar-primary-foreground`
- `--sidebar-accent`
- `--sidebar-accent-foreground`
- `--sidebar-border`
- `--sidebar-ring`
- `--danger`
- `--danger-foreground`
- `--danger-border`
- `--warning`
- `--warning-foreground`
- `--warning-border`
- `--info`
- `--info-foreground`
- `--info-border`
- `--success`
- `--success-foreground`
- `--success-border`
- `--surface-1`
- `--surface-2`
- `--surface-3`
- `--surface-4`

### Radius Scale Behavior

Kuzenbo derives additional radius tokens from `--radius`:

- `--radius-sm: calc(var(--radius) - 4px)`
- `--radius-md: calc(var(--radius) - 2px)`
- `--radius-lg: var(--radius)`
- `--radius-xl: calc(var(--radius) + 4px)`
- `--radius-2xl: calc(var(--radius) + 8px)`
- `--radius-3xl: calc(var(--radius) + 12px)`
- `--radius-4xl: calc(var(--radius) + 16px)`

Changing `--radius` updates the whole corner scale.

### Recommended Retheme Process

1. Start by overriding core tokens only:
   `--background`, `--foreground`, `--primary`, `--primary-foreground`,
   `--border`, `--ring`, `--radius`.
2. Add status tokens next (`--success`, `--warning`, `--danger`, `--info`).
3. Add chart/sidebar/surface tokens if your app uses those components.
4. Mirror overrides in both `:root` and `.dark`.
5. Validate contrast for text-on-surface and CTA states.

### Full-Stack Theme Override Example

```css
@import "tailwindcss";
@import "kuzenbo/styles.css";
@source "../node_modules/kuzenbo/dist";

:root {
  --radius: 0.5rem;

  --background: oklch(0.99 0.004 248);
  --foreground: oklch(0.2 0.02 260);

  --primary: oklch(0.62 0.22 258);
  --primary-foreground: oklch(0.98 0.002 260);

  --secondary: oklch(0.93 0.02 258);
  --secondary-foreground: oklch(0.28 0.03 258);

  --muted: oklch(0.96 0.01 255);
  --muted-foreground: oklch(0.53 0.03 260);

  --accent: oklch(0.92 0.03 240);
  --accent-foreground: oklch(0.26 0.04 250);

  --border: oklch(0.9 0.01 258);
  --input: oklch(0.9 0.01 258);
  --ring: oklch(0.7 0.1 258);

  --success: oklch(0.96 0.07 156);
  --success-foreground: oklch(0.38 0.13 156);
  --success-border: oklch(0.9 0.09 156);

  --warning: oklch(0.98 0.07 92);
  --warning-foreground: oklch(0.44 0.12 88);
  --warning-border: oklch(0.93 0.09 90);

  --danger: oklch(0.97 0.05 18);
  --danger-foreground: oklch(0.45 0.18 24);
  --danger-border: oklch(0.92 0.07 20);

  --info: oklch(0.97 0.03 245);
  --info-foreground: oklch(0.46 0.15 250);
  --info-border: oklch(0.92 0.05 250);

  --surface-1: oklch(0.98 0.002 250);
  --surface-2: oklch(0.95 0.003 250);
  --surface-3: oklch(0.92 0.004 250);
  --surface-4: oklch(0.88 0.006 250);
}

.dark {
  --background: oklch(0.16 0.015 260);
  --foreground: oklch(0.96 0.003 260);

  --primary: oklch(0.88 0.08 258);
  --primary-foreground: oklch(0.22 0.02 260);

  --secondary: oklch(0.29 0.02 260);
  --secondary-foreground: oklch(0.95 0.004 260);

  --muted: oklch(0.27 0.015 260);
  --muted-foreground: oklch(0.74 0.02 260);

  --accent: oklch(0.31 0.03 248);
  --accent-foreground: oklch(0.95 0.005 260);

  --border: oklch(1 0 0 / 12%);
  --input: oklch(1 0 0 / 16%);
  --ring: oklch(0.62 0.06 258);

  --surface-1: oklch(0.18 0.01 260);
  --surface-2: oklch(0.22 0.01 260);
  --surface-3: oklch(0.26 0.012 260);
  --surface-4: oklch(0.3 0.014 260);
}
```

### Scoped Theme Pattern

For multi-brand or themed sections, scope overrides to a container class.

```css
.theme-ocean {
  --primary: oklch(0.62 0.18 235);
  --primary-foreground: oklch(0.98 0 0);
}

.dark .theme-ocean {
  --primary: oklch(0.84 0.1 235);
  --primary-foreground: oklch(0.2 0.01 250);
}
```

### Theming Pitfalls to Avoid

- Do not edit `node_modules/kuzenbo/styles.css`; override tokens in app CSS.
- Do not forget `.dark` equivalents for custom light-theme tokens.
- Do not skip `@source` or Tailwind may purge needed classes.
- Prefer overriding semantic tokens (`--primary`) over hardcoded utility color
  overrides in every component.

## Complete Component Catalog

Public top-level components and utilities exported by Kuzenbo:

### Layout

- `Accordion`
- `AspectRatio`
- `Card`
- `Collapsible`
- `Empty`
- `ResizablePanelGroup` / `ResizablePanel` / `ResizableHandle`
- `ScrollArea`
- `Separator`
- `Spacer`

### Forms

- `Autocomplete`
- `Checkbox`
- `CheckboxGroup`
- `Combobox`
- `Dropzone`
- `FormField`
- `Input`
- `InputGroup`
- `InputOTP`
- `Label`
- `NumberField`
- `RadioGroup`
- `Select`
- `Slider`
- `Switch`
- `Textarea`

### Navigation

- `Breadcrumb`
- `Menubar`
- `NavigationMenu`
- `Pagination`
- `Sidebar`
- `Tabs`
- `Toolbar`

### Feedback

- `Alert`
- `AlertDialog`
- `Announcement`
- `Meter`
- `Progress`
- `Rating`
- `Skeleton`
- `Spinner`
- `Toast`
- `Tooltip`

### Overlay

- `ContextMenu`
- `Dialog`
- `Drawer`
- `DropdownMenu`
- `HoverCard`
- `Popover`
- `Sheet`

### Data Display

- `Avatar`
- `Badge`
- `Calendar`
- `Carousel`
- `ChartContainer` (plus chart helpers)
- `CountryFlag`
- `EmojiPicker`
- `GoogleLogo`
- `Item`
- `Kbd`
- `Marquee`
- `Pill`
- `QRCode`
- `Table`
- `ThemeIcon`
- `Timeline`
- `VideoPlayer`

### Actions

- `Affix`
- `Button`
- `ButtonGroup`
- `Command`
- `Toggle`
- `ToggleGroup`

### Utilities and Providers

- `Portal`
- `CSPProvider`
- `DirectionProvider`
- `mergeProps`
- `useRender`

### Exported Hooks and Helper APIs

- `useFilter`
- `useCarousel`
- `useChart`
- `useComboboxAnchor`
- `useDropzoneContext`
- `useNumberField`
- `useSidebar`
- `useToast`
- `useToastManager`
- `createToastManager`
- `useIsomorphicEffect`
- `useIsMobile`

## Troubleshooting

### Components Render Unstyled

- Verify `@import "kuzenbo/styles.css"` exists in global CSS.
- Verify `@source` path is correct relative to that CSS file.
- Restart dev server after changing Tailwind `@source` directives.

### Theme Overrides Not Applying

- Ensure overrides are declared after `@import "kuzenbo/styles.css"`.
- Ensure dark overrides are under `.dark` and that `.dark` is present on an
  ancestor element.

### Missing Module Errors

- Install missing peers based on the component-to-peer map.

### Type Errors With Generic Components

- Add explicit generic type parameters (`Select<Value>`, `Combobox<Value>`)
  when value inference is ambiguous.

## Definition of Done

An implementation is complete when:

1. Required CSS setup is present (`tailwindcss`, `kuzenbo/styles.css`,
   correct `@source`).
2. At least one Kuzenbo component is rendered with expected styling.
3. Theme overrides work in both light and dark modes.
4. Required peer dependencies for used components are installed.
5. Consumers can import and use target components without runtime errors.
