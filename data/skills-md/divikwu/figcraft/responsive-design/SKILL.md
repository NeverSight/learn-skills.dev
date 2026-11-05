---
name: responsive-design
description: "Responsive web design rules — breakpoints, auto-layout strategy, sizing patterns. Use when: responsive/breakpoint/mobile/tablet/desktop + design/layout/screen, or when creating multi-breakpoint web designs."
---

# Responsive Design — Web Breakpoint Rules

Rules and patterns for creating responsive web designs in Figma across mobile, tablet, and desktop breakpoints. Covers auto-layout strategy, sizing patterns, and common pitfalls.

## Skill Boundaries

- Use this skill for **responsive web layout decisions** (breakpoints, column grids, sizing).
- If the task is **iOS-specific design** (safe areas, HIG), switch to [platform-ios](../platform-ios/SKILL.md).
- If the task is **Android-specific design** (Material, 48dp), switch to [platform-android](../platform-android/SKILL.md).
- If the task is **creating UI**, switch to [figma-create-ui](../figma-create-ui/SKILL.md) and reference this skill for responsive rules.

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

## On-Demand Guide

For the full responsive layout reference at runtime:

```
get_creation_guide(topic: "responsive")
```

## Breakpoints

| Breakpoint | Width | Columns | Padding |
|-----------|-------|---------|---------|
| Mobile | 375px | 1 | 16px |
| Tablet | 768px | 2 | 24px |
| Desktop | 1280px | 3–4 | 32–64px |

## Auto-Layout Strategy

- Mobile: VERTICAL stack, 1 column, FILL width children
- Tablet: mix HORIZONTAL rows (2-col) + VERTICAL sections
- Desktop: HORIZONTAL main layout with sidebar + content area

## Sizing Patterns

| Context | Horizontal | Vertical |
|---------|-----------|----------|
| Page container | FIXED (breakpoint width) | HUG |
| Content area | FILL | HUG |
| Sidebar | FIXED (240–300px) | FILL |
| Cards in grid | layoutGrow: 1 (equal width) | HUG |
| Full-width sections | FILL | HUG |

## Key Rules

- NEVER use fixed pixel widths for content children at mobile — use FILL
- SHOULD use maxWidth constraints for text readability (600–800px at desktop)
- Breakpoint frames are FIXED width; their children adapt via FILL/HUG
- Cards: use layoutGrow: 1 in HORIZONTAL rows for equal distribution
- Navigation: HORIZONTAL on desktop, bottom tab bar on mobile

## Workflow for Multi-Breakpoint Designs

### Step 1: Create Breakpoint Frames

Build one frame per breakpoint, side by side:

```
create_frame (wrapper, HORIZONTAL, itemSpacing: 40, clipsContent: false)
  ├── Mobile frame (375 × HUG)
  ├── Tablet frame (768 × HUG)
  └── Desktop frame (1280 × HUG)
```

### Step 2: Build Mobile First

Design the mobile layout first — it forces content prioritization.

### Step 3: Adapt to Tablet

Expand to 2-column layouts where appropriate. Keep single-column for forms and focused content.

### Step 4: Adapt to Desktop

Add sidebar navigation, expand grids to 3–4 columns, increase padding.

### Step 5: Verify

Use `verify_design` on each breakpoint frame to check for overflow and layout issues.
