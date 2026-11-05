---
name: flutter-accessibility
description: Build or audit Flutter accessibility for semantics, screen readers, focus, keyboard access, text scaling, contrast, target size, and motion preferences. Pair with flutter-responsive-layout when large text causes reflow, clipping, or overflow across constraints.
---

# Flutter Accessibility

Treat accessibility as behavior to implement and verify, not a label-only cleanup.

## Audit the flow

Identify the primary task, semantic reading order, actionable controls, dynamic announcements, focus transitions, text scaling, contrast, motion, and keyboard or switch access on each target platform.

## Rules

- Prefer semantic built-in controls before manually adding `Semantics`.
- Give custom interactive widgets roles, labels, values, states, and actions without duplicating child semantics.
- Keep visual, semantic, and keyboard focus order aligned.
- Allow text to scale without clipping or hiding essential actions.
- Meet platform-appropriate target sizes and do not rely on color alone.
- Preserve functionality with reduced motion and increased contrast preferences.
- Announce meaningful asynchronous state changes without creating repetitive noise.
- Exclude decorative content from the semantics tree when it adds no information.

## Verification

Use widget tests with semantics enabled and Flutter's accessibility guideline matchers where suitable. Also test the changed flow with TalkBack or VoiceOver and keyboard navigation on supported desktop/web targets.

## References

- Read [semantics and screen readers](references/semantics-and-screen-readers.md) when annotating custom widgets with Semantics, merging subtrees, or triggering dynamic voice announcements.
- Read [target sizes and contrast](references/target-sizes-and-contrast.md) when auditing WCAG AA contrast ratios, minimum touch targets, or large text scaling adaptation.

## Sources

- [Flutter accessibility](https://docs.flutter.dev/ui/accessibility)
- [Accessibility testing](https://docs.flutter.dev/ui/accessibility/accessibility-testing)
