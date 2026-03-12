---
name: baseline-ui
description: Output the project design system reference — colors, typography, spacing, component patterns. Invoke when discussing visual consistency, design tokens, or referencing the style guide.
user-invocable: true
---

# Baseline UI — Design System Reference

When invoked, read and reference these canonical source files before answering any design question:

- `frontend/src/styles/global.css` — design tokens (CSS custom properties)
- `frontend/src/styles/responsive.css` — breakpoints, accessibility rules
- `frontend/src/components/Layout/AdminLayout.tsx` — admin shell layout

---

## Color Palette (CSS Custom Properties)

| Token | Value | Usage |
|---|---|---|
| `--color-primary` | `#1a365d` | Navy — headings, primary buttons, brand |
| `--color-primary-light` | `#2b6cb0` | Links, hover states, focus outlines |
| `--color-secondary` | `#e53e3e` | Red — CTAs, warnings, destructive actions |
| `--color-accent` | `#38a169` | Green — success states, positive indicators |
| `--color-bg` | `#ffffff` | Page background |
| `--color-bg-alt` | `#f7fafc` | Alternate section backgrounds |
| `--color-text` | `#2d3748` | Body text |
| `--color-text-light` | `#718096` | Muted/secondary text |
| `--color-border` | `#e2e8f0` | Card borders, dividers |

**Rule**: Never hardcode hex values. Always use `var(--color-*)` in CSS or reference Bootstrap utility classes that map to these values.

---

## Typography

- **Font stack**: `'Segoe UI', system-ui, -apple-system, sans-serif`
- **Headings**: `font-weight: 700`, `line-height: 1.2`, `color: var(--color-primary)`
- **Body**: `line-height: 1.6`, `color: var(--color-text)`
- **Links**: `color: var(--color-primary-light)`, underline on hover

---

## Spacing & Layout

- **Max width**: `--max-width: 1200px`
- **Section padding**: `4rem 0` (desktop), `2.5rem 0` (mobile), `3rem 0` (tablet)
- **Container**: `max-width: var(--max-width)`, `padding: 0 1rem`
- **Admin shell**: Dark navbar (`navbar-dark bg-dark`), `bg-light` main area, `container py-4` content wrapper

---

## Bootstrap 5 Component Patterns

These are the canonical patterns used throughout the admin UI:

### Cards
```html
<div class="card border-0 shadow-sm mb-4">
  <div class="card-header bg-white fw-semibold">Title</div>
  <div class="card-body">Content</div>
</div>
```

### KPI Stat Cards
```html
<div class="col-md-3">
  <div class="card border-0 shadow-sm">
    <div class="card-body text-center p-3">
      <div class="fs-4 fw-bold text-primary">42</div>
      <div class="text-muted small">Metric Label</div>
    </div>
  </div>
</div>
```

### Data Tables
```html
<div class="table-responsive">
  <table class="table table-hover mb-0">
    <thead class="table-light">...</thead>
    <tbody>...</tbody>
  </table>
</div>
```

### Tab Navigation
```html
<ul class="nav nav-tabs mb-4">
  <li class="nav-item">
    <button class="nav-link active" onClick={...}>Tab Label</button>
  </li>
</ul>
```

### Badges
```html
<span class="badge bg-success">active</span>
<span class="badge bg-warning">paused</span>
<span class="badge bg-info">completed</span>
<span class="badge bg-secondary">draft</span>
<span class="badge bg-danger">TEST MODE</span>
```

### Filter Bars
```html
<div class="d-flex gap-2 mb-3 flex-wrap align-items-center">
  <input class="form-control form-control-sm" style="max-width: 250px" placeholder="Search..." />
  <select class="form-select form-select-sm" style="max-width: 150px">...</select>
  <div class="ms-auto d-flex gap-2">
    <button class="btn btn-outline-primary btn-sm">Action</button>
  </div>
</div>
```

### Buttons
```html
<button class="btn btn-primary btn-sm">Primary</button>
<button class="btn btn-outline-secondary btn-sm">Secondary</button>
<button class="btn btn-outline-danger btn-sm">Danger</button>
<button class="btn btn-success btn-sm">Success</button>
```

### Form Controls
```html
<label class="form-label small fw-medium">Label</label>
<input class="form-control form-control-sm" />
<div class="form-text">Helper text</div>

<!-- Toggle switch -->
<div class="form-check form-switch">
  <input class="form-check-input" type="checkbox" id="sw-id" />
  <label class="form-check-label small" for="sw-id">
    <span class="fw-medium">Title</span><br />
    <span class="text-muted">Description</span>
  </label>
</div>
```

### Modal Overlays
```html
<div class="modal show d-block" style="backgroundColor: 'rgba(0,0,0,0.5)'">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Title</h5>
        <button class="btn-close" onClick={onClose} />
      </div>
      <div class="modal-body" style="max-height: 500px; overflow: auto">...</div>
      <div class="modal-footer">...</div>
    </div>
  </div>
</div>
```

---

## Custom CSS Classes (from global.css)

| Class | Purpose |
|---|---|
| `.card-lift` | Hover: translateY(-4px) + deeper shadow |
| `.fade-in-section` | Scroll-triggered fade + slide-up animation |
| `.badge-label` | Small-caps uppercase label badge |
| `.agent-card` | Bordered card with hover lift for agent/feature cards |
| `.callout-box` | Left-bordered gradient callout for emphasis |
| `.timeline-horizontal` | Horizontal step timeline |
| `.skip-nav` | Skip navigation link for accessibility |
| `.hero-bg` | Hero section with gradient overlay |
| `.btn-accent` | Secondary red CTA button |

---

## Responsive Breakpoints

| Breakpoint | Range | Key adjustments |
|---|---|---|
| Mobile | `< 576px` | Smaller headings, reduced padding, stacked layouts |
| Tablet | `576px – 992px` | Medium headings, intermediate padding |
| Desktop | `> 992px` | Full layout, default spacing |
| Touch targets | `< 992px` | Min 44px height/width on buttons, inputs, links |
| iOS zoom prevention | `< 992px` | `font-size: 16px` on form controls |

---

## Accessibility Patterns

- **Focus**: `outline: 3px solid var(--color-primary-light)`, `outline-offset: 2px` on `:focus-visible`
- **Reduced motion**: All animations/transitions → `0.01ms` when `prefers-reduced-motion: reduce`
- **High contrast**: Cards get `2px solid` borders, `.text-muted` becomes full contrast, outline buttons get `2px` borders

---

## Existing Reusable Components

| Component | Path | Usage |
|---|---|---|
| `TemperatureBadge` | `frontend/src/components/TemperatureBadge.tsx` | Color-coded lead temperature pill (cold/cool/warm/hot/qualified) |
| `LeadDetailModal` | `frontend/src/components/campaign/LeadDetailModal.tsx` | Per-lead drill-down with timeline + temperature history |
| `AdminLayout` | `frontend/src/components/Layout/AdminLayout.tsx` | Admin page shell with dark navbar |
