---
name: vue-component
description: >-
  Builds frontend components/pages/composables in the project's UI stack.
  Use when implementing UI features, reusable components, and typed state flows.
---

# UI Component Skill

## When to Apply
- User asks for frontend component/page work.
- Existing UI needs refactor into reusable units.

## Workflow
1. Read UI constraints from `specs/ui-spec.md` and `specs/specs.md`.
2. Detect project UI stack and conventions from repository.
3. Implement component/page with:
   - clear props/contracts
   - typed state/events
   - loading/error/empty states
   - accessibility basics (labels, focus, landmarks)
4. Reuse existing design system/component primitives first.

## Quality Bar
- No `any` unless unavoidable and justified.
- Avoid duplicated business logic in view components.
- Keep components composable and testable.
