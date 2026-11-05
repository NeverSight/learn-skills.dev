---
name: screen-flow-diagram
description: "Build interactive screen flow diagrams as standalone HTML files using D3.js, showing simplified wireframe mockups connected by action labels. Use this skill whenever the user wants to create a screen flow, wireflow, UI flow, or navigation map that shows how users move between actual screens by interacting with specific UI elements. Also trigger when the user says 'screen flow', 'wireflow', 'UI flow', 'navigation flow', 'screen map', 'tap flow', or asks to map out how screens connect to each other through user actions. This is different from abstract flow diagrams (which use generic boxes) — screen flows show simplified wireframe representations of actual screens with realistic UI elements inside them."
---

# Screen Flow Diagram Builder

Build interactive screen flow diagrams as standalone HTML files powered by D3.js. Screen flows are visual navigation maps that show **simplified wireframe mockups** of actual screens, connected by **action labels** that describe what the user clicks/taps to move between them. They answer the question: "What does the user see, and what do they tap to get to the next screen?"

## What Makes a Screen Flow Different

| Artifact | What it shows | Node style |
|----------|--------------|------------|
| **Flow diagram** | Abstract process with phases and decisions | Generic boxes, diamonds |
| **Screen flow** | Concrete screen-to-screen navigation | Wireframe mockups with UI elements |
| **Journey map** | Emotional/experiential view across time | Table grid with phases × dimensions |

A screen flow lives in the middle ground: more visual than an abstract flow diagram, but more structural than a full prototype. Screens contain simplified placeholder content (headers, cards, buttons, lists) that communicates the *type* of screen without showing actual content.

## Architecture

Every screen flow is a single `.html` file with D3.js loaded from CDN. No build step, no npm — just open in a browser or serve via `npx serve`.

The diagram renders as an SVG canvas with:
- **Screen mockup nodes**: Rounded rectangles containing simplified wireframe content
- **Action label pills**: Dark blue rounded-rectangle labels on connector lines describing the user action
- **Connector lines**: Dark blue lines with arrowheads routing between screens
- **Connection ports**: Small dark blue circles where connectors attach to screens
- **Pan & zoom**: D3 zoom behavior for navigating large flows

## Screen Mockup Anatomy

Each screen mockup represents a simplified wireframe of an actual application screen. The mockup communicates the *type* of UI without showing real content.

### Screen Frame

```
┌─────────────────────────────┐
│ ● ● ●                      │  ← Status bar dots (mobile) or browser chrome
│ ┌─────────────────────────┐ │
│ │  ◄  Screen Title    ⋮   │ │  ← Navigation bar with back arrow, title, menu
│ ├─────────────────────────┤ │
│ │                         │ │
│ │   [Content Area]        │ │  ← Screen-type-specific content
│ │                         │ │
│ │                         │ │
│ ├─────────────────────────┤ │
│ │  ┌─────────────────┐    │ │
│ │  │    Button        │    │ │  ← Interactive elements (green fill)
│ │  └─────────────────┘    │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
    Screen Name Label            ← Name label below the frame
```

### Content Types

Different screen types get different wireframe content:

| Screen Type | Content Wireframe |
|------------|-------------------|
| **List / Feed** | Stacked horizontal bars (card rows), each with a small icon square left + text lines right |
| **Detail** | Large rectangle at top (hero/image), text lines below, action button at bottom |
| **Form** | Stacked input fields (rounded rectangles with label text), submit button |
| **Dashboard** | 2×2 grid of small rectangles (metric cards), chart area below |
| **Empty state** | Centered icon, two short text lines, CTA button |
| **Settings** | Stacked rows with label left + toggle/chevron right |
| **Modal / Dialog** | Smaller rectangle centered within the screen, dimmed background, buttons |
| **Login** | Centered form with logo placeholder, two inputs, button |

