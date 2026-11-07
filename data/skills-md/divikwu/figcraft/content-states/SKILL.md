---
name: content-states
description: "Design patterns for empty, loading, and error states. Use when: empty state/loading/skeleton/error/no data + design/screen/component, or when ensuring data-driven views handle all states."
---

# Content States — Empty, Loading, Error Patterns

Design patterns for the three critical content states every data-driven view must handle: empty, loading (skeleton), and error. Ensures no view is left without guidance when data is absent or unavailable.

## Skill Boundaries

- Use this skill for **content state design patterns** (empty, loading, error).
- If the task is **creating the full UI**, switch to [figma-create-ui](../figma-create-ui/SKILL.md) and reference this skill for state patterns.
- If the task is **reviewing existing designs for missing states**, switch to [design-review](../design-review/SKILL.md).

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

## On-Demand Guide

For the full content states reference at runtime:

```
get_creation_guide(topic: "content-states")
```

## Empty State

```
Container (VERTICAL, FILL/HUG, counterAxisAlignItems: CENTER, padding: 40–60)
  ├── Illustration (120–160px, subtle fill or SVG)
  ├── Heading ("No items yet" / "Get started") — 20px, semibold
  ├── Body ("Add your first item to see it here") — 14–16px, muted
  └── CTA Button ("Add Item") — primary style
```

Rules:
- Center vertically and horizontally in container
- Use encouraging, action-oriented language (not error language)
- CTA should directly trigger the creation action
- NEVER leave a list/grid container with zero children and no empty state

## Loading State (Skeleton)

```
Same structure as loaded state, but:
  ├── Text → gray rectangles (cornerRadius: 4, fill: gray-200, height matching line-height)
  ├── Images → gray rectangles (same dimensions, fill: gray-100)
  ├── Avatar → gray circle (same size)
  └── All skeleton elements: no stroke, uniform gray palette
```

Rules:
- Match the loaded layout exactly — skeleton IS the layout with gray placeholders
- NEVER use a centered spinner for content with a known layout
- Spinner only for indeterminate operations (file upload, search)

## Error State

```
Container (VERTICAL, FILL/HUG, counterAxisAlignItems: CENTER, padding: 40–60)
  ├── Error icon (48–64px, warning/error color)
  ├── Heading ("Something went wrong") — 20px, semibold
  ├── Body ("We couldn't load your data. Please try again.") — 14–16px, muted
  └── Retry Button ("Try Again") — secondary or outline style
```

Rules:
- Use neutral, non-blaming language
- Always provide a retry action
- Don't use red for the entire error state — red for icon/accent only

## Workflow

When designing a data-driven view:

1. Design the loaded state first (primary content)
2. Create the empty state variant (no data yet)
3. Create the loading state (skeleton matching loaded layout)
4. Create the error state (recovery-focused)
5. Verify all four states fit within the same container dimensions
