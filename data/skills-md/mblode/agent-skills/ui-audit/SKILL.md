---
name: ui-audit
description: Audits web UI quality across accessibility, interaction, forms, typography, navigation, layout, performance, motion, and microcopy. Use when reviewing or refining frontend UI before merge or release, or when the user asks for a UI, UX, or accessibility audit.
---

# UI Audit

Final-pass audit workflow for web interfaces. Focuses on concrete issues with concrete fixes.

## Trigger Cues

Use this skill when:
- The user asks for a UI quality audit, design QA, polish pass, or pre-release review
- The task requires accessibility, keyboard, form usability, typography, or interaction checks
- The request includes loading/error/empty states, responsiveness, or visual stability checks
- The request mentions visual hierarchy, dense product chrome, headers, tabs, sidebars, icons, or separator cleanup

## Audit Workflow

Copy and track this checklist during the audit:

```text
Audit progress:
- [ ] Step 1: Scope changed surfaces and select relevant categories
- [ ] Step 2: Run CRITICAL checks first (a11y, interaction, forms)
- [ ] Step 3: Run HIGH/MEDIUM checks for the same surfaces
- [ ] Step 4: Report findings with file:line and concrete fixes
- [ ] Step 5: Re-check touched files and mark passes
```

1. Audit only changed pages/components unless a full sweep is requested.
2. Prioritize `CRITICAL` and `HIGH` findings before medium-priority polish.
3. For motion behavior, also apply `ui-animation` for timing/easing/reduced-motion details.
4. After fixes, rerun the relevant rules before finalizing.
5. When hierarchy or chrome cleanup is in scope, use the navigation, layout, and extra-polish sections in `craft-checklist.md` before reporting.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Accessibility and Semantics | CRITICAL | `a11y-` |
| 2 | Keyboard and Interaction | CRITICAL | `interaction-` |
| 3 | Forms and Validation | CRITICAL | `forms-` |
| 4 | Typography and Readability | HIGH | `type-` |
| 5 | Navigation and Feedback | HIGH | `nav-` |
| 6 | Layout and Resilience | HIGH | `layout-` |
| 7 | Performance and Visual Stability | HIGH | `perf-` |
| 8 | Motion and Theme Behavior | HIGH | `motion-` |
| 9 | Content and Microcopy | MEDIUM | `copy-` |

## Quick Reference

Read only what is needed for the current audit scope:
- Category map and impact rationale: `rules/_sections.md`
- Rule-level guidance and examples: `rules/<prefix>-*.md`
- Full craft sweep: `craft-checklist.md`
- Typography deep sweep: `typography-checklist.md`

Example rule files:

```
rules/a11y-semantic-html-first.md
rules/forms-inline-errors-first-focus.md
rules/perf-image-dimensions-and-priority.md
```

Each rule file contains:
- Why the rule matters
- Incorrect example
- Correct example

## Review Output Contract

Report findings in this format:

```markdown
## UI Audit Findings

### path/to/file.tsx
- [CRITICAL] `a11y-icon-controls-labeled`: Icon button is missing an accessible name.
  - Fix: Add `aria-label="Close dialog"` (or visible text label).

### path/to/clean-file.tsx
- ✓ pass
```

- Group findings by file.
- Use `file:line` when line numbers are available.
- State issue and propose a concrete fix.
- Include clean files as `✓ pass`.