Wireframe elements use these colors:
- Content placeholder bars: `#EBE6DD` (warm gray, --sds-border-subtle)
- Highlighted/selected row: `#D9EBED` (light blue tint, --sds-interactive-primary-subtle)
- Interactive buttons inside screens: `#013D5B` fill, white text (--sds-interactive-primary)
- Text placeholders: `#E0DCD3` (warm gray, --sds-border-default)
- Screen background: `#FFFFFF` (--sds-bg-card)
- Screen border: `#E0DCD3`, 1px, 16px border-radius (--sds-border-default)

### Screen Dimensions

- **Mobile screens**: 160px wide × 280px tall (portrait)
- **Desktop screens**: 280px wide × 180px tall (landscape)
- **Tablet screens**: 220px wide × 160px tall
- Border radius: 16px (matches device rounding)
- Drop shadow: `0 2px 8px rgba(0,0,0,0.06)` for subtle depth

## Action Label Pills

Action labels sit **on the connector lines** between screens, describing what the user does to navigate:

```
[Screen A] ──● ────── ( Click Card ) ────── ●── [Screen B]
              port     action label          port
```

### Visual Treatment

Path labels must be **visually distinct from in-screen buttons**. In-screen buttons use solid fills to represent actual UI; path labels use an outlined style to represent navigation actions.

- **Shape**: Rounded rectangle (stadium), 11px border-radius
- **Background**: `#FFFFFF` (white fill)
- **Border**: 1.5px solid, color matches the connector line color
- **Text**: Connector color, 8.5px, font-weight 600
- **Accent dot**: Small colored circle (3px radius) on the left inside the pill
- **Height**: 22px
- **Padding**: 0 12px
- **Examples**: "Click Card", "Tap Button", "Submit Form", "Swipe Left", "Pull Down", "Go Back", "Long Press"

**Why outlined instead of solid?** In-screen buttons (inside wireframe mockups) use solid dark blue fills (`#013D5B`) with white text. If path labels also use solid fills, they become indistinguishable from buttons at a glance. The outlined style — white background, colored border, colored text, accent dot — creates an immediate visual distinction between "this is a UI element" and "this is a navigation action on the flow diagram."

```javascript
// Path label rendering (outlined style)
const w = label.length * 5.2 + 24;
roundRect(ig, -w/2, -11, w, 22, 11, '#FFFFFF', connColor, 1.5);  // white bg, colored border
ig.append('circle').attr('cx', -w/2 + 9).attr('cy', 0).attr('r', 3).attr('fill', connColor);  // accent dot
txt(ig, 3, 4, label, 8.5, connColor, 600, 'middle');  // colored text

// In-screen button rendering (solid style — unchanged)
roundRect(g, x, y, w, h, h/2, '#013D5B', 'none');  // solid blue fill
txt(g, x+w/2, y+h*0.65, label, 7, '#FFF', 500, 'middle');  // white text
```

### Connection Ports

Small dark blue circles that mark where a connector attaches to a screen edge:

- **Diameter**: 10px
- **Fill**: `#013D5B` (--sds-interactive-primary)
- **Border**: 2px solid white
- **Position**: Centered on the screen's edge at the attachment point
- **Inner dot**: 4px white circle centered inside (optional, for emphasis)

## Connector Lines

Lines connect screens through action labels. The routing follows these rules:

### Line Style

- **Color**: `#013D5B` (--sds-interactive-primary), matching the action pills
- **Width**: 2px stroke
- **Arrowheads**: Filled dark blue triangles, 8×6px, defined as SVG `<marker>`
- **Routing**: Prefer orthogonal (right-angle) paths. Use straight horizontal/vertical segments with 90° turns. Build as SVG `<path>` with M, H, V, L commands.
- **When orthogonal routing is too complex** (overlapping lines): Fall back to smooth curves with `d3.curveBasis` or `curveMonotoneX`

### Connection Pattern

The full connection chain is:
```
Screen edge → port (blue dot) → line → action pill → line → port → Screen edge
```

