---
name: bootstrap5-ui
description: Production-grade Bootstrap 5.3 patterns for building modern, responsive web UIs in HTML and ASP.NET Core Razor Pages/Views. Use when creating or styling web pages, layouts, navigation, forms, cards, modals, tables, or any UI component with Bootstrap 5. Covers the grid system, responsive breakpoints, utility classes, color modes (dark/light), accessibility, and integration with ASP.NET Core tag helpers and Razor syntax. Trigger on any task involving Bootstrap CSS classes, responsive HTML layouts, Razor Page UI design, or front-end styling for .NET web applications.
---

# Bootstrap 5 UI

Production patterns for building responsive, accessible web UIs with Bootstrap 5.3 in HTML and ASP.NET Core Razor Pages/Views. Target Bootstrap 5.3.x (current CDN: 5.3.8). Bootstrap 5 dropped jQuery dependency entirely.

## Setup in ASP.NET Core

### CDN (Quick Start)

In `_Layout.cshtml` or `_Host.cshtml`:

```html
<!-- In <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous">

<!-- Before closing </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
        crossorigin="anonymous"></script>
```

### LibMan (Recommended for Production)

```json
// libman.json
{
  "version": "1.0",
  "defaultProvider": "jsdelivr",
  "libraries": [
    {
      "library": "bootstrap@5.3.8",
      "destination": "wwwroot/lib/bootstrap/"
    }
  ]
}
```

Reference locally in layout:
```html
<link rel="stylesheet" href="~/lib/bootstrap/dist/css/bootstrap.min.css" />
<script src="~/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
```

### Required Globals

Always include in `<head>`:
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
```

## Grid System

Bootstrap uses a 12-column flexbox grid with 6 responsive breakpoints:

| Breakpoint | Prefix | Min-width |
|------------|--------|-----------|
| Extra small | `.col-` | <576px |
| Small | `.col-sm-` | >=576px |
| Medium | `.col-md-` | >=768px |
| Large | `.col-lg-` | >=992px |
| Extra large | `.col-xl-` | >=1200px |
| XXL | `.col-xxl-` | >=1400px |

### Core Pattern

```html
<div class="container">
  <div class="row">
    <div class="col-md-8">Main content</div>
    <div class="col-md-4">Sidebar</div>
  </div>
</div>
```

### Key Rules
- Always wrap columns in `.row` inside a `.container` (or `.container-fluid` for full-width)
- Columns must be direct children of rows
- Use `.g-*` classes for gutters (`.g-0` removes gutters, `.gx-*` horizontal, `.gy-*` vertical)
- Use `.row-cols-*` on the row for uniform column counts: `<div class="row row-cols-1 row-cols-md-3 g-4">`
- Mix breakpoints: `<div class="col-6 col-md-4 col-lg-3">` — stacks to 2-up on xs, 3-up on md, 4-up on lg

### Container Types
- `.container` — responsive fixed-width
- `.container-fluid` — full-width always
- `.container-{breakpoint}` — fluid until breakpoint, then fixed

## Spacing Utilities

Format: `{property}{sides}-{breakpoint}-{size}`

**Property:** `m` (margin), `p` (padding)
**Sides:** `t` top, `b` bottom, `s` start(left), `e` end(right), `x` horizontal, `y` vertical, blank = all
**Size:** `0`=0, `1`=0.25rem, `2`=0.5rem, `3`=1rem, `4`=1.5rem, `5`=3rem, `auto`

```html
<div class="mt-3 mb-4 px-2">Spaced element</div>
<div class="mx-auto" style="width: 200px;">Centered block</div>
<div class="py-md-5">Padding only on md+</div>
```

## Color Modes (Dark/Light)

Bootstrap 5.3 supports `data-bs-theme` attribute for dark mode:

```html
<!-- Global dark mode -->
<html lang="en" data-bs-theme="dark">

<!-- Per-component -->
<div class="card" data-bs-theme="dark">...</div>
<nav class="navbar bg-dark" data-bs-theme="dark">...</nav>
```

Use semantic color classes that adapt to color mode:
- `bg-body`, `bg-body-secondary`, `bg-body-tertiary` — adapt to theme
- `text-body`, `text-body-secondary`, `text-body-emphasis` — adapt to theme
- `border-body` — adapts to theme

**Avoid hardcoded colors.** Use `bg-body-tertiary` instead of `bg-light` for theme-aware backgrounds.

## Common Component Patterns

### Navbar

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Brand</a>
    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse" data-bs-target="#mainNav"
            aria-controls="mainNav" aria-expanded="false"
            aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">About</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### Cards in Grid

```html
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">
    <div class="card h-100">
      <img src="..." class="card-img-top" alt="...">
      <div class="card-body">
        <h5 class="card-title">Title</h5>
        <p class="card-text">Description text.</p>
        <a href="#" class="btn btn-primary">Action</a>
      </div>
    </div>
  </div>
  <!-- repeat -->
