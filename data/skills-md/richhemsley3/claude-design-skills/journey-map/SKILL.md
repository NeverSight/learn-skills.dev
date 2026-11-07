---
name: journey-map
description: "Build interactive customer journey maps as standalone HTML files with D3.js. Use this skill whenever the user wants to create a journey map, experience map, service blueprint, or customer experience visualization showing phases, touchpoints, emotions, pain points, and opportunities. Also trigger when the user says 'journey map', 'customer journey', 'experience map', 'CX map', 'service blueprint', 'touchpoint map', or asks to visualize a user's end-to-end experience across stages. This is different from flow diagrams — journey maps focus on the emotional and experiential layer of a user's relationship with a product, not just the screen-by-screen navigation."
---

# Customer Journey Map Builder

Build interactive, data-rich customer journey maps as standalone HTML files powered by D3.js. Journey maps visualize the end-to-end experience of a user persona across phases of their relationship with a product — capturing not just what they do, but how they feel, what they need, and where the opportunities are.

## What Makes a Journey Map Different from a Flow Diagram

A **flow diagram** maps screens, clicks, and navigation paths — it's about the system. A **journey map** maps the human experience across time — it's about the person. Journey maps include emotional states, unmet needs, pain points, and opportunities alongside the functional steps. They're organized as a **grid/table** (phases × dimensions) rather than a **node-and-arrow graph**.

## Architecture

Every journey map is a single `.html` file with D3.js loaded from CDN. No build step, no npm — just open in a browser or serve via `npx serve`.

The map renders as a structured table/grid with:
- **Columns** = journey phases (horizontal axis, left to right)
- **Rows** = journey dimensions (vertical axis, stacked)
- **Emotion curve** = an SVG line chart overlaid across phases

### Interactive Features

- **Hover on cells**: Reveal full text content, highlight the column (phase) and row context
- **Click on phase headers**: Expand/collapse sub-phases or show a detail panel
- **Emotion curve tooltips**: Hover on data points to see sentiment score and annotation
- **Role badges**: Clickable to filter/highlight which roles are involved at each step
- **Responsive scroll**: Horizontal scroll when phases exceed viewport width, with sticky row labels
- **Export**: Print-friendly view via `@media print` styles

## Journey Map Structure

The journey map follows a **phases × dimensions** grid. Phases run left to right as columns; dimensions stack top to bottom as rows.

### Phases (Columns)

Each phase represents a stage in the customer's journey. Phases can contain sub-phases.

```
Phase 1: Awareness    Phase 2: Consideration    Phase 3: Purchase    Phase 4: Onboarding    Phase 5: Retention
├─ Step 1             ├─ Step 4                 ├─ Step 7            ├─ Step 9              ├─ Step 12
├─ Step 2             ├─ Step 5                 ├─ Step 8            ├─ Step 10             ├─ Step 13
└─ Step 3             └─ Step 6                                     └─ Step 11             └─ Step 14
```

### Dimensions (Rows)

Each row captures a different lens on the user's experience at each phase:

| Row | What It Captures | Visual Treatment |
|-----|-----------------|-----------------|
| **Phase** | Phase name and color indicator | Full-width background band (`#F4F1EB`) with bold dark text — NOT a pill badge |
| **Steps** | Individual steps within the phase | Column sub-headers with step labels |
| **Primary User** | Primary role responsible for this step | Color-coded role badge pill (each role has a unique color) |
| **Secondary Users** | Supporting roles involved | Multiple smaller role badge pills, stacked |
| **UX Score** | User sentiment across the journey (supports multi-user curves) | SVG line chart(s) with emoji markers (😊 😐 😞) — subtitle "Context: if applicable" |
| **Critical Unmet Needs** | What each role needs but doesn't have (per-role, filterable) | Text cells with italic emphasis — filtered by active role |
| **Workarounds** | What users do to fulfill unmet needs | Text cells describing behaviors |
| **Touchpoints** | Channels and interfaces used | Icon + text (e.g., 📱 Mobile App, 💻 Web Portal) |
| **Pain Points** | Frustrations and friction per role (filterable) | Red-accented text — filtered by active role (no icons) |
| **Opportunities** | Ideas for improvement per role (filterable) | Green-accented text — filtered by active role (no icons) |
| **Metrics / KPIs** | Measurable indicators | Small metric cards with values |
| **Reliance on Support** | How much users depend on human help — subtitle "if applicable" | Colored bar segments (Heavy / Medium / Light) |