- Connectors exit from the **nearest edge** of the source screen to the target
- For horizontal flows: exit right edge, enter left edge
- For vertical branches: exit bottom edge, enter top edge
- For "go back" connections: exit left/top edge with a curved path

## Design Standards

### Color Palette

The screen flow uses the **Software Design System (SDS) light theme** — warm-toned with dark blue as the primary accent for all interactive/connective elements:

```css
/* ─── Canvas & Surface (layered: canvas < subtle < card < elevated) ─── */
--bg-canvas: #FAF8F5;           /* Canvas background (--sds-bg-surface, warm-gray-025) */
--bg-screen: #FFFFFF;           /* Screen mockup fill (--sds-bg-card) */
--bg-subtle: #F4F1EB;           /* Nav bar bg, sub-surfaces (--sds-bg-subtle, warm-gray-050) */
--bg-elevated: #FFFFFF;         /* Detail panel, title bar (--sds-bg-elevated + shadow) */
--bg-content: #EBE6DD;          /* Wireframe content placeholder (--sds-border-subtle, warm-gray-100) */
--bg-content-active: #D9EBED;   /* Highlighted/selected content (--sds-interactive-primary-subtle, blue-100) */

/* ─── Text ─── */
--text-primary: #1C1A17;        /* Screen names, titles (--sds-text-primary, warm-gray-900) */
--text-secondary: #54514D;      /* Descriptions, labels (--sds-text-secondary, warm-gray-650) */
--text-tertiary: #6B6760;       /* Muted labels (--sds-text-tertiary, warm-gray-550) */
--text-wireframe: #B0ABA2;      /* Placeholder text inside wireframes (--sds-text-disabled, warm-gray-300) */
--text-on-primary: #FFFFFF;     /* Text on primary-colored backgrounds (--sds-text-on-primary) */

/* ─── Borders ─── */
--border-subtle: #EBE6DD;       /* Faint separators (--sds-border-subtle, warm-gray-100) */
--border-default: #E0DCD3;      /* Screen borders, dividers (--sds-border-default, warm-gray-150) */
--border-strong: #D0CBC3;       /* Hover borders, strong separators (--sds-border-strong, warm-gray-200) */
--border-focus: #013D5B;        /* Focus ring (--sds-border-focus, blue-750) */

/* ─── Interactive (connectors + actions) ─── */
--interactive-primary: #013D5B;         /* Action pills, connectors, ports, buttons (--sds-interactive-primary, blue-750) */
--interactive-primary-hover: #05314D;   /* Hover state (--sds-interactive-primary-hover, blue-800) */
--interactive-primary-subtle: #D9EBED;  /* Subtle highlight (--sds-interactive-primary-subtle, blue-100) */

/* ─── Screen Frame ─── */
--screen-border: #E0DCD3;       /* Screen mockup border (--sds-border-default) */
--screen-shadow: rgba(0,0,0,0.06); /* Drop shadow */
--screen-nav-bg: #F4F1EB;       /* Navigation bar background within screen (--sds-bg-subtle) */

/* ─── Status ─── */
--status-start: #7A9A01;        /* Start node (--sds-status-success-strong, green-400) */
--status-end: #7A9A01;          /* End node (--sds-status-success-strong) */
--status-error: #CF6253;        /* Error path (--sds-status-error-strong, red-450) */
--status-error-bg: #FFEEEB;     /* Error screen background tint (--sds-status-error-bg) */
--status-error-text: #BF5547;   /* Error labels (--sds-status-error-text, red-500) */
--status-success-bg: #F4FAEB;   /* Success/confirmation bg (--sds-status-success-bg, green-025) */
--status-success-text: #62800B; /* Success labels (--sds-status-success-text, green-500) */
--status-warning-bg: #FCF9D9;   /* Warning bg (--sds-status-warning-bg, yellow-025) */
--status-warning-text: #8A7515; /* Warning labels (--sds-status-warning-text, yellow-500) */
--status-info-bg: #EBF4F5;      /* Info bg (--sds-status-info-bg, blue-050) */
--status-info-text: #0C4A69;    /* Info labels (--sds-status-info-text, blue-700) */
```

