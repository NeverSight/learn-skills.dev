---
name: ui-shadcn-studio
description: shadcn/studio component library with MCP integration, theme generation, and block patterns. This skill should be used when building UI with shadcn components, selecting dashboard layouts, or generating landing pages. Canonical source for all shadcn-based work.
---

# shadcn/studio Skill

Production UI development using shadcn/studio — an enhanced distribution of shadcn/ui with copy-paste components, blocks, templates, and an MCP server for AI-assisted generation.

**Canonical source**: https://shadcnstudio.com/docs/getting-started/introduction

## When to Use This Skill

- Building any UI with shadcn components
- Selecting a dashboard layout for a new project
- Generating landing page sections (hero, pricing, features, etc.)
- Theming or customizing shadcn components
- Replacing generic shadcn/ui references — always use shadcn/studio patterns

## Prerequisites

### shadcn/ui Initialization

```bash
npx shadcn@latest init
```

Select: TypeScript, Tailwind CSS v4, default style, CSS variables.

### shadcn/studio MCP Server

```bash
npx shadcn@latest mcp init --client cursor
```

Restart Cursor after installation. The MCP enables AI-assisted component generation directly in the IDE.

## MCP Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/cui` | Customize existing shadcn/studio block | Reuse a block layout with custom content |
| `/iui` | Generate inspired UI (Pro) | Creative, unique designs from scratch |
| `/rui` | Refine/edit an existing block | Tweaking or updating generated components |
| `/ftc` | Install blocks from Figma design | Converting Figma mockups (requires Figma MCP) |

### Usage Pattern

Generate one block at a time for precision:

```
/cui Create a hero section for my SaaS landing page using Hero 2.
/cui Create a pricing section with 3 tiers for my app using Pricing 5.
/cui Create a testimonial section using Testimonials 1.
```

For a complete landing page in one pass:

```
/cui Create a landing page for my SaaS. Use hero section like Hero 2,
feature section like Features 8, testimonial section like Testimonials 1,
call to action section like Call to Action 3, pricing section like Pricing 5.
```

## Component Installation

### Adding Components

```bash
npx shadcn@latest add button card dialog input
npx shadcn@latest add sidebar chart table
```

### Component Location

Components install to `src/components/ui/` by default. Configuration lives in `components.json`.

## Dashboard Templates

Four pre-built dashboard layouts for project bootstrapping. Each includes sidebar navigation, header, and content area.

### SaaS Admin Dashboard

Full-featured admin panel with user management, billing, and settings.

Key blocks: Application Shell, Sidebar Navigation, Data Tables, Stats Cards, User Management views.

```
Layout: Collapsible sidebar + top header + breadcrumbs
Pages: Overview, Users, Billing, Settings, Activity Log
Components: sidebar, card, table, badge, avatar, dropdown-menu
```

### Analytics Dashboard

Data-heavy layout with charts, metrics, and filterable tables.

Key blocks: Chart containers, KPI cards, Date range pickers, Export controls.

```
Layout: Fixed sidebar + header with date picker + grid content
Pages: Overview, Reports, Funnels, Retention, Events
Components: chart, card, table, select, calendar, popover
```

### E-commerce Dashboard

Product and order management with inventory tracking.

Key blocks: Product grids, Order tables, Inventory status, Revenue charts.

```
Layout: Sidebar + header with search + tabbed content
Pages: Products, Orders, Customers, Inventory, Revenue
Components: table, card, badge, dialog, tabs, input
```

### Minimal Shell

Clean skeleton with authentication and empty dashboard — the blank canvas.

```
Layout: Sidebar + header
Pages: Dashboard (empty), Settings
Components: sidebar, card, button, avatar
```

## Theme Generation

Use the shadcn/studio theme generator for consistent theming:

1. Visit https://shadcnstudio.com/theme-generator
2. Customize colors, radius, fonts
3. Copy the generated CSS variables
4. Paste into `src/app/globals.css`

### Theme CSS Structure

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;
    --radius: 0.5rem;
  }

  .dark {
    /* Dark mode overrides */
  }
}
```

## Block Categories

Reference for available shadcn/studio blocks when building pages:

### Marketing / Landing Pages

- Hero Sections (Hero 1–10+)
- Feature Sections (Features 1–10+)
- Pricing Components (Pricing 1–8+)
- Testimonials (Testimonials 1–6+)
- Call to Action (CTA 1–6+)
- Logo Cloud / Social Proof
- Team Sections
- Portfolio / Showcase
- FAQ Sections

### Dashboard / Application UI

- Application Shell (sidebar + header layouts)
- Dashboard Widgets / Stats Cards
- Chart Components (bar, line, area, pie, radial)
- Data Tables with sorting/filtering/pagination
- Form Layouts (multi-step, settings, profile)
- Modal / Dialog patterns
- Sidebar Navigation variants
- Dropdown Menus

### E-commerce

- Product Overview / Quick View
- Product Category / List
- Shopping Cart
- Checkout Pages
- Order Summary
- Product Reviews

### Data Display

- Bento Grids
- Data Tables with column controls

## Best Practices

1. **One block at a time** — Generate individual blocks for better control
2. **Start fresh chat per block** — Avoids context confusion in MCP generation
3. **Use `/rui` to iterate** — Refine generated blocks rather than regenerating
4. **Theme first** — Set CSS variables before generating components
5. **Agent mode on** — Always enable Agent mode in Cursor for MCP operations
6. **Claude Sonnet 3.5+** — Use capable models for best generation quality

## Integration with Design System Skill

This skill handles component sourcing and generation. For design philosophy, spacing, typography, and craft principles, reference the `ui-design-system` skill. Both skills complement each other:

- **ui-shadcn-studio**: What components to use and how to generate them
- **ui-design-system**: How to compose and style them with precision