Not every journey map needs all rows. Build what the user provides. The minimum viable journey map needs: Phases, Steps, Emotions, and at least one of (Needs / Pain Points / Opportunities).

## Design Standards

The journey map uses a **clean, spacious, minimal theme** — generous whitespace, subtle warm-gray borders, and restrained use of color. Phase headers are full-width background bands with bold dark text (NOT colored pills or pill badges). The overall feel is professional and airy, with content breathing in well-padded cells. This is a document-style artifact meant to be shared in presentations and stakeholder meetings.

### Color Palette

```css
/* ─── Canvas & Surface (layered: canvas < subtle < card < elevated) ─── */
--bg-canvas: #FAF8F5;            /* Page background (--sds-bg-surface, warm-gray-025) */
--bg-card: #FFFFFF;              /* Cell/card background (--sds-bg-card) */
--bg-header: #F4F1EB;            /* Row header background (--sds-bg-subtle, warm-gray-050) */
--bg-elevated: #FFFFFF;          /* Detail panels, tooltips (--sds-bg-elevated + shadow) */

/* ─── Borders ─── */
--border-subtle: #EBE6DD;        /* Grid lines between cells (--sds-border-subtle, warm-gray-100) */
--border-default: #E0DCD3;       /* Standard dividers (--sds-border-default, warm-gray-150) */
--border-strong: #D0CBC3;        /* Phase column separators (--sds-border-strong, warm-gray-200) */
--border-focus: #013D5B;         /* Focus ring (--sds-border-focus, blue-750) */

/* ─── Text ─── */
--text-primary: #1C1A17;         /* Headings, phase names (--sds-text-primary, warm-gray-900) */
--text-secondary: #54514D;       /* Body text, descriptions (--sds-text-secondary, warm-gray-650) */
--text-tertiary: #6B6760;        /* Muted labels, placeholders (--sds-text-tertiary, warm-gray-550) */
--text-disabled: #B0ABA2;        /* Disabled/placeholder (--sds-text-disabled, warm-gray-300) */
--text-on-primary: #FFFFFF;      /* Text on colored backgrounds (--sds-text-on-primary) */

/* ─── Interactive ─── */
--interactive-primary: #013D5B;          /* Selected/focused cells (--sds-interactive-primary, blue-750) */
--interactive-primary-hover: #05314D;    /* Hover on interactive (--sds-interactive-primary-hover, blue-800) */
--interactive-primary-subtle: #D9EBED;   /* Selection highlight (--sds-interactive-primary-subtle, blue-100) */

/* ─── Phase Header Band Color ─── */
/* Phase headers use a warm-gray background band with dark text — NOT pill badges */
--phase-header-bg: #F4F1EB;     /* Warm beige band background (--sds-bg-subtle, warm-gray-050) */
/* Phase accent colors are still available for subtle column tinting if needed */
--phase-1: #805AA1;              /* Purple - Awareness/Discovery (--sds-status-purple-text, purple-550) */
--phase-2: #013D5B;              /* Dark Blue - Consideration (--sds-interactive-primary, blue-750) */
--phase-3: #0C4A69;              /* Blue - Purchase/Action (--sds-status-info-text, blue-700) */
--phase-4: #7A9A01;              /* Green - Onboarding/Adoption (--sds-status-success-strong, green-400) */
--phase-5: #8A7515;              /* Warm Yellow - Retention/Growth (--sds-status-warning-text, yellow-500) */
--phase-6: #CF6253;              /* Red - Churn risk (--sds-status-error-strong, red-450) */

/* ─── Emotion Curve ─── */
--emotion-positive: #7A9A01;     /* Green for happy (--sds-status-success-strong) */
--emotion-neutral: #0C4A69;      /* Blue for neutral (--sds-status-info-text) */
--emotion-negative: #CF6253;     /* Red for frustrated (--sds-status-error-strong) */

/* ─── Status Accents ─── */
--accent-pain: #BF5547;          /* Pain point text (--sds-status-error-text, red-500) */
--accent-pain-bg: #FFEEEB;       /* Pain point cell bg (--sds-status-error-bg) */
--accent-opportunity: #62800B;   /* Opportunity text (--sds-status-success-text, green-500) */
--accent-opportunity-bg: #F4FAEB; /* Opportunity cell bg (--sds-status-success-bg) */
--accent-need: #8A7515;          /* Unmet need text (--sds-status-warning-text) */
--accent-need-bg: #FCF9D9;       /* Unmet need cell bg (--sds-status-warning-bg) */

/* ─── Role Badge Colors (assigned per-role in order of appearance) ─── */
--role-1: #013D5B;               /* 1st role - Dark Navy */
--role-2: #4A6E82;               /* 2nd role - Steel Blue */
--role-3: #5C7A3D;               /* 3rd role - Forest Green */
--role-4: #805AA1;               /* 4th role - Purple */
--role-5: #8A7515;               /* 5th role - Warm Gold */
--role-6: #CF6253;               /* 6th role - Coral Red */
```