### Typography

- **Font stack**: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Screen name labels**: 13px, font-weight 600, `--text-primary`, centered below the screen
- **Action pill text**: 11px, font-weight 500, white
- **Screen title (inside nav bar)**: 10px, font-weight 600, `--text-primary`
- **Wireframe placeholder text**: 8px, `--text-wireframe`
- **Flow title**: 24px, font-weight 700, `--text-primary`
- **Flow description**: 14px, font-weight 400, `--text-secondary`

### Spacing & Layout

- **Horizontal spacing between screens**: 300–400px center-to-center. Room for action pills on connectors.
- **Vertical spacing for branches**: 350–400px center-to-center (screens are tall, need more vertical space than abstract nodes).
- **Screen name label**: 12px below the screen's bottom edge, centered
- **Primary flow direction**: Left to right (horizontal)
- **Branches**: Top to bottom for alternatives / error paths

### Interaction

- **Pan**: Click-drag on canvas background, or arrow keys
- **Zoom**: Mouse wheel / pinch, +/- keys. Range: 0.15x–3x
- **Screen hover**: Border strengthens to `#D0CBC3` (--sds-border-strong), shadow deepens to `rgba(0,0,0,0.10)`, subtle `transform: scale(1.01)`
- **Action pill hover**: Darkens to `#05314D` (--sds-interactive-primary-hover), cursor pointer
- **Screen click**: Opens a detail panel/sidebar showing screen name, type, description, and the list of exits
- **Fit-to-content**: On load and on double-click empty canvas, call `fitToContent()`

### Detail Panel (Click a Screen)

When clicking a screen mockup, a slide-in sidebar (right side, 320px wide) shows:

- **Screen name** (bold, 18px)
- **Screen type** badge (e.g., "List View", "Form", "Dashboard")
- **Description**: What happens on this screen
- **UI Elements**: List of interactive elements on the screen
- **Exits**: Where the user can go from here (action → target screen)
- **Close button** or click-outside to dismiss

## Building the HTML File

### Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>[Flow Name] — Screen Flow</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    /* Light theme — all styles inline */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #FAF8F5;
      color: #1C1A17;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      overflow: hidden;
    }
    /* Title bar, screen mockups, action pills, connectors, detail panel */
  </style>
</head>
<body>
  <!-- Title bar -->
  <!-- SVG canvas for D3 rendering -->
  <!-- Detail sidebar -->
  <script>
    /* Screen flow data */
    /* D3 rendering: screens, connectors, action pills */
    /* Interaction handlers: pan, zoom, click, hover */
  </script>
</body>
</html>
```

### Data Structure

```javascript
const flowData = {
  title: "Screen Flow Name",
  description: "Brief description of the flow",
  deviceType: "mobile",  // "mobile" | "desktop" | "tablet"
  screens: [
    {
      id: "home",
      name: "Home Screen",
      type: "list",        // list | detail | form | dashboard | empty | settings | modal | login
      description: "Main feed showing personalized content cards",
      navTitle: "Home",
      elements: [
        { type: "navbar", content: "Home" },
        { type: "search-bar" },
        { type: "card-row", content: "Featured Item", highlighted: false },
        { type: "card-row", content: "Recent Item 1" },
        { type: "card-row", content: "Recent Item 2" },
        { type: "card-row", content: "Recent Item 3" },
        { type: "button", content: "Create New", isAction: true }
      ],
      exits: [
        { action: "Click Card", target: "detail" },
        { action: "Tap Create", target: "create-form" },
        { action: "Tap Search", target: "search" }
      ]
    },
    {
      id: "detail",
      name: "Item Detail",
      type: "detail",
      description: "Full detail view of a selected item",
      navTitle: "← Item Detail",
      elements: [
        { type: "navbar", content: "← Detail", hasBack: true },
        { type: "hero-image" },
        { type: "text-block", lines: 3 },
        { type: "button", content: "Take Action", isAction: true }
      ],
      exits: [
        { action: "Go Back", target: "home" },
        { action: "Tap Action", target: "confirm-modal" }
      ]
    }
  ]
};
```

### D3 Rendering

Screen flow diagrams are rendered entirely in SVG using D3.js. Each screen mockup is a `<g>` group containing:

1. **Frame**: `<rect>` with rounded corners, white fill, light border, drop shadow (via `<filter>`)
2. **Status bar**: Three small circles at the top (mobile) or a thin gray bar (desktop)
3. **Nav bar**: A `<rect>` with the screen title as `<text>`
4. **Content elements**: Stacked `<rect>` placeholders based on the screen `type`
5. **Interactive buttons**: Dark blue `<rect>` (`#013D5B`) with white `<text>` for clickable elements
6. **Screen name**: `<text>` below the frame

