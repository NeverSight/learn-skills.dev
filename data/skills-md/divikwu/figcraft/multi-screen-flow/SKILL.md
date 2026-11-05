---
name: multi-screen-flow
description: "Multi-screen flow architecture — wrapper hierarchy, stage containers, step pills, build order. Use when: multi-screen/flow/onboarding/checkout + design/create/build, or when creating 3+ screens in a single task."
---

# Multi-Screen Flow Architecture

Multi-screen flows (login, onboarding, checkout, etc.) MUST use a strict hierarchy. Skipping levels causes layout collapse and missing context.

## Skill Boundaries

- Use this skill for **multi-screen flow structure** (3+ screens in one task).
- If the task is **single screen or single element**, this skill is not needed — use [figma-create-ui](../figma-create-ui/SKILL.md) directly.
- If the task is **responsive breakpoints** (same content at different widths), switch to [responsive-design](../responsive-design/SKILL.md).

## Hierarchy (do not skip levels)

```
Wrapper (VERTICAL, HUG/HUG, counterAxisAlignItems=MIN, clipsContent=false,
         cornerRadius=20-40, fill=lightGray, role:"presentation",
         padding=48, itemSpacing=32)
  ├── Header (VERTICAL, HUG/HUG, itemSpacing=8)
  │     ├── Title (24px, bold)
  │     └── Description (16px, muted)
  └── Flow Row (HORIZONTAL, HUG/HUG, clipsContent=false, itemSpacing=40)
        └── Stage / {label} (VERTICAL, HUG/HUG, clipsContent=false, itemSpacing=16)
              ├── Step Pill (HORIZONTAL, HUG/HUG, cornerRadius=100, fill=dark,
              │              padding 6/14, itemSpacing=6)
              │     ├── Number ("01", accent color, bold, 13px)
              │     └── Label ("登录", white, medium, 13px)
              └── Screen / {label} (VERTICAL, FIXED 402×874, role:"screen",
                                    cornerRadius=28, clipsContent=true, padding,
                                    SPACE_BETWEEN)
                    ├── Top Content (VERTICAL, FILL/FILL)
                    └── Bottom Content (VERTICAL, FILL/HUG)
```

## Build Order

1. **Skeleton first** — `create_frame`: Wrapper + children with full hierarchy (Header + Flow Row + Stages + empty Screens) → check _children in response to confirm structure
2. **Verify layout** — `export_image(scale:0.3)` to confirm all screens are horizontal in Flow Row. Do NOT proceed until this is confirmed.
3. **Fill screens** — `create_frame` per screen (parentId=screenId, children=[TopContent, BottomContent]). Use inline `{type: "icon", icon: "lucide:home", size: 24}` children for icons — do NOT call `icon_search`/`icon_create` separately. Merge Top + Bottom content into a single `create_frame` call per screen.
4. **Fill remaining screens** — one `create_frame` per screen → `export_image` as needed
5. **Lint** — `lint_fix_all` → done

The Opinion Engine automatically handles: sizing inference, FILL ordering, conflict detection, cross-level validation, and failure cleanup. No need to manually handle these Figma API details.

## Key Rules

- ALL ancestor containers of Screen MUST have `clipsContent: false`
- Screen MUST include `role: "screen"` — prevents lint from misidentifying it as button/input based on name
- Screen uses `primaryAxisAlignItems: "SPACE_BETWEEN"` for top/bottom distribution
- Direct child of SPACE_BETWEEN screen MUST declare `layoutSizingVertical: "FILL"` — HUG defeats SPACE_BETWEEN
- Screen dimensions: iOS 402×874, Android 412×915
- Wrapper fill: light gray (#F3F4F6 or similar) to contrast with white screens
- Screen is a page-level container, NOT a card — do not add shadow/elevation
- Use `dryRun: true` when uncertain about parameters

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

## On-Demand Guide

For additional details at runtime:

```
get_creation_guide(topic: "multi-screen")
```