### Typography

- **Font stack**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Journey title**: 24px, `font-weight: 700`, `--text-primary` — format: "Customer Journey Domain Title │ Project Title" with a light separator and lighter subtitle
- **Phase names**: 14px, `font-weight: 700`, `--text-primary` (#1C1A17) on warm-gray background band, uppercase
- **Step labels**: 12px, `font-weight: 400`, `--text-tertiary` (#6B6760) — light and understated
- **Row labels**: 12px, `font-weight: 600`, `--text-tertiary` (#6B6760), uppercase tracking
- **Cell content**: 12px, `font-weight: 400`, `--text-secondary` (#54514D)
- **Metric values**: 16px, `font-weight: 700`, phase color

### Grid Layout

The journey map uses CSS Grid for the table structure with fixed row headers. The overall feel is **spacious and minimal** — generous whitespace, subtle borders, and clean separation between cells.

- **Row header column**: 140px fixed width, sticky on horizontal scroll
- **Step columns**: Each step column is `minmax(180px, 220px)` wide (generous width for readability)
- **Phase header row**: 44px tall, `#F4F1EB` background band spanning all step columns per phase
- **Step header row**: 36px tall, white background, centered text
- **Role rows**: 52px tall (room for badge pills with breathing room)
- **Emotion row**: 120px tall (space for the line chart)
- **Content rows**: `auto` height, minimum 72px, padding `12px 16px`
- **Grid gap**: 0 (no gap-based borders)
- **Cell borders**: `1px solid rgba(208, 203, 195, 0.4)` — very subtle warm-gray dividers between cells
- **Phase separators**: `1px solid #E0DCD3` between phase groups (subtle, not heavy)
- **Row background**: Alternating white `#FFFFFF` and `#FAFAF8` for gentle zebra striping
- **Cell background on step columns**: Subtle `#FAF8F5` tinting on content cells

### Phase Header Bands

Each phase gets a **full-width background band** spanning all of its step columns. This is NOT a pill or badge — it's a header row with a solid background fill:

```
  ┌───────────────────────────────────────┐  ┌──────────────────────────────────┐
  │            PHASE 1                    │  │           PHASE 2                │
  └───────────────────────────────────────┘  └──────────────────────────────────┘
  Step 1    Step 2    Step 3                 Step 4    Step 5    Step 6
```

- Shape: Rectangular band spanning the full width of all step columns in that phase
- Height: 44px
- Background: `#F4F1EB` (--bg-header, warm-gray-050) — a subtle warm beige, NOT dark navy
- Text: `#1C1A17` (--text-primary), 14px, `font-weight: 700`, uppercase letter-spacing `0.5px`, centered
- No border-radius — flush edges that align with the grid columns
- The band merges/spans across all step columns belonging to that phase (use `grid-column` spanning)
- 1px border between phases: `1px solid #E0DCD3` (--border-default)

### Role Badge Pills

Every role badge — whether in the Primary User or Secondary Users row — uses the **same color from the role palette**. This ensures one consistent color per persona across the entire map, matching the role legend.

**Primary User badge** (single primary role per step):
- Shape: Full-width rounded pill spanning the step column width
- Height: 28px, padding: `0 12px`
- Border-radius: `14px`
- Background: **Color from role palette, looked up by role name** — e.g. if the role is "Product Manager" and that role is assigned `#013D5B`, the badge is `#013D5B`. If the role is "New User" assigned `#4A6E82`, the badge is `#4A6E82`. Each distinct role name gets its OWN color — do NOT use the same color for all primary user badges.
- Text: White, 11px, `font-weight: 600`, centered
- One badge per cell, centered vertically
- **IMPORTANT**: The badge color comes from `step.primaryUser.color` in the data, which must match the role's color in `journeyData.roles[]`. Different role names = different colors.

**Secondary User badges** (multiple supporting roles per step):
- Shape: Smaller rounded pills, stacked vertically with 4px gap
- Height: 22px, padding: `0 10px`
- Border-radius: `11px`
- Background: **Color from role palette** — same color as if this role appeared in the Primary User row
- Text: White, 10px, `font-weight: 500`
- No border (the role color fill provides enough contrast)
- Multiple badges stack vertically within the cell

**Color consistency rule**: A role like "Engineering" MUST always use the same color everywhere it appears — in Primary User pills, Secondary User pills, role legend dots, per-role content dots, and UX Score curves. Colors are assigned once from the palette and never reused for a different role.

```
Primary User row:
┌────────────────────────────────┐
│       Product Manager          │  ← Dark Navy (#013D5B)
└────────────────────────────────┘

Secondary Users row:
  ┌──────────────┐
  │  Engineering │  ← Steel Blue (#4A6E82), same as legend
  └──────────────┘
  ┌──────────────┐
  │    Design    │  ← Forest Green (#5C7A3D), same as legend
  └──────────────┘
```

### Role Color Palette

Each role in the journey map gets a unique color. Owner badges use these as their fill; the role legend displays colored dots for each role. Assign colors in order of appearance:

| Role Slot | Color | Hex | Usage |
|-----------|-------|-----|-------|
| Role A (1st) | Dark Navy | `#013D5B` | Primary role |
| Role B (2nd) | Steel Blue | `#4A6E82` | Secondary role |
| Role C (3rd) | Forest Green | `#5C7A3D` | Tertiary role |
| Role D (4th) | Purple | `#805AA1` | Quaternary role |
| Role E (5th) | Warm Gold | `#8A7515` | Fifth role |
| Role F (6th) | Coral Red | `#CF6253` | Sixth role |

### Role Legend

A compact legend in the top-right corner of the map showing all roles with their assigned color:

```
                                            Roles: ● A  ● B  ● C  ● D
```

- Position: Top-right, aligned with the title bar
- Each role shown as a small filled circle (5px radius) + abbreviated label
- Font: 9px, `--text-tertiary` (#6B6760)
- Spacing: 30px between each role entry
- Only show roles that actually appear in the journey data

### UX Score / Emotion Curve (Multi-User)

The UX Score row contains SVG line chart(s) that span all phase columns. **Multiple user perspectives** can be overlaid on the same chart:

- **Chart area**: The SVG MUST span the full width of ALL step columns (excluding row label column), 150px tall. The emotion row container must use `grid-column` to span from column 2 to the last column, and the SVG `width` must be calculated from the actual rendered container width (use `requestAnimationFrame` or `setTimeout(0)` to ensure the container has been laid out before reading its width). Set `overflow: visible` on the container and `position: relative; z-index: 1` to prevent clipping behind adjacent cells
- **Primary line**: 2.5px solid stroke, `#0C4A69` (--emotion-neutral) — represents the primary user/role perspective
- **Secondary line(s)**: 2px dashed stroke (`stroke-dasharray: 6,3`), colored by role color — represents additional user perspectives
- **Data points (primary)**: 5px radius circles, color-coded by score: green (`#7A9A01`) > 0.6, blue (`#0C4A69`) 0.3–0.6, red (`#CF6253`) < 0.3
- **Data points (secondary)**: 4px radius circles, role color with 0.7 opacity
- **Emoji markers**: 😊 (score > 0.6), 😐 (0.3–0.6), 😞 (< 0.3) — positioned above primary line data points only
- **Background bands**: Three subtle horizontal bands showing positive (`rgba(122,154,1, 0.04)` green), neutral (`rgba(12,74,105, 0.04)` blue), negative (`rgba(207,98,83, 0.04)` red) zones
- **Curve legend**: Small legend in bottom-right of UX Score row showing line style + role name for each curve (solid line = primary, dashed = secondary)
- **Tooltips**: On hover, show the step name, emotion score, role, and annotation text
- **Line interpolation**: Use `d3.curveMonotoneX` for smooth but non-overshooting curves
- **Row label subtitle**: "Context: if applicable" in 9px muted text below "UX Score"

### Reliance on Support Bar

The bottom row shows how much users rely on human support at each step:

- Colored bar segments within each cell
- Colors: `#1C1A17` (--sds-text-primary) for Heavy, `#54514D` (--sds-text-secondary) for Medium, `#B0ABA2` (--sds-text-disabled) for Light
- Height: 8px bar, centered vertically in the cell
- Label below the bar: "Heavy" / "Medium" / "Light" in 10px text

### Interaction & Hover

- **Cell hover**: Very subtle warm highlight (`rgba(244, 241, 235, 0.6)`) on the cell — no box-shadow
- **Column hover**: When hovering any cell, lightly tint the entire column with `rgba(0, 0, 0, 0.015)`
- **Row hover**: Lightly highlight the row header with `#F4F1EB`
- **Phase header click**: Scroll to center that phase, or expand sub-phases
- **Emotion point hover**: Show tooltip with score and annotation, enlarge circle to 12px
- **Role badge click**: Toggle a role filter — when a role is selected:
  - Pain Points, Critical Unmet Needs, and Opportunities rows show only that role's content
  - The UX Score curve highlights that role's line
  - Active role badge gets a 2px white outline ring
  - **All non-selected role badges fade to 30% opacity** (`opacity: 0.3`) — both Primary User and Secondary User pills that don't match the active role. This makes the selected role visually pop across the entire map.
  - Non-selected role legend dots also fade to 30% opacity
  - Click again to deselect: all roles return to full opacity and all content is shown
- **Cursor**: `pointer` on interactive elements, `default` on content cells

### Sticky Behavior

- **Row label column**: `position: sticky; left: 0; z-index: 3` — stays visible when scrolling horizontally
- **Phase header row**: `position: sticky; top: 0; z-index: 2` — sticks to top of viewport when scrolling vertically. Background must be opaque (`#F4F1EB`) so content scrolls beneath it.
- **Step header row**: `position: sticky; top: 44px; z-index: 2` — sticks directly below the phase row (44px = phase row height). Background must be opaque (`#FFFFFF`) so content scrolls beneath it.
- **Corner cell** (row label × phase/step intersection): `z-index: 4` — must be above both sticky axes
- **Scroll shadows**: Subtle `box-shadow: 0 2px 4px rgba(0,0,0,0.08)` on sticky rows when scrolled past their natural position

## Building the HTML File

### Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Journey Name] — Customer Journey Map</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    /* Light theme — all styles inline */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #FAF8F5;
      color: #1C1A17;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    /* Title bar, grid container, cells, emotion chart, role badges, tooltips */
  </style>
</head>
<body>
  <!-- Title bar with journey name and persona info -->
  <!-- Grid container with sticky headers -->
  <!-- Emotion curve: D3 appends an <svg> element into the emotion-row container -->
  <!-- Tooltip container -->
  <script>
    /* Journey data as JS object */
    /* D3 rendering: grid, emotion curve, role badges */
    /* Interaction handlers: hover, click, filter, scroll */
  </script>
</body>
</html>
```

### Data Structure

Define the journey data as a JavaScript object at the top of the script:

```javascript
const journeyData = {
  title: "Customer Journey Map",
  persona: {
    name: "Persona Name",
    role: "Role / Segment",
    goal: "Primary goal statement"
  },
  phases: [
    {
      id: "awareness",
      label: "Awareness",
      icon: "search",           // Lucide-style icon name
      color: "#805AA1",        // Phase accent color (--sds-status-purple-text)
      steps: [
        {
          id: "step-1",
          label: "Step 1 Name",
          primaryUser: { name: "Product Manager", color: "#013D5B" },
          secondaryUsers: [
            { name: "Engineering", color: "#4A6E82" },
            { name: "Design", color: "#5C7A3D" }
          ],
          emotion: {
            score: 0.7,         // 0 (worst) to 1 (best) — primary user
            label: "Excited",
            annotation: "User discovers the product through a recommendation"
          },
          // Optional: additional user perspective emotions for multi-line UX score
          secondaryEmotions: [
            {
              role: "Role B",      // Must match a role name
              score: 0.4,
              label: "Uncertain",
              annotation: "Secondary user has less context"
            }
          ],
          // Role-scoped content: pain points, needs, and opportunities are per-role
          // Clicking a role badge filters these rows to show that role's perspective
          needs: {
            "Product Manager": "Need to understand value proposition quickly",
            "Engineering": "Need clear technical requirements"
          },
          workarounds: "Reads landing page, watches demo video",
          touchpoints: ["Website", "Social Media"],
          painPoints: {
            "Product Manager": ["Too much jargon on landing page"],
            "Engineering": ["Unclear integration requirements"]
          },
          opportunities: {
            "Product Manager": ["Add interactive product tour"],
            "Engineering": ["Provide API sandbox"]
          },
          metrics: { name: "Bounce Rate", value: "45%" },
          supportReliance: "light"  // "heavy" | "medium" | "light"
        }
      ]
    }
  ],
  // Roles that appear across the map — each gets a unique color from the Role Color Palette
  // Colors are assigned in order: #013D5B, #4A6E82, #5C7A3D, #805AA1, #8A7515, #CF6253
  roles: [
    { name: "Product Manager", abbrev: "PM", color: "#013D5B" },
    { name: "Engineering", abbrev: "Eng", color: "#4A6E82" },
    { name: "Design", abbrev: "Des", color: "#5C7A3D" },
    { name: "Support", abbrev: "Spt", color: "#805AA1" }
  ]
};
```

### Per-Role Content Model

Pain Points, Critical Unmet Needs, and Opportunities are **scoped per role** — each role can have different pain points and opportunities at each step. This reflects that a Product Manager's frustrations at a given step differ from Engineering's.

**Data format**: These fields are objects keyed by role name:

```javascript
painPoints: {
  "Product Manager": ["Too much jargon on landing page"],
  "Engineering": ["Unclear integration requirements"]
}
```

**Default display**: When no role is selected (no filter active), show ALL roles' content in the cell, each prefixed with a small colored dot matching the role's color:

```
● PM: Too much jargon on landing page
● Eng: Unclear integration requirements
```

**Filtered display**: When a role badge is clicked, only that role's content appears. Other roles' entries are hidden (not just dimmed).

**Backward compatibility**: If the user provides these fields as simple strings or arrays (not keyed by role), treat them as applying to all roles and display without role prefixes.

### D3 Rendering

The journey map combines HTML grid layout (for the table structure) with D3.js SVG (for the emotion curve). This is not a purely SVG-based visualization like a flow diagram.

**Grid rendering approach:**

1. Build the HTML grid structure with `document.createElement` or template literals
2. Populate cells from `journeyData`
3. Use D3 only for the emotion curve SVG and any data-driven visualizations
4. Attach event listeners for hover/click interactions

**Emotion curve rendering:**

Include a static `<svg>` element in the emotion row container in the HTML body (not dynamically created via JS). D3 then selects this existing `<svg>` and populates it:

```html
<!-- In the emotion row container -->
<div id="emotion-row" class="emotion-row-container">
  <svg id="emotion-svg"></svg>
</div>
```

```javascript
// IMPORTANT: Defer rendering until the container has been laid out
// so that scrollWidth/clientWidth are accurate
requestAnimationFrame(() => {
  const container = document.getElementById('emotion-row');
  const totalContentWidth = container.scrollWidth || container.clientWidth;

  const emotionSvg = d3.select('#emotion-svg')
    .attr('width', totalContentWidth)
    .attr('height', 150)
    .style('overflow', 'visible')
    .style('position', 'relative')
    .style('z-index', '1');

// Flatten all steps across phases
const allSteps = journeyData.phases.flatMap(p => p.steps);

// X scale: one point per step, positioned at column centers
const xScale = d3.scaleLinear()
  .domain([0, allSteps.length - 1])
  .range([firstColCenter, lastColCenter]);

// Y scale: emotion score 0-1 mapped to chart height
const yScale = d3.scaleLinear()
  .domain([0, 1])
  .range([90, 10]);  // inverted: higher score = higher on chart

// Line generator
const line = d3.line()
  .x((d, i) => xScale(i))
  .y(d => yScale(d.emotion.score))
  .curve(d3.curveMonotoneX);

// Draw the primary emotion line
emotionSvg.append('path')
  .datum(allSteps)
  .attr('d', line)
  .attr('fill', 'none')
  .attr('stroke', '#0C4A69')
  .attr('stroke-width', 2.5)
  .attr('stroke-linecap', 'round');

// Draw secondary emotion lines (multi-user)
// Collect unique secondary roles from the data
const secondaryRoles = [...new Set(
  allSteps.flatMap(s => (s.secondaryEmotions || []).map(e => e.role))
)];

secondaryRoles.forEach(role => {
  const roleColor = journeyData.roles.find(r => r.name === role)?.color || '#CF6253';
  const secondaryLine = d3.line()
    .x((d, i) => xScale(i))
    .y(d => {
      const se = (d.secondaryEmotions || []).find(e => e.role === role);
      return yScale(se ? se.score : 0.5);
    })
    .curve(d3.curveMonotoneX);

  emotionSvg.append('path')
    .datum(allSteps)
    .attr('d', secondaryLine)
    .attr('fill', 'none')
    .attr('stroke', roleColor)
    .attr('stroke-width', 2)
    .attr('stroke-dasharray', '6,3')
    .attr('stroke-linecap', 'round');

  // Secondary data points (smaller, semi-transparent)
  emotionSvg.selectAll(`.emotion-dot-${role}`)
    .data(allSteps)
    .join('circle')
    .attr('cx', (d, i) => xScale(i))
    .attr('cy', d => {
      const se = (d.secondaryEmotions || []).find(e => e.role === role);
      return yScale(se ? se.score : 0.5);
    })
    .attr('r', 4)
    .attr('fill', roleColor)
    .attr('opacity', 0.7);
});

// Draw primary data points (on top)
emotionSvg.selectAll('.emotion-dot')
  .data(allSteps)
  .join('circle')
  .attr('cx', (d, i) => xScale(i))
  .attr('cy', d => yScale(d.emotion.score))
  .attr('r', 5)
  .attr('fill', d => d.emotion.score > 0.6 ? '#7A9A01'
                    : d.emotion.score > 0.3 ? '#0C4A69' : '#CF6253');
```

### Key Implementation Details

**Responsive horizontal scroll**: The grid container has `overflow-x: auto`. Row labels are sticky. Phase headers should remain visible as you scroll.

**Phase color propagation**: Each phase's accent color tints its column cells with a very subtle background: `rgba(phase-color, 0.03)`. This creates visual "swim lanes" without being overwhelming.

**Print styles**: Include `@media print` rules that linearize the grid for A3/landscape printing — each phase becomes a section with its dimensions listed vertically.

**Empty state handling**: If a dimension has no data for a step, show a dashed border cell with muted placeholder text ("—" or "No data"). Don't leave cells visually empty.

## Accepting Journey Content from the User

When the user provides journey content, expect it organized by phase:

**Phases** — stage names, descriptions, step breakdowns
**Emotions** — sentiment/satisfaction at each step
**Needs & Pain Points** — what users struggle with
**Opportunities** — improvement ideas
**Roles** — who owns each step

The user may provide this as:
- A structured markdown document organized by phases and dimensions
- A spreadsheet/table format (copy-pasted)
- A bullet-point outline describing the journey
- A verbal description of the user's experience to interpret
- An existing journey map image to recreate

If the content is sparse, build what's provided and suggest additional dimensions to fill in. Always render at minimum: phases, steps, and one experiential dimension (emotions, pain points, or needs).

## Iteration Prompts

Recognize these as refinements to the existing journey map:

| User says | What to do |
|-----------|-----------|
| "add pain points" | Add a Pain Points row with red-accented cells |
| "add opportunities" | Add an Opportunities row with green-accented cells |
| "add the emotion curve" | Add/update the UX Score SVG line chart |
| "add a second user" | Add a secondary emotion curve (dashed line) for another role's perspective |
| "add role badges" | Add Primary User/Secondary Users rows with color-coded pills |
| "add a new phase" | Add a column group to the right |
| "show metrics" | Add a Metrics/KPIs row with metric cards |
| "add touchpoints" | Add a Touchpoints row with channel icons |
| "make it printable" | Enhance print styles for A3 landscape |
| "add sub-phases" | Break a phase column into sub-columns |
| "color code by sentiment" | Tint cell backgrounds based on emotion scores |
| "add a persona header" | Add persona info (photo placeholder, name, role, goal) above the map |

## Serving the Journey Map

After building the HTML file, serve it using the project's dev server configuration. Save the file in the user's project directory and ensure `launch.json` is configured to serve it. Open it in the browser for the user to interact with.

## Next Steps

After building the journey map, suggest:
- "Want me to add more dimensions like touchpoints or pain points?"
- "Should I add emotion annotations to explain the sentiment curve?"
- "Want to add a persona header with user details?"
- "Should I create a companion flow diagram showing the screen-level navigation for a specific phase?"