#### Positioning

Use a grid layout for screen positions:

```javascript
const SCREEN_W = 160;  // mobile width
const SCREEN_H = 280;  // mobile height
const H_SPACING = 380; // horizontal between screens
const V_SPACING = 400; // vertical for branches

// Position screens in a left-to-right flow
// Main path: screens at y=0, increasing x
// Branches: offset y by ±V_SPACING
screens.forEach((screen, i) => {
  screen.x = 80 + i * H_SPACING;
  screen.y = 200;  // center row, adjust for branches
});
```

#### Connector Rendering

```javascript
function drawConnector(source, target, actionLabel) {
  // Calculate exit/entry points on screen edges
  const exitX = source.x + SCREEN_W;
  const exitY = source.y + SCREEN_H / 2;
  const entryX = target.x;
  const entryY = target.y + SCREEN_H / 2;

  // Midpoint for action pill
  const midX = (exitX + entryX) / 2;
  const midY = (exitY + entryY) / 2;

  // Draw orthogonal path
  const path = `M ${exitX},${exitY} H ${midX} V ${entryY} H ${entryX}`;

  // Render line, port circles, and action pill
  container.append('path')
    .attr('d', path)
    .attr('stroke', '#013D5B')
    .attr('stroke-width', 2)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrowhead)');

  // Port circles
  container.append('circle')
    .attr('cx', exitX).attr('cy', exitY)
    .attr('r', 5).attr('fill', '#013D5B')
    .attr('stroke', 'white').attr('stroke-width', 2);

  // Action pill at midpoint
  const pillG = container.append('g')
    .attr('transform', `translate(${midX}, ${midY})`);

  const textWidth = actionLabel.length * 6.5 + 24;
  pillG.append('rect')
    .attr('x', -textWidth/2).attr('y', -12)
    .attr('width', textWidth).attr('height', 24)
    .attr('rx', 12)
    .attr('fill', '#013D5B');

  pillG.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '0.35em')
    .attr('fill', 'white')
    .attr('font-size', '11px')
    .attr('font-weight', '500')
    .text(actionLabel);
}
```

## Multi-Path Flows (Happy Path + Error States)

When a screen flow includes multiple path types (happy path, error states, back-loops), additional routing and collision avoidance is required. Without it, connector lines overlap, pill labels stack on top of each other, and labels land on top of screens from other rows.

### Screen Types & Layers

Extend the screen data with `type` and `layer` properties:

```javascript
// Screen types control color
const COLORS = {
  screen:   { bg:'#FFFFFF', border:'#C8C3BA', accent:'#013D5B' },
  decision: { bg:'#FFFDF5', border:'#D4A800', accent:'#7A6200' },
  error:    { bg:'#FFFAFA', border:'#EF9A9A', accent:'#C62828' },
  success:  { bg:'#FBFDF7', border:'#A5D6A7', accent:'#2E7D32' }
};

// Layers control toggle visibility
// layer: 'happy' | 'error'
```

### Connector Styles by Action Type

Different action types get distinct visual styles:

```javascript
function connStyle(action) {
  const a = action.toLowerCase();
  if (a.includes('fail') || a.includes('error') || a.includes('denied'))
    return {c:'#C62828', d:'6,3', m:'url(#arr-err)'};     // red dashed
  if (a.includes('success') || a.includes('continue') || a.includes('save'))
    return {c:'#558B2F', d:'none', m:'url(#arr-ok)'};      // green solid
  if (a.includes('back') || a.includes('cancel') || a.includes('retry'))
    return {c:'#B0ABA2', d:'4,3', m:'url(#arr-back)'};     // gray dashed
  return {c:'#013D5B', d:'none', m:'url(#arr)'};            // blue solid (default)
}
```

### Safe Gutter Routing

When connectors cross between rows (e.g., happy path row → error path row), vertical segments must run through **column gutters** — the space between screens where no screen exists at any row.

```javascript
const COL_W = SW + 200;  // column spacing (screen width + gutter)
const ROW_H = SH + 260;  // row spacing (screen height + label/connector space)

function col(n) { return 100 + n * COL_W; }
function row(n) { return 100 + n * ROW_H; }

// Compute safe vertical corridors centered between each pair of columns
const SAFE_GUTTERS_X = [];
for (let i = 0; i < maxCols; i++)
  SAFE_GUTTERS_X.push(col(i) + SW + (COL_W - SW) / 2);
SAFE_GUTTERS_X.unshift(col(0) - (COL_W - SW) / 2); // left edge gutter

function nearestSafeGutterX(x) {
  return SAFE_GUTTERS_X.reduce((best, gx) =>
    Math.abs(x - gx) < Math.abs(x - best) ? gx : best
  );
}
```

### Lane Offsets per Connector Type

When multiple connector types share the same gutter, they must run in **distinct parallel lanes** so each is independently traceable. Assign a perpendicular offset based on the connector style:

```javascript
function laneOffset(style) {
  if (style.c === '#013D5B') return 0;      // primary (blue)
  if (style.c === '#558B2F') return -16;     // success (green)
  if (style.c === '#C62828') return 16;      // error (red)
  if (style.c === '#B0ABA2') return 32;      // back/retry (gray)
  return 0;
}
```

Apply the offset to:
1. **Gutter X positions** — shift the vertical segment in column gutters by `off`
2. **Top-loop Y positions** — shift the over-the-top back-loop height by `off`
3. **Exit/entry port positions** — shift ports perpendicular to the edge by `off * 0.6`

```javascript
// In buildPath(), apply offset to gutter routing:
if (es === 'bottom' && en === 'top') {
  const gx = nearestSafeGutterX((a.x + b.x) / 2) + off;
  return `M${a.x},${a.y} V${a.y+30} H${gx} V${b.y-30} H${b.x} V${b.y}`;
}

// For back-loops over the top:
if (es === 'top' && en === 'top') {
  const topY = Math.min(a.y, b.y) - 70 + off;
  return `M${a.x},${a.y} V${topY} H${b.x} V${b.y}`;
}

// Offset exit/entry ports so parallel connectors don't share the same pixel:
if (route.exit === 'top' || route.exit === 'bottom') a.x += off * 0.6;
if (route.exit === 'left' || route.exit === 'right') a.y += off * 0.6;
```

### Explicit Routing Table

For complex flows, define an explicit routing table instead of auto-computing exit/entry sides:

```javascript
const ROUTES = {
  'list->add-conn':           {exit:'right', enter:'left'},    // same-row horizontal
  'add-conn->list':           {exit:'top',   enter:'top'},     // back-loop over top
  'test-decision->err-auth':  {exit:'bottom', enter:'top'},    // cross-row down
  'err-auth->test-decision':  {exit:'top',   enter:'bottom'},  // cross-row back up
};
```

### Three-Layer Rendering Order

Render in three passes to ensure correct z-ordering:

