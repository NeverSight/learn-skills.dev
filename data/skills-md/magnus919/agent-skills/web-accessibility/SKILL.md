---
name: web-accessibility
description: >-
  Design, build, and review accessible web interfaces with native semantics, keyboard and
  focus behavior, forms and recovery, responsive input, motion, assistive-technology
  testing, and WCAG 2.2-informed evidence. Use for a11y, WCAG, ARIA, screen-reader,
  keyboard, focus, dialog, form, widget, or accessibility review work across frameworks.
  Do not use this skill for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Works with any agent framework supporting the Agent Skills format; no runtime dependency.
metadata:
  wcag-status: "W3C Recommendation 2023-10-05"
  aria-version: "WAI-ARIA 1.2"
---

# Web Accessibility

Accessibility is successful task completion and recovery for disabled people, not a tool score. Define observable requirements before implementation, prefer native platform behavior where it fits, and gather bounded evidence in the supported browser and assistive-technology (AT) environment.

## Workflow

1. Define the task, users, supported browsers/AT, input methods, and failure recovery. Start with `assets/acceptance-criteria-template.md`.
2. Choose native HTML first. Load `references/semantics-and-names.md` for structure, native controls, accessible names, descriptions, and dynamic updates.
3. Specify every interactive state: trigger, role/name/state/value, keyboard commands, focus entry/exit/return, pointer alternative, errors, and visible feedback. Load the focused pattern reference.
4. Design for visual and input adaptation using `references/visual-input-and-motion.md`; distinguish WCAG requirements from product goals and exceptions.
5. Implement only after the contract is defined. For custom composite widgets, first evaluate a proven native or maintained component in the chosen stack; APG examples are informative guidance, not production proof.
6. Verify with `references/testing-and-evidence.md` and the design, implementation, and release templates. Record tool, version, scope, manual tasks, actual browser/AT combinations, failures, and blocked or not-applicable items.
7. Do not issue a WCAG conformance or general accessibility verdict from an automated scan. A conformance claim needs a complete, scoped evaluation outside this skill's automatic verdict.

## Load On Demand

| Need | Load |
|---|---|
| Standards status, source authority, or exact links | `references/source-index.md` |
| Native semantics, labels, accessible names, landmarks, live updates | `references/semantics-and-names.md` |
| Tab order, focus visibility, traps, restoration, route changes | `references/keyboard-focus-and-routing.md` |
| Labels, validation, recoverable errors, authentication | `references/forms-errors-authentication.md` |
| Modal dialogs, disclosure, responsive navigation | `references/dialogs-disclosures-navigation.md` |
| Tabs, comboboxes, listboxes, grids, menus, other composites | `references/composite-widgets.md` |
| Contrast, reflow, zoom, targets, drag, motion, media | `references/visual-input-and-motion.md` |
| Automated checks, manual protocols, AT matrix, evidence | `references/testing-and-evidence.md` |
| Framework or skill boundary | `references/routing.md` |
| Validate common outcomes without claiming conformance | `references/outcome-probes.md` |

## Decision Rules

- Treat WCAG 2.2 success criteria, HTML/ARIA specifications, and informative tutorials/patterns as separate layers. See `references/source-index.md`.
- Use WAI-ARIA 1.2 only when native host-language semantics do not provide the required behavior. ARIA changes semantics; it does not create keyboard behavior or visual presentation.
- Use the Accessible Name and Description Computation 1.2 algorithm for edge cases. Do not substitute a priority mnemonic; inspect the computed accessibility tree and name.
- For a modal, prefer `<dialog>.showModal()` when it supports the target environment. Keep background content unavailable/inert, choose initial focus for the content and task, provide a visible close path, and return focus logically. Do not hide a backdrop with `aria-hidden` or hide an ancestor of the dialog.
- Treat ordinary responsive navigation as a disclosure over ordinary links, not an ARIA menu. Use menu semantics only with the application-menu keyboard contract.
- Target Size (Minimum) is 24 by 24 CSS pixels at WCAG 2.2 AA, subject to its spacing, equivalent, inline, user-agent, and essential exceptions. A larger target may be a product goal.

## Completion

Stop when each acceptance criterion has direct evidence or a recorded failed, blocked, or not-applicable result. Report residual risk and the exact evidence boundary; do not turn absent testing into a pass.

## When Not To Use

- For Hugo template architecture, theme-wide layout, or CMS rendering concerns, use [hugo-theme](../hugo-theme/SKILL.md) and its [design/accessibility reference](../hugo-theme/references/design-accessibility.md).
- For evidence gathering, scope decisions, or user-facing behavior outside accessibility, use [product-discovery](../product-discovery/SKILL.md), [product-methodology](../product-methodology/SKILL.md), or [product-design-and-ux](../product-design-and-ux/SKILL.md). Keep this skill responsible for accessibility interaction and conformance depth.
- For framework or library APIs, consult the current official documentation after defining this skill's semantic and interaction contract. React implementation details route to [react](../react/SKILL.md); Vite configuration routes to [vite](../vite/SKILL.md).
