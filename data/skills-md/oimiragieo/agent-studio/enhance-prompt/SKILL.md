---
name: enhance-prompt
version: 1.1.0
description: Transforms vague UI/feature requests into structured, optimized prompts with design system awareness. Use when generating prompts for UI implementation, feature specification, or design-to-code translation. Triggers on tasks requiring prompt refinement, UI specification, or design system integration.
license: MIT
category: Frameworks
tags:
  - prompt-engineering
  - ui-specification
  - design-system
  - frontend
  - react
agents:
  - planner
  - frontend-pro
  - architect
  - developer
tools:
  - Read
  - Write
invoked_by: "Skill({ skill: 'enhance-prompt' })"
user_invocable: true
metadata:
  author: google-labs-code
  source: google-labs-code/stitch-skills
verified: false
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Enhance Prompt

Transform vague UI and feature requests into structured, optimized prompts with design system awareness. Based on the Google Labs Stitch Skills prompt enhancement pipeline.

## When to Apply

Use this skill when:

- A user request describes a UI feature vaguely ("make a nice login page")
- You need to generate implementation prompts from loose requirements
- Translating design mockups or wireframes into actionable specs
- Integrating design system tokens into component specifications
- Scaffolding page layouts from high-level descriptions

## 4-Step Enhancement Pipeline

### Step 1: Assess Intent

Analyze the raw request to identify:

- **Core objective**: What is the user trying to build?
- **Implicit requirements**: What is assumed but not stated?
- **Target audience**: Who will use this UI?
- **Interaction patterns**: What user flows are implied?

**Example:**

```
Raw: "Add a settings page"
Assessment:
  - Core: User preferences management interface
  - Implicit: Navigation integration, form validation, save/cancel actions
  - Audience: Authenticated users
  - Interactions: View current settings, modify, save, receive confirmation
```

### Step 2: Check DESIGN.md

Look for a `DESIGN.md` or equivalent design system file in the project root or docs directory. Extract:

- **Color tokens**: Primary, secondary, accent, semantic colors
- **Typography scale**: Font families, sizes, weights, line heights
- **Spacing system**: Base unit, scale (4px, 8px, 12px, 16px, etc.)
- **Component inventory**: Available pre-built components
- **Layout patterns**: Grid system, breakpoints, container widths

If no design system file exists, generate reasonable defaults based on the project's existing patterns (check `tailwind.config.*`, `theme.*`, or CSS custom properties).

**Lookup order:**

1. `DESIGN.md` in project root
2. `docs/design-system.md`
3. `tailwind.config.ts` / `tailwind.config.js` theme section
4. CSS custom properties in global styles
5. shadcn/ui theme configuration (if present)

### Step 3: Apply Enhancements

Transform the raw request by applying these enhancement layers:

#### 3a. Add Specificity

Replace vague terms with specific component names and patterns:

| Vague Term      | Specific Replacement                                                      |
| --------------- | ------------------------------------------------------------------------- |
| "nice"          | Clean layout with consistent spacing, proper visual hierarchy             |
| "modern"        | Card-based layout, rounded corners, subtle shadows, micro-interactions    |
| "responsive"    | Mobile-first grid (1-col mobile, 2-col tablet, 3-col desktop)             |
| "fast"          | Skeleton loading states, optimistic updates, prefetched data              |
| "user-friendly" | Clear labels, inline validation, helpful error messages, focus management |
| "beautiful"     | Design-system-compliant colors, balanced whitespace, typography scale     |
| "simple"        | Single-column layout, minimal navigation, progressive disclosure          |
| "interactive"   | Hover states, transitions, keyboard navigation, ARIA attributes           |

#### 3b. Inject Design Tokens

Insert design system values into the specification:

```
Enhanced: "Use the primary color (--color-primary / colors.primary.500)
for the submit button. Apply spacing-4 (16px) between form fields.
Use the heading-2 typography preset for section titles."
```

#### 3c. Scaffold Layout Structure

Generate a structural layout for the page/component:

```
Page Layout:
  Header: Breadcrumb navigation + page title
  Body:
    Sidebar (desktop only): Section navigation
    Main Content:
      Section 1: [Primary feature area]
      Section 2: [Secondary feature area]
      Section 3: [Related actions]
  Footer: Save/Cancel actions (sticky on mobile)
```

#### 3d. Add Interaction Specifications

Specify loading states, error states, empty states, and transitions:

- **Loading**: Skeleton placeholder matching final layout
- **Error**: Inline error messages with retry action
- **Empty**: Helpful illustration + primary action CTA
- **Success**: Toast notification + state update
- **Transitions**: 200ms ease-in-out for element appearance