```javascript
drawConnectors();                               // 1. Lines & dots (bottom)
screens.forEach(s => drawScreen(screenLayer, s)); // 2. Screen wireframes (middle)
drawPillsLayer();                                // 3. Action pill labels (top)
```

This ensures:
- Connectors are always behind screens (never visually "on top of" a screen)
- Pill labels are always in front of everything (legible on top of lines AND screens)

### Smart Pill Placement (Avoid Screen Overlap)

Pills are placed on connector paths. When a connector spans multiple rows, its midpoint may land on a screen from another row. The pill placement function tries every segment of the path and picks the first position that doesn't overlap any screen:

```javascript
function getPillPosition(pathStr, a, b, labelText) {
  const segs = parsePathSegments(pathStr);
  const screenBoxes = screens.map(s => ({x:s.x, y:s.y, w:SW, h:SH+40}));
  const pillW = (labelText||'').length * 5 + 28;

  function overlapsAnyScreen(px, py) {
    return screenBoxes.some(box =>
      px - pillW/2 < box.x + box.w + 8 && px + pillW/2 > box.x - 8 &&
      py - 12 < box.y + box.h + 8 && py + 12 > box.y - 8
    );
  }

  // Try midpoint of each segment, longest first
  const sorted = [...segs].sort((a,b) => b.len - a.len);
  for (const seg of sorted) {
    const mx = (seg.x1+seg.x2)/2, my = (seg.y1+seg.y2)/2;
    if (!overlapsAnyScreen(mx, my)) return {x:mx, y:my};
  }
  // Try quarter-points as fallback
  for (const seg of sorted) {
    for (const t of [0.25, 0.75, 0.15, 0.85]) {
      const px = seg.x1+(seg.x2-seg.x1)*t, py = seg.y1+(seg.y2-seg.y1)*t;
      if (!overlapsAnyScreen(px, py)) return {x:px, y:py};
    }
  }
  // Last resort: longest segment midpoint
  return {x:(sorted[0].x1+sorted[0].x2)/2, y:(sorted[0].y1+sorted[0].y2)/2};
}
```

### Pill Collision Resolution

After computing all pill positions, run a multi-pass collision resolver to separate overlapping pills into distinct vertical lanes:

```javascript
function resolvePillCollisions(pendingPills, screens) {
  const pillH = 22;
  function pillW(p) { return p.label.length * 5 + 18; }

  // Push overlapping pills apart (up to 8 passes for cascading)
  for (let pass = 0; pass < 8; pass++) {
    let moved = false;
    for (let i = 0; i < pendingPills.length; i++) {
      for (let j = i+1; j < pendingPills.length; j++) {
        const pi = pendingPills[i], pj = pendingPills[j];
        const overlapX = (pillW(pi)+pillW(pj))/2 + 6 - Math.abs(pi.x-pj.x);
        const overlapY = pillH + 4 - Math.abs(pi.y-pj.y);
        if (overlapX > 0 && overlapY > 0) {
          const shift = (pillH + 6) / 2;
          if (pi.y <= pj.y) { pi.y -= shift; pj.y += shift; }
          else { pi.y += shift; pj.y -= shift; }
          moved = true;
        }
      }
    }
    if (!moved) break;
  }

  // Second pass: push any pills that were shifted onto screens
  const screenBoxes = screens.map(s => ({x:s.x, y:s.y, w:SW, h:SH+40}));
  pendingPills.forEach(p => {
    const pw = pillW(p);
    for (const box of screenBoxes) {
      if (p.x-pw/2 < box.x+box.w+8 && p.x+pw/2 > box.x-8 &&
          p.y-pillH/2 < box.y+box.h+8 && p.y+pillH/2 > box.y-8) {
        const above = Math.abs(p.y - (box.y - pillH/2 - 10));
        const below = Math.abs(p.y - (box.y + box.h + pillH/2 + 10));
        p.y = above < below ? box.y - pillH/2 - 10 : box.y + box.h + pillH/2 + 10;
      }
    }
  });
}
```