</div>
```

### Forms

```html
<form method="post">
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email">
  </div>
  <div class="mb-3">
    <label for="password" class="form-label">Password</label>
    <input type="password" class="form-control" id="password">
  </div>
  <div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="remember">
    <label class="form-check-label" for="remember">Remember me</label>
  </div>
  <button type="submit" class="btn btn-primary">Sign in</button>
</form>
```

### Floating Labels

```html
<div class="form-floating mb-3">
  <input type="email" class="form-control" id="floatEmail" placeholder="name@example.com">
  <label for="floatEmail">Email address</label>
</div>
```

### Responsive Table

```html
<div class="table-responsive">
  <table class="table table-striped table-hover">
    <thead class="table-dark">
      <tr><th>Name</th><th>Email</th><th>Actions</th></tr>
    </thead>
    <tbody>
      <tr><td>John</td><td>john@example.com</td><td><a class="btn btn-sm btn-outline-primary">Edit</a></td></tr>
    </tbody>
  </table>
</div>
```

## Razor Pages Integration

For detailed ASP.NET Core Razor Pages integration patterns including tag helpers, validation, layouts, and partial views, see [references/razor-integration.md](references/razor-integration.md).

Key points:
- Use `asp-for`, `asp-page`, `asp-action` tag helpers with Bootstrap classes
- Combine `asp-validation-for` with `.invalid-feedback` / `.is-invalid` classes
- Place Bootstrap validation classes via jQuery Validation Unobtrusive or custom JS
- Use `@section Scripts` for page-specific scripts in layout

## Component Reference

For complete component patterns (modals, alerts, toasts, accordion, pagination, breadcrumbs, badges, offcanvas, spinners, progress bars), see [references/components.md](references/components.md).

## Utility Classes Quick Reference

### Display
`d-none`, `d-block`, `d-flex`, `d-grid`, `d-inline`, `d-inline-block`
Responsive: `d-md-none`, `d-lg-flex`

### Flexbox
`justify-content-{start|center|end|between|around|evenly}`
`align-items-{start|center|end|stretch}`
`flex-{row|column}`, `flex-wrap`, `flex-grow-1`

### Text
`text-{start|center|end}`, `text-{lowercase|uppercase|capitalize}`
`fw-{bold|semibold|normal|light}`, `fs-{1-6}`
`text-truncate`, `text-nowrap`, `text-break`

### Colors
`text-{primary|secondary|success|danger|warning|info|light|dark}`
`bg-{primary|secondary|success|danger|warning|info|light|dark}`
`text-bg-{color}` — sets matching text+bg together

### Borders & Shadows
`border`, `border-{top|bottom|start|end}`, `border-{color}`, `border-{1-5}`
`rounded`, `rounded-{0-5|circle|pill}`
`shadow`, `shadow-sm`, `shadow-lg`, `shadow-none`

### Sizing
`w-{25|50|75|100|auto}`, `h-{25|50|75|100|auto}`
`mw-100`, `mh-100`, `vw-100`, `vh-100`
`min-vw-100`, `min-vh-100`

### Position
`position-{static|relative|absolute|fixed|sticky}`
`top-{0|50|100}`, `start-{0|50|100}`, `translate-middle`

## Accessibility Requirements

- Always include `aria-label` on icon-only buttons and togglers
- Use `aria-current="page"` on active nav links
- Use `aria-expanded` on collapse/dropdown triggers
- Provide `alt` text on images; use `.visually-hidden` for screen-reader-only text
- Ensure color contrast meets WCAG 2.1 AA (4.5:1 for text, 3:1 for large text)
- Use semantic HTML: `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>`
- Never remove `:focus` styles; use Bootstrap's `.focus-ring` utility for custom focus

## Anti-Patterns

- Using `col-*` without a parent `.row` — breaks grid alignment
- Nesting containers — only nest rows, never containers inside containers
- Using `<br>` and inline styles for spacing — use spacing utilities (`mt-3`, `mb-4`)
- Hardcoding `bg-light`/`bg-dark` — use `bg-body-tertiary` for theme-aware backgrounds
- Forgetting `navbar-expand-{breakpoint}` — navbar won't collapse responsively
- Mixing Bootstrap 4 classes (e.g., `ml-3`, `mr-3`) — use `ms-3`, `me-3` (start/end logical properties)
- Omitting `type="button"` on non-submit buttons in forms — causes unintended form submission
- Using `<a>` for actions without `href` — use `<button>` for actions, `<a>` for navigation
- Skipping `.form-label` on form inputs — hurts accessibility
- Not wrapping tables in `.table-responsive` — causes horizontal overflow on mobile
