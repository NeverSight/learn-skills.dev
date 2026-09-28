---
name: ui-engineering
description: >-
  Design, implement, refine, or review user interfaces across web, desktop, mobile surfaces, and
  hybrid/WebView boundaries. Use for responsive/adaptive layout, interaction behavior, keyboard/
  pointer/touch input, accessibility, visual hierarchy, UX copy, and durable design-system work.
  Preserve project design truth and use optional visual-design providers only when they match the
  current concern; provider availability never overrides DESIGN.md or product behavior.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# UI Engineering

Treat UI as product behavior plus surface engineering, not decoration.

## Trigger

Use for UI layout, interaction, responsive/adaptive behavior, accessibility, visual refinement, UX copy, or surface-specific behavior on web, desktop, mobile, or hybrid/WebView products.

Do not trigger for mobile lifecycle/background/offline behavior without a UI concern; that belongs to mobile-engineering.

## Workflow

1. Inspect current product behavior, existing components/tokens, DESIGN.md, platform targets, and the actual surface before inventing a new visual language.
2. Classify the surface: web, desktop, mobile, or hybrid/WebView. A task may span more than one.
3. Identify the primary UI concern: structure/layout, typography, color, interaction, input modality, motion, accessibility, responsive/adaptive behavior, UX copy, or visual polish.
4. Preserve established design/system patterns unless the task intentionally changes them.
5. Make behavior work across relevant viewport/window sizes and input modes rather than optimizing a single screenshot.
6. Use motion sparingly and purposefully; respect reduced-motion and accessibility needs.
7. When a specialist visual-design provider is available, route only the matching concern to it and keep project DESIGN.md authoritative.
8. Verify rendered behavior directly when the environment can render it; otherwise use build/static evidence and disclose the visual-verification gap.

## Durable design

Update DESIGN.md only when a change establishes durable visual or interaction truth. One-off spacing fixes belong in code, not permanent design documentation.

## Composition

Mobile-specific lifecycle, offline/local-first, backgrounding, device capabilities, or native-shell behavior should add a mobile-engineering concern. Complex WebView bridges may also require API/integration/security concerns.

## Stop

Stop when the requested UI behavior is implemented or specified, relevant surfaces and input modes are covered, accessibility concerns are handled proportionally, and available visual evidence is sufficient.
## Reference Guide

Load only the references needed for the current task:

- [interaction accessibility](references/interaction-accessibility.md)
- [impeccable](references/providers/impeccable.md)
- [responsive adaptive](references/responsive-adaptive.md)
- [surface awareness](references/surface-awareness.md)
- [visual craft](references/visual-craft.md)
- [webview hybrid](references/webview-hybrid.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [design](references/_shared/artifacts/design.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