### Layer Toggle

Allow toggling happy path and error paths independently:

```javascript
const layerOn = {happy: true, error: true};
function toggleLayer(l) {
  layerOn[l] = !layerOn[l];
  container.selectAll('.screen-group').each(function() {
    const d = d3.select(this).datum();
    d3.select(this).transition().duration(200)
      .style('opacity', layerOn[d.layer] ? 1 : 0.06)
      .style('pointer-events', layerOn[d.layer] ? 'all' : 'none');
  });
  container.selectAll('.connector-group').each(function() {
    const d = d3.select(this).datum();
    d3.select(this).transition().duration(200)
      .style('opacity', layerOn[d.layer] ? 1 : 0.04);
  });
}
```

### Critical Setup (Same as Flow Diagram)

Use the exact same D3 zoom + fitToContent pattern. All screen nodes must be placed at **positive coordinates** starting from (0,0). Call `fitToContent()` after rendering to ensure everything is visible.

```javascript
const svg = d3.select('#flow-svg')
  .attr('width', width)
  .attr('height', height);

const container = svg.append('g');

const zoom = d3.zoom()
  .scaleExtent([0.15, 3])
  .on('zoom', (event) => container.attr('transform', event.transform));

svg.call(zoom);

// fitToContent() — same implementation as flow diagram skill
```

## Accepting Flow Content from the User

Users may provide screen flow content as:

- **A list of screens with navigation paths** (most common)
- **A verbal description** of the app flow ("first the user sees a login page, then...")
- **A Mermaid diagram** to convert into visual screen mockups
- **An existing wireframe or sitemap** to connect with flow arrows

When interpreting the content:
- Identify individual screens and their types (list, form, detail, etc.)
- Extract the user actions that cause navigation ("click", "tap", "submit", "swipe")
- Determine the primary (happy) path vs. alternative paths
- Infer screen content types from context (e.g., "product listing" → list type, "checkout form" → form type)

## Iteration Prompts

| User says | What to do |
|-----------|-----------|
| "add a new screen" | Add a new screen mockup to the flow |
| "show the back navigation" | Add "Go Back" connectors for reverse navigation |
| "make it desktop" | Switch screen dimensions to landscape/desktop proportions |
| "add error screens" | Add red-tinted error/failure screen mockups with error path connectors. Use multi-path routing: safe gutter routing, lane offsets, pill collision resolution, three-layer rendering, and layer toggle buttons |
| "highlight the happy path" | Thicken and brighten the primary path connectors |
| "separate the arrow paths" | Apply lane offsets so each connector type (primary, success, error, back) runs in a distinct parallel lane through shared gutters |
| "labels are overlapping" | Run pill collision resolution: check pill-vs-screen and pill-vs-pill overlaps, shift pills to safe positions using smart placement + multi-pass resolver |
| "include happy and error paths" | Build full multi-path flow with three-layer rendering (connectors → screens → pills), safe gutter routing, lane offsets per type, pill collision resolution, and layer toggle UI |
| "add screen details" | Flesh out the wireframe content inside screen mockups |
| "show modals" | Add modal/dialog overlays as smaller screens connected from triggers |
| "add annotations" | Add text callouts explaining design decisions |
| "switch to dark mode" | Swap to SDS dark mode: canvas `#0E1012` (cool-gray-950), screens `#1F2326` (cool-gray-850), borders `#34383D` (cool-gray-750), text `#F8F8F9` (cool-gray-025) |

## Serving the Screen Flow

After building the HTML file, serve it using the project's dev server configuration. Save the file in the user's project directory and ensure `launch.json` is configured to serve it. Open it in the browser for the user to interact with.

## Next Steps

After building the screen flow, suggest:
- "Want me to add more detail to the wireframe content inside each screen?"
- "Should I add back-navigation and error paths?"
- "Want a companion journey map showing the emotional experience across this flow?"
- "Should I convert this to a more abstract flow diagram for the engineering spec?"