### Step 4: Format Output

Produce the enhanced prompt in this structured format:

```markdown
## Enhanced Specification: [Feature Name]

### Objective

[1-2 sentences describing the precise goal]

### Design System Integration

- Colors: [specific tokens]
- Typography: [specific presets]
- Spacing: [specific scale values]
- Components: [reusable components to use]

### Layout Structure

[ASCII or markdown layout diagram]

### Component Breakdown

1. [Component name] - [purpose] - [key props/state]
2. [Component name] - [purpose] - [key props/state]

### Interaction States

- Loading: [description]
- Error: [description]
- Empty: [description]
- Success: [description]

### Accessibility Requirements

- Keyboard navigation: [specifics]
- Screen reader: [ARIA labels/roles]
- Focus management: [focus trap/restore behavior]

### Responsive Behavior

- Mobile (< 640px): [layout]
- Tablet (640-1024px): [layout]
- Desktop (> 1024px): [layout]
```

## Complete Example

**Raw Request:** "Build a dashboard for our analytics"

**Enhanced Output:**

```markdown
## Enhanced Specification: Analytics Dashboard

### Objective

Build a data visualization dashboard displaying key business metrics
with real-time updates, date range filtering, and exportable reports.

### Design System Integration

- Colors: --color-primary for active states, --color-success/warning/danger
  for metric status indicators
- Typography: heading-1 for page title, heading-3 for card titles,
  body-sm for metric labels
- Spacing: gap-6 between metric cards, padding-4 inside cards
- Components: Card, Select (date picker), Button, Badge, Skeleton

### Layout Structure

[Nav]
[Page Title + Date Range Selector + Export Button]
[KPI Card] [KPI Card] [KPI Card] [KPI Card] <- 4-col grid
[Line Chart (2/3 width)] [Pie Chart (1/3 width)] <- 2-col split
[Data Table (full width)] <- sortable, paginated

### Component Breakdown

1. KPICard - Displays single metric with trend indicator - { label, value, change, status }
2. DateRangeSelector - Preset ranges + custom date picker - { range, onRangeChange }
3. TrendChart - Line/area chart for time series data - { data, dateRange, metric }
4. DistributionChart - Pie/donut for categorical data - { data, metric }
5. MetricsTable - Sortable, paginated data table - { columns, data, sortBy, page }

### Interaction States

- Loading: Skeleton cards (pulse animation) matching final dimensions
- Error: Error banner with retry button, individual chart error boundaries
- Empty: "No data for selected range" with suggestion to expand range
- Success: Smooth number transitions (count-up animation) on data refresh

### Accessibility Requirements

- Keyboard navigation: Tab through cards, charts have data table alternatives
- Screen reader: Chart descriptions via aria-label, live region for metric updates
- Focus management: Date picker focus trap, return focus on close

### Responsive Behavior

- Mobile (< 640px): Single column, KPI cards stack vertically, charts full width
- Tablet (640-1024px): 2-col KPI grid, charts stack vertically
- Desktop (> 1024px): 4-col KPI grid, side-by-side charts
```

## Anti-Patterns

- Do NOT skip Step 2 (design system check) -- prompts without design tokens produce inconsistent UI
- Do NOT leave vague terms unresolved -- "nice" is not a specification
- Do NOT generate prompts without interaction states -- every view has loading, error, and empty states
- Do NOT ignore accessibility -- every enhanced prompt must include keyboard and screen reader specs
- Do NOT hardcode pixel values -- always reference design system tokens or relative units

## Iron Laws

1. **ALWAYS** analyze the original prompt for ambiguities and implicit assumptions before enhancing — never enhance a prompt whose scope you haven't verified with the caller.
2. **NEVER** add requirements that weren't implicit or explicit in the original — enhancement clarifies and structures; it does not invent scope.
3. **ALWAYS** preserve the original intent — an enhanced prompt that redirects to a different goal is a rewrite, not an enhancement.
4. **NEVER** produce an enhanced prompt longer than necessary to resolve ambiguities — verbosity in prompts reduces AI response quality; keep it focused.
5. **ALWAYS** include success criteria in the enhanced prompt — a prompt without acceptance criteria cannot be evaluated as done or not done.

## Memory Protocol (MANDATORY)

After using this skill, record learnings using `MemoryRecord`:

```javascript
MemoryRecord({
  type: 'pattern',
  text: 'enhance-prompt: [describe what design system pattern or prompt structure worked well]',
  area: 'frontend',
});
```

Write decisions to `.claude/context/memory/decisions.md` when choosing between design system approaches. Write issues to `.claude/context/memory/issues.md` when DESIGN.md is absent and fallback patterns were used.
