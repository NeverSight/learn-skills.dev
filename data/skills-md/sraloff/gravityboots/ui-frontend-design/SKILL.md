---
name: ui-frontend-design
description: Pro-level UI/UX principles, layouts, and aesthetics for Laravel/Antigravity.
---

# UI & Frontend Design (Pro Max)

## When to use this skill
- Designing new pages or components (Blade/React).
- Refactoring UI for "premium" aesthetic.
- Choosing colors, typography, or spacing.

## 1. Core Visual Principles
- **Layouts**: Mobile-first always. Use **Bento Grids** for dashboards and data density.
- **Layers & Depth**: Use a consistent Z-Index scale (10, 20, 30, 40, 50).
- **Styles**: Experiment with Glassmorphism (layered transparency) and Neo-Brutalism (high contrast borders) where appropriate.

## 2. Spacing & Touch
- **Touch Targets**: Minimum 44x44px for ALL interactive elements (mobile access).
- **Tailwind**: Use logical increments (`p-4`, `m-2`). Avoid arbitrary values unless absolutely necessary.
- **Line Length**: Limit text width to 65-75 characters for readability (`prose` or `max-w-prose`).

## 3. Colors & Typography
- **Palettes**:
  - **SaaS**: Primary Blue (`#2563EB`).
  - **Creative**: Indigo/Violet (`#6366F1`).
  - **Commerce**: Emerald (`#059669`).
- **Contrast**: Strict 4.5:1 ratio for text. Visible focus rings for keyboard users.
- **Typography**:
  - Headings: *Inter*, *Poppins*, or *Space Grotesk*.
  - Body: *Inter*, *Open Sans*, or *DM Sans*.
  - Line Height: 1.5 - 1.75 for body text.

## 4. Laravel/Blade Strategies
- **Components**: Wrap UI patterns in Blade Components (`<x-card>`, `<x-button>`) to enforce consistency.
- **Animations**: Use `@push('scripts')` or Alpine.js for micro-interactions (150ms-300ms duration).
- **Theme**: Extend `tailwind.config.js` with semantic names (`bg-primary`, `text-on-primary`) instead of raw colors.
