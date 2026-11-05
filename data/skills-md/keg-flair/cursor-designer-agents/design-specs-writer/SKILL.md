---
name: design-specs-writer
description: Generates structured, engineering-ready design specs for components or flows (states, behaviors, edge cases, a11y, token hooks, open questions). Use when the user asks to “write a spec”, “handoff notes”, “document this component/flow”, or “spec out this feature”.
---

# Design Specs Writer

## Defaults

- **Engineering-ready**: concrete behaviors, states, edge cases, and decision points (not just UI description).
- **Tool-agnostic**: do not assume a specific design tool or plugin.
- **System-first**: prefer existing patterns/tokens/components; propose additions only when reusable.
- **Honest uncertainty**: separate what’s provided vs inferred; include assumptions and how to verify.

## Constraints

- **Do not invent** product policy, existing component APIs, analytics numbers, or platform constraints.
- **Ask at most 3 clarifying questions**, only if the answers materially change the spec’s API surface or states.
- **Accessibility baseline**: include keyboard/focus/labels/contrast/motion considerations for interactive UI.

## Clarifying questions (ask max 3)

Ask only if missing and it changes the spec’s structure materially.

1. Is this a **component** or a **flow** (and what screens/steps are in scope)?
2. What are the **platform targets** (web/iOS/Android) and theming requirements (light/dark/high-contrast)?
3. What’s the **success definition** (user goal + metric or qualitative outcome)?

## Inputs to request (only if missing)

- Component/feature name + brief purpose
- Screenshots or a Figma link (optional but best)
- Primary user goal + key constraints (a11y, localization, auth/payments, compliance/trust)
- Any existing design system primitives/tokens to align with

## Output template

Use this template; compress sections for simple components.

```markdown
## [Component / Feature Name] — Design spec

### Assumptions / constraints
- …

### Overview
- **What it is**:
- **Who it’s for**:
- **Primary user goal**:
- **Success definition**:

### In scope / out of scope
- **In scope**:
- **Out of scope**:

### UX requirements (non-negotiables)
- …

### Anatomy (for components) / Steps (for flows)
- **Anatomy / slots** (if component):
  - …
- **Steps** (if flow):
  1. …

### Variants (if applicable)
- **Variant props**:
- **Invalid combinations**:

### States
| State | Trigger | UI behavior | Notes |
| --- | --- | --- | --- |
| Default | … | … | … |
| Loading | … | … | … |
| Empty | … | … | … |
| Error | … | … | … |
| Disabled | … | … | … |

### Interactions & behavior
- **User actions**:
- **System feedback**: loading/progress/success/failure
- **Undo / escape hatches**:
- **Performance / latency**: skeletons/spinners/timeouts (as applicable)

### Content guidelines
- **Labels**:
- **Error messages**: (pattern + examples)
- **Empty states**: (pattern + examples)
- **Length constraints**: truncation/wrapping/localization notes

### Edge cases
- Long strings / overflow
- Permissions / role differences (if applicable)
- Slow network / offline / retries
- Bulk operations (if applicable)

### Accessibility
- **Keyboard**:
- **Focus management**:
- **Labels / names**:
- **Contrast**:
- **Motion + reduced motion**:

### Design system hooks (token-first)
- **Existing components to reuse**:
- **Token hooks**: color / type / spacing / radius / elevation
- **If new tokens/variants are needed**: list + rationale

### Instrumentation (optional)
- Suggested events + properties (only if user asked or it’s critical)

### Open questions (owners TBD)
- [ ] …

### Test plan / how to verify
- **Design QA**:
- **Engineering QA**:
- **User validation**:
```

## Domain notes (optional, only when relevant)

If the user indicates HR/enterprise/compliance constraints, incorporate:

- **Role-based access** and permission-gated UI
- **PII/sensitive data** handling (masking, audit trails)
- **Localization** (dates, currencies, names)

