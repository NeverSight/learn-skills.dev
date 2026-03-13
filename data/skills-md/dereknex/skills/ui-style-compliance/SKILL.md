---
name: ui-style-compliance
description: Use when designing or reviewing UI in React-based frameworks (Next.js, Vite, Remix, Astro) and the task involves checking interface style, interaction, animation, typography, layout, performance, or design constraints for compliance.
---

# UI Style Compliance

## Overview

Apply a strict UI compliance checklist to React-based UI work so outputs match the UI Skills constraints without adding unrequested styling or interaction behavior.

**Priority:** This skill is a compliance gate. When it conflicts with other UI skills (e.g., animation or styling), these rules take precedence.

## Scope

Use this skill for UI design, UI review, or implementation review in Next.js, Vite, Remix, or Astro projects. It is a compliance gate, not a creativity prompt.

## Quick Checklist

1. Confirm stack rules (Tailwind defaults, motion/react, tw-animate-css, cn).
2. Confirm component primitive rules (accessibility, no mixing systems, aria-labels).
3. Confirm interaction rules (AlertDialog, skeletons, h-dvh, safe-area, errors, paste).
4. Confirm animation rules (only when requested, compositor-only, timing, reduced motion).
5. Confirm typography rules (text-balance, text-pretty, tabular-nums, no tracking).
6. Confirm layout rules (fixed z-index scale, size-x for squares).
7. Confirm performance rules (no large blur/backdrop animations, no stray will-change, avoid unnecessary useEffect).
8. Confirm design rules (no gradients unless asked, no purple/multicolor, no glow affordance, empty state CTA, limited accent color).

## Rules by Category

### Stack

- MUST use Tailwind CSS defaults (spacing, radius, shadows) before custom values
- MUST use `motion/react` when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

### Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (Base UI, React Aria, Radix)
- MUST use the project’s existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer Base UI for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

### Interaction

- MUST use an AlertDialog for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in input or textarea elements

### Animation

- NEVER add animation unless explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- MUST respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces

### Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify letter-spacing (`tracking-`) unless explicitly requested

### Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-x`)
- SHOULD use `size-x` for square elements instead of `w-x` + `h-x`

### Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

### Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

## Quick Reference Table

| Area | Hard Stop | Preferred Defaults |
| --- | --- | --- |
| Animation | No unrequested animation; only transform/opacity; <=200ms feedback | ease-out entrances, tw-animate-css | 
| Layout | No `h-screen`, no arbitrary `z-*` | `h-dvh`, fixed z-index scale | 
| Typography | No `tracking-*` without request | `text-balance`, `text-pretty`, `tabular-nums` |
| Design | No gradients unless requested; no purple/multicolor | Tailwind default shadows, 1 accent color |
| Components | No mixing primitives | Use existing primitives, Base UI preferred |

## Example (Single View Audit)

User request: "Design a settings page in Next.js with a subtle animated header and a destructive delete button."

Compliance response:
- Ask whether animation is explicitly required. If not, remove it.
- Use existing component primitives for dialog and inputs.
- Implement destructive action with AlertDialog.
- Use `h-dvh` for full height layout.
- Use `text-balance` for the title and `text-pretty` for descriptions.
- Add `aria-label` for any icon-only buttons.
- Avoid gradients unless the user explicitly asked for them.

## Common Mistakes and Fixes

- "Added a gradient for polish" -> Remove it unless explicitly requested.
- "Used h-screen out of habit" -> Replace with `h-dvh`.
- "Mixed Radix and Headless UI" -> Pick one primitive system per surface.
- "Animated height for accordion" -> Use transform/opacity or remove animation.
- "Added tracking for headings" -> Remove tracking unless requested.

## Rationalization vs Reality

| Rationalization | Reality |
| --- | --- |
| "It looks better with a gradient" | Gradients are forbidden unless requested.
| "The animation is tiny" | Any animation still requires explicit request.
| "h-screen is standard" | The rule is `h-dvh`.
| "Custom easing feels smoother" | Custom easing is forbidden unless requested.
| "I can hack focus behavior quickly" | Use accessible primitives; do not rebuild focus handling.

## Red Flags (Stop and Correct)

- Adding animation without the user explicitly asking
- Using `h-screen` or arbitrary `z-*`
- Mixing primitive systems in a single surface
- Introducing gradients or purple/multicolor accents
- Modifying letter-spacing without a request
- Adding `useEffect` for render-derivable state

## Resources

No external resources required for this skill.
