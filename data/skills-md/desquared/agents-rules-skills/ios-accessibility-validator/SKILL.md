---
name: ios-accessibility-validator
description: Checks and suggests accessibility improvements for SwiftUI and UIKit code including VoiceOver labels, dynamic type support, and color contrast. Use when creating or modifying UI components, views, or when the user asks about accessibility.
---

# Accessibility Validator

## Checklist

### VoiceOver
- [ ] Interactive elements have `.accessibilityLabel()`
- [ ] Decorative elements: `.accessibilityHidden(true)`
- [ ] Related elements: `.accessibilityElement(children: .combine)`
- [ ] Labels are localized

### Dynamic Type
- [ ] Use `.font(.body)` not `.system(size:)`
- [ ] Use `@ScaledMetric` for spacing
- [ ] Layout adapts to large text

### Color Contrast
- [ ] Text: 4.5:1 (normal), 3:1 (large)
- [ ] Use semantic colors (`.primary`, `.secondary`)
- [ ] Color not sole indicator

### Touch Targets
- [ ] Minimum 44x44pt

## Quick Fixes

| Issue | Fix |
|-------|-----|
| No label | `.accessibilityLabel("desc")` |
| Decorative | `.accessibilityHidden(true)` |
| Group | `.accessibilityElement(children: .combine)` |
| Small target | `.frame(minWidth: 44, minHeight: 44)` |
| Fixed font | Use `.body`, `.headline`, etc. |

## Severity

- 🔴 Critical: Blocks accessibility
- 🟡 Moderate: Reduces usability
- 🟢 Minor: Enhancement
