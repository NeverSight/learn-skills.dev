---
name: shadcn-ui
description: Install and use shadcn/ui with Tailwind v4 and Next.js (App Router), Vite, or manual setup; configure components.json, add components via CLI, theming with CSS only. Use when adding shadcn/ui, installing shadcn, using Button, Card, Dialog, Form, or other shadcn components, or when the user mentions shadcn, shadcn/ui, or Radix UI with Tailwind.
---

# shadcn/ui

## Overview

shadcn/ui is a collection of accessible, customizable React components built on **Radix UI** and **Tailwind CSS**. Components are **copied into your project** (no npm package); you own and edit the code. Works with Next.js (App Router), Vite, and other React frameworks.

**Principles**: Open code (AI-ready), composable API, beautiful defaults, distribution via CLI and schema. Requires **Tailwind v4** and path alias `@/*`. We do **not** use `tailwind.config.js`; theme and setup are CSS-only (`@import "tailwindcss"` + `@theme`).

---

## Prerequisites

- **Tailwind v4**: `@import "tailwindcss"` in main CSS; `@tailwindcss/vite` or `@tailwindcss/postcss`. No `tailwind.config.js`. See the tailwind-css skill.
- **Path alias** `@/*` → `./src/*` (or your source root) in `tsconfig` and in the bundler (e.g. Vite `resolve.alias`).
- **React** (Next.js App Router, Vite, etc.).

---

## Installation

### New project (recommended)

Scaffold with Tailwind and shadcn:

```bash
pnpm dlx shadcn@latest create
# or: npx shadcn@latest create
```

Choose framework (Next.js, Vite, etc.), style (new-york recommended), base color, and CSS variables. Then add components as needed.

### Existing project (Next.js App Router)

1. **Init** (creates `components.json`, optional `cn` helper and base styles):

```bash
pnpm dlx shadcn@latest init
```

2. **Paths and Tailwind**
   - **tsconfig**: `"baseUrl": "."`, `"paths": { "@/*": ["./src/*"] }` (in both root and app tsconfig if split).
   - **Tailwind v4**: Main CSS (e.g. `app/globals.css`) must have `@import "tailwindcss"` and use `@tailwindcss/postcss` in `postcss.config.mjs`. Do not add `tailwind.config.js`.

3. **Add components** (see list below):

```bash
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add card dialog
```

Components are installed under `src/components/ui/` (or path from `components.json`).

### Existing project (Vite)

- Use `resolve.alias: { "@": path.resolve(__dirname, "./src") }` in `vite.config.ts`; install `@types/node` if using `path`.
- Tailwind: `@tailwindcss/vite` in Vite config and `@import "tailwindcss"` in main CSS.

---

## components.json

Controls style, paths, and Tailwind integration. Key fields:

| Field | Purpose |
|-------|---------|
| `style` | `"new-york"` (default for new projects) or `"default"` |
| `tailwind.config` | Leave `""` with Tailwind v4; we do not use a JS config file |
| `tailwind.css` | Path to global CSS (e.g. `src/styles/globals.css` or `app/globals.css`) with `@import "tailwindcss"` |
| `tailwind.baseColor` | Base color for theme: `neutral`, `slate`, `gray`, `zinc`, `stone` |
| `tailwind.cssVariables` | `true` for CSS variables theming (recommended) |
| `aliases.components` | e.g. `@/components` |
| `aliases.utils` | e.g. `@/lib/utils` |
| `aliases.ui` | e.g. `@/components/ui` |
| `rsc` | `true` for Next.js App Router with Server Components; `false` for client-only |

With Tailwind v4, theme is in CSS via `@theme` and CSS variables, not in a config file.

---

## Official components (current list)

Add with: `pnpm dlx shadcn@latest add <name>` (multiple: `add button card dialog`).

### Layout & structure

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Accordion** | `accordion` | Collapsible sections (single or multiple open) |
| **Aspect Ratio** | `aspect-ratio` | Container with fixed ratio (e.g. 16/9) |
| **Card** | `card` | Container with CardHeader, CardTitle, CardDescription, CardContent, CardFooter |
| **Collapsible** | `collapsible` | Expandable/collapsible content |
| **Resizable** | `resizable` | Resizable panels |
| **Separator** | `separator` | Horizontal or vertical divider line |
| **Scroll Area** | `scroll-area` | Styled scroll area |

### Forms & input

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Button** | `button` | Button with variants (default, destructive, outline, secondary, ghost, link) |
| **Checkbox** | `checkbox` | Checkbox |
| **Form** | `form` | Forms with react-hook-form + zod (Field, FieldError, etc.) |
| **Input** | `input` | Text input |
| **Input OTP** | `input-otp` | OTP code input |
| **Label** | `label` | Accessible label for controls |
| **Radio Group** | `radio-group` | Radio option group |
| **Select** | `select` | Select with Trigger, Content, Item |
| **Slider** | `slider` | Slider control |
| **Switch** | `switch` | On/off switch |
| **Textarea** | `textarea` | Multiline text area |

