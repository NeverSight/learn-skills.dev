---
name: all-in-one-ui-ux-design
description: Unified UI/UX operating system for planning, designing, implementing, and auditing modern interfaces across web and mobile stacks. Use when requests involve creating, redesigning, reviewing, fixing, or optimizing pages/components (landing pages, dashboards, SaaS apps, admin panels, e-commerce, portfolios, blogs, mobile screens) and require strong visual direction plus accessibility, interaction, performance, and responsive quality.
---

# All-in-One UI/UX Design

Use this skill as the default end-to-end UI/UX system.
Keep this file focused on workflow. Load reference files only when needed.

Goal: deliver memorable interfaces that are production-ready, accessible, and maintainable.

## Start Here

Collect the minimum context before generating or reviewing code:

1. Product context: product type, audience, tone, and brand constraints.
2. Scope: full page/app, component set, redesign, or UI audit.
3. Platform and stack: web/mobile + framework/library choices.
4. Required states: loading, empty, error, success, disabled, and edge cases.
5. Delivery target: prototype, production code, audit findings, or design system spec.

If details are missing, ask 1-3 focused questions. If the user prefers speed, proceed with explicit assumptions.

## Mode Selection

Pick the mode that matches intent:

1. `build`: design and implement new UI.
2. `redesign`: keep functionality, replace visual and interaction layer.
3. `audit`: review existing UI and return actionable findings.
4. `design-system`: define tokens, type scale, and component primitives before coding.
5. `flow`: design multi-screen journeys (onboarding, checkout, settings, dashboards).

For mixed requests, run `design-system -> build -> audit` in sequence.

## Default Recommendations

Use these defaults unless the user asks otherwise:

1. Stack selection:
   Use the stack already present in the codebase.
   If no stack is present and the task is web, default to `html-tailwind`.
   If no stack is present and the task is mobile, use platform-native patterns.
2. Audit depth:
   Use full checklist audit by default.
   Use quick audit only when the user explicitly asks for speed over depth.
3. Creativity:
   Do not rely on rigid templates as the primary output.
   Use a bespoke direction per project, with reusable principles instead of cloned layouts.
   Use `assets/primitives/` as composable scaffolding, not final visual identity.

## Reference Loading Map

Load only what the task needs:

| File | Load when |
|---|---|
| [references/creative-direction.md](references/creative-direction.md) | Choosing style direction, typography personality, palette mood, layout composition, and visual differentiation |
| [references/system-build-playbook.md](references/system-build-playbook.md) | Building implementation plans, selecting stacks, applying UX priority rules, and using final delivery checklists |
| [references/web-interface-guidelines.md](references/web-interface-guidelines.md) | Auditing UI code for accessibility, interaction, performance, copy quality, and anti-pattern detection |

## Asset Kit

Use these optional assets when implementation speed is needed without sacrificing originality:

| Asset | Use for |
|---|---|
| [assets/primitives/tokens.css](assets/primitives/tokens.css) | Typography, color, spacing, radius, elevation, and semantic token scaffold |
| [assets/primitives/motion.css](assets/primitives/motion.css) | Motion tokens, entry effects, and reduced-motion-safe behavior |
| [assets/primitives/layout.css](assets/primitives/layout.css) | Responsive layout primitives (container, stack, cluster, grid, section, surface) |
| [assets/primitives/component-states.css](assets/primitives/component-states.css) | Accessible default states for buttons, fields, and cards |
| [assets/blueprints/semantic-shell.html](assets/blueprints/semantic-shell.html) | Minimal semantic page skeleton for rapid prototyping |

Asset rules:

1. Copy only what is needed.
2. Retheme tokens before final delivery.
3. Recompose layouts per project; never ship blueprint defaults unchanged.

## Core Principles

1. Commit to a clear aesthetic direction. Do not produce generic template-looking UI.
2. Keep style and interaction consistent across the entire surface.
3. Prioritize accessibility and usability before decorative polish.
4. Use motion intentionally; communicate state changes, do not add noise.
5. Build for responsive behavior and real content from the first pass.
6. Favor readable, maintainable code and tokenized styling over ad hoc values.

## Non-Negotiable Quality Bar

Apply these rules in every mode:

