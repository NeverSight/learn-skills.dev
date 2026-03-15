---
name: pos-restaurant-ui-standard
description: Standard Restaurant POS UI derived from the Restaurant POS redesign plan. Use for any restaurant POS screen to enforce the approved layout, components, accessibility, and speed workflow.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

**Frontend Design plugin (`webapp-gui-design`):** MUST be active for all visual output from this skill. Use for design system work, component styling, layout decisions, colour selection, typography, responsive design, and visual QA.

# Restaurant POS UI Standard

Use this skill for any restaurant POS screen. It enforces the approved UI layout, workflow, and accessibility targets from the Restaurant POS redesign plan.

## When to Use

- Building or refactoring restaurant POS screens
- Reviewing restaurant POS UX for speed and clarity
- Standardizing restaurant order entry workflow

## Required Baseline

- Follow the three-level hierarchy (context, order, actions)
- Use large touch targets (>= 56px; 64px preferred)
- Auto-focus search on load
- Quick access lanes (Recent, Favorites, Popular)
- Sticky or floating cart with dominant Pay CTA
- Never generate invoices until Pay is clicked
- WCAG 2.1 AA compliance for all interactive elements

## Canonical Source

The canonical layout and component specs live in:
- [docs/plans/restaurant-pos/2026-02-03-restaurant-pos-ui-redesign.md](../../docs/plans/restaurant-pos/2026-02-03-restaurant-pos-ui-redesign.md)

## References

- [references/restaurant-pos-ui-standard.md](references/restaurant-pos-ui-standard.md)
