---
name: base-ui-overview-quickstart
description: Use for Base UI onboarding, architecture orientation, quick-start setup, accessibility baseline, and release/version validation before component-level work.
---

# Base UI Overview and Quick Start

This is the entry point for Base UI knowledge in Kuzenbo. Use it before touching a specific component to confirm assumptions, version scope, and ownership.

## Scope

- Overview docs: Quick start, accessibility, releases, about page
- Global index references: Handbook/handbook entries, components, utilities
- Baseline release evidence for drift checks and compatibility gates

## Routing cues

- "what is Base UI", "quick start", "release notes", "about Base UI", "how to set up portal stacking", "what is in v1.2.0" → this skill
- "unstyled", "styling strategy", "customize behavior", "form patterns" with no concrete component → route to handbook/domain skills
- Concrete component/unified utility questions → route to the owning skill from `references/coverage-matrix.md`

## Canonical references

- https://base-ui.com/react/overview/quick-start
- https://base-ui.com/react/overview/accessibility
- https://base-ui.com/react/overview/releases
- https://base-ui.com/react/overview/about
- https://base-ui.com/react/handbook/styling
- https://base-ui.com/react/handbook/composition
- https://base-ui.com/react/handbook/customization
- https://base-ui.com/react/handbook/forms
- https://base-ui.com/react/handbook/typescript
- https://base-ui.com/react/overview/releases/v1-2-0
- https://base-ui.com/llms.txt

## Key operating rules

- Base UI is unstyled and composition-first; `render`, `className`, and `style` state callbacks are primary extension points.
- Portals should be layered with app shell `isolation: isolate` guidance from quick start.
- Accessibility remains opt-in beyond base semantics: labels/role attributes/keyboard behavior still need explicit integration in app-level UI.

## Maintenance

- Snapshot date: 2026-02-13
- Release anchor snapshot: 1.2.0 (2026-02-12)
- Refresh cadence: quarterly or on `@base-ui/react` dependency update
- Upstream changelog anchor: https://github.com/mui/base-ui/blob/master/CHANGELOG.md

## References

- [Source map](./references/source-map.md)
- [Release snapshot](./references/release-snapshot.md)
- [Coverage matrix](./references/coverage-matrix.md)