1. Typography must feel intentional. Avoid default stacks and repetitive safe choices.
2. Color must be cohesive. Use design tokens or CSS variables for primary, secondary, accent, and semantic states.
3. Interactive elements must expose visible hover and keyboard focus states.
4. Touch targets must be at least 44x44px on touch interfaces.
5. Respect reduced-motion preference and avoid expensive animation properties.
6. Provide complete state coverage: normal, hover, focus, active, disabled, loading, empty, error, success.
7. Prevent layout shifts and clipping with explicit media sizing and robust text overflow handling.
8. Avoid anti-patterns listed in [references/web-interface-guidelines.md](references/web-interface-guidelines.md).

## Anti-Generic Design Checks (Required)

Before final delivery, fail the output if any of these remain:

1. Default-looking typography choices with no clear intent.
2. Generic gradient-heavy or template-first visual direction with weak brand fit.
3. Boilerplate page composition that could belong to any product with minimal changes.
4. Decorative motion that does not communicate hierarchy, feedback, or state.
5. No memorable differentiator in type, layout, interaction, or visual texture.

## End-to-End Workflow

### 1. Understand and Frame

1. Translate request into problem statement and success criteria.
2. Extract constraints: brand, compliance, performance, deadlines.
3. Define deliverables and acceptance criteria before coding.

### 2. Choose a Design Direction

1. Pick one primary visual direction and one secondary supporting influence.
2. Define mood words, contrast level, texture strategy, and motion character.
3. Lock direction with a concise design brief before component implementation.

Use [references/creative-direction.md](references/creative-direction.md) for direction options and anti-generic guardrails.

### 3. Define the Design System

Create a compact spec:

1. Color tokens: background, surface, text, muted, border, primary, accent, danger, success.
2. Typography system: display/headline/body/caption styles and line-height rules.
3. Spacing and radius scales.
4. Elevation/shadow system and border treatments.
5. Motion tokens: durations, easing, and reduced-motion fallbacks.
6. Component primitives: button, input, select, card, modal, tooltip, toast, table.

Use [references/system-build-playbook.md](references/system-build-playbook.md) for rule priority and stack-specific guidance.

### 4. Build Layout and Interaction Architecture

1. Draft responsive structure first (mobile-first breakpoints unless specified otherwise).
2. Define hierarchy, grouping, and scanning paths.
3. Assign interaction patterns: navigation, filtering, validation, feedback.
4. Plan edge states early to avoid late-stage regressions.

### 5. Implement by Stack

1. Respect user-selected stack. If unspecified, apply the defaults from the `Default Recommendations` section above.
2. Keep implementation style-consistent with the design system.
3. Use semantic HTML and accessible component APIs.
4. Prefer composable primitives and reusable tokens over one-off classes.
5. If using the Asset Kit, customize tokens, composition, and interaction details before delivery.

### 6. Audit Before Delivery

Run self-review against [references/web-interface-guidelines.md](references/web-interface-guidelines.md):

1. Accessibility and semantic correctness.
2. Focus/keyboard and touch quality.
3. Responsive behavior and overflow handling.
4. Motion/performance and hydration safety.
5. Copy clarity and interaction labels.

## Audit Mode Output Contract

When request intent is review/audit/check:

1. Findings first, ordered by severity.
2. Group by file with `file:line` locations.
3. Keep each finding terse and actionable.
4. Mention pass status only when file has no issues.
5. Include residual risks or missing test coverage.

Default behavior:

1. Run strict/full audit against the complete guideline set.
2. Switch to quick audit only when user asks for lightweight review.

Format:

```text
## path/to/file.tsx

path/to/file.tsx:42 - issue summary
path/to/file.tsx:77 - issue summary

## path/to/another.tsx

pass
```

## Build Mode Output Contract

When request intent is implementation:

1. Provide final code or patch.
2. Summarize design direction in 2-4 bullets.
3. Confirm key accessibility and responsive decisions.
4. List known tradeoffs and follow-up improvements.

## Rapid Prompt Pattern

Use this structure internally when requirements are vague:

1. "Who is this interface for and what is the core action?"
2. "What emotional tone should the UI convey?"
3. "What stack or platform constraints apply?"
4. "What quality constraints are mandatory (a11y, perf, brand, localization)?"

If user does not answer, continue with assumptions and state them clearly.

## Completion Checklist

Before final delivery, confirm:

1. Visual direction is distinctive and coherent.
2. All critical interactions have hover/focus/active/disabled states.
3. Accessibility checks pass for labels, semantics, focus, and contrast.
4. Mobile and desktop layouts are verified.
5. Performance-sensitive behavior (images, animations, lists) is handled.
6. Copy and error states are specific and user-actionable.
