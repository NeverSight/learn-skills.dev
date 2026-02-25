---
name: phase-3-mockup
description: |
  Phase 3: UI/UX Mockups and Wireframe Design.
  Create wireframes, screen flows, and user journey maps.
  Next: $phase-4-api.
  Triggers: mockup, wireframe, UI design, UX, screen design, prototype,
  목업, 와이어프레임, 화면 설계, UI 디자인, モックアップ, ワイヤーフレーム,
  原型设计, 线框图, maqueta, wireframe, maquette, Wireframe, Mockup
  Do NOT use for: coding conventions (use $phase-2-convention), components (use $phase-5-design-system).
---

# Phase 3: Mockup & UI/UX Design

> Design screens and user flows before building components.

## Purpose

Phase 3 creates visual blueprints for the application. Mockups prevent expensive redesigns during development and align stakeholders on the user experience.

## Actions

| Action | Description | Example |
|--------|-------------|---------|
| `start` | Begin Phase 3 | `$phase-3-mockup start` |
| `screens` | List all screens needed | `$phase-3-mockup screens` |
| `flow` | Create user flow diagram | `$phase-3-mockup flow` |

## Deliverables

1. **Screen Inventory** - List of all screens/pages
2. **Wireframes** - Low-fidelity layout for each screen
3. **User Flow Diagram** - Navigation paths between screens
4. **Responsive Breakpoints** - Mobile/tablet/desktop layouts
5. **Mockup Document** - `docs/02-design/mockup.md`

## Process

### Step 1: Screen Inventory

List every screen the application needs:

```markdown
### Public Pages
- [ ] Landing Page - Hero, features, CTA
- [ ] Login - Email/password form
- [ ] Register - Signup form
- [ ] Password Reset - Recovery flow

### Authenticated Pages
- [ ] Dashboard - Overview, stats, recent activity
- [ ] Profile - User info, settings
- [ ] Item List - CRUD list with filters
- [ ] Item Detail - Single item view/edit
```

### Step 2: Wireframe Each Screen

Use ASCII for text-based wireframes:

```
+-----------------------------------+
| [Logo]        [Nav]    [Login]    |
+-----------------------------------+
|                                   |
|     Welcome to AppName            |
|     Subtitle description          |
|                                   |
|     [Get Started Button]          |
|                                   |
+-----------------------------------+
|  Feature 1  | Feature 2  | F3    |
|  Icon+Text  | Icon+Text  |       |
+-----------------------------------+
|         Footer Links              |
+-----------------------------------+
```

### Step 3: User Flow

```
Landing -> Login -> Dashboard
                 -> Register -> Email Verify -> Dashboard

Dashboard -> Item List -> Item Detail -> Edit Item
          -> Profile -> Settings
          -> Logout -> Landing
```

### Step 4: Responsive Design

| Breakpoint | Width | Layout Changes |
|-----------|-------|----------------|
| Mobile | < 640px | Single column, hamburger menu |
| Tablet | 640-1024px | Two columns, condensed nav |
| Desktop | > 1024px | Full layout, sidebar visible |

### Step 5: Component Identification

Identify reusable components from wireframes:
- Header (logo, nav, user menu)
- Footer (links, copyright)
- Card (image, title, description, actions)
- Form (input, select, checkbox, submit)
- Table (sortable, filterable, paginated)
- Modal (confirm, form, info)
- Toast/Alert (success, error, warning, info)

## Mockup Patterns

See `references/mockup-patterns.md` for common layout, form, and list patterns.

## Output Location

```
docs/02-design/
├── mockup.md         # Screen wireframes
├── user-flow.md      # Navigation flow diagram
└── screen-list.md    # Screen inventory
```

## Next Phase

When mockups are complete, proceed to **$phase-4-api** for API design.

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| Skipping mobile layout | Design mobile-first, then scale up |
| Too detailed too early | Start with low-fi wireframes |
| Missing error states | Design empty, loading, and error states |
| No user flow | Map the full journey before screen details |
| Forgetting edge cases | Include 0 items, max items, long text states |