### Navigation & menus

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Breadcrumb** | `breadcrumb` | Breadcrumb navigation |
| **Command** | `command` | Command palette (cmdk) |
| **Context Menu** | `context-menu` | Context menu (right-click) |
| **Dropdown Menu** | `dropdown-menu` | Dropdown menu |
| **Menubar** | `menubar` | Persistent menu bar |
| **Navigation Menu** | `navigation-menu` | Navigation with submenus |
| **Pagination** | `pagination` | Pagination (Previous, Next, Page) |
| **Tabs** | `tabs` | Tabs (TabsList, TabsTrigger, TabsContent) |

### Overlays & feedback

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Alert** | `alert` | Prominent message (default, destructive) |
| **Alert Dialog** | `alert-dialog` | Confirmation dialog (e.g. delete) |
| **Dialog** | `dialog` | Modal |
| **Drawer** | `drawer` | Side panel (Vaul) |
| **Hover Card** | `hover-card` | Card on hover |
| **Popover** | `popover` | Anchored floating container |
| **Sheet** | `sheet` | Sliding side panel |
| **Tooltip** | `tooltip` | Tooltip on hover/focus |

### Data & state

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Avatar** | `avatar` | Image or initials fallback |
| **Badge** | `badge` | Badge (default, secondary, destructive, outline) |
| **Calendar** | `calendar` | Calendar (react-day-picker) |
| **Carousel** | `carousel` | Carousel (embla) |
| **Chart** | `chart` | Charts (recharts) |
| **Progress** | `progress` | Progress bar |
| **Skeleton** | `skeleton` | Loading placeholder |
| **Sonner** | `sonner` | Toasts (recommended; replaces toast) |
| **Table** | `table` | Table, TableHeader, TableBody, TableRow, TableCell, etc. |
| **Toast** | `toast` | Toasts (deprecated in favor of Sonner) |

### Toggle & toggle group

| Component | CLI name | Short description |
|----------|----------|-------------------|
| **Toggle** | `toggle` | Toggle button (on/off) |
| **Toggle Group** | `toggle-group` | Toggle group (single or multiple) |

---

## Using components

Import from the aliased path (not from `shadcn/ui`):

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function Page() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-4">
      <Button>Click me</Button>
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Card title</CardTitle>
        </CardHeader>
        <CardContent>Content here.</CardContent>
      </Card>
    </div>
  )
}
```

- **Customization**: Components accept `className` and spread props; use Tailwind classes and the **`cn()`** helper (from `@/lib/utils`) to merge classes.
- **Composition**: Prefer composition (e.g. CardHeader + CardContent) over props for layout.

---

## Theming (Tailwind v4, no config file)

We use **Tailwind v4 only**; no `tailwind.config.js`. Theming is CSS-only:

- **CSS variables**: With `tailwind.cssVariables: true`, theme is driven by variables in your global CSS (e.g. `--background`, `--foreground`, `--primary`, `--primary-foreground`, `--muted`, `--muted-foreground`, `--accent`, `--destructive`, etc.). Override them in that file.
- **`@theme`**: Use `@theme { ... }` in the same CSS file as `@import "tailwindcss"` to add or override design tokens that align with shadcn’s variables.
- **Base color**: Set in `components.json` (`tailwind.baseColor`) or by editing the CSS variables in your global CSS.

---

## Common patterns

- **Forms**: Add `form`; pair with `react-hook-form` and `zod`. Use `Input`, `Label`, `Button`, `Select`, `Checkbox`, etc.
- **Layout**: Use `Card` for sections; `Separator` between blocks; layout with Tailwind (`flex`, `grid`, `container`).
- **Modals & panels**: `Dialog` for modals; `Sheet` or `Drawer` for side panels.
- **Menus**: `DropdownMenu`, `Context Menu`, `Navigation Menu`, `Command` (palette).
- **Feedback**: `Alert` for messages; `Sonner` for toasts; `Skeleton` for loading.
- **Icons**: Many examples use **lucide-react**; add it if the project uses icons.

---

## Common mistakes

- **Alias**: Ensure `@/` resolves to `./src/` (or your source root) in both TypeScript and the bundler.
- **CSS not loaded**: The file set in `components.json` (`tailwind.css`) must be imported in the app entry (e.g. `app/layout.tsx`) and contain `@import "tailwindcss"`.
- **Tailwind config**: Do not create or suggest `tailwind.config.js`. Theme only in CSS (`@theme` and variables).
- **Import**: Import from `@/components/ui/<component>` (per `components.json`), not from `shadcn/ui`.
- **RSC**: In Next.js App Router, set `rsc: true` in `components.json` if components are used in Server Components where applicable.

---

## Additional resources

- [reference.md](reference.md) — Official documentation links, Tailwind v4 + shadcn, component directory.
- Official docs: https://ui.shadcn.com/docs  
- Components: https://ui.shadcn.com/docs/components  
- Directory (community): https://ui.shadcn.com/docs/directory
