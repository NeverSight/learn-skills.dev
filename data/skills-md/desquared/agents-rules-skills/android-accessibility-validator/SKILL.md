---
name: android-accessibility-validator
description: Checks and suggests accessibility improvements for Jetpack Compose and Android Views including TalkBack labels, dynamic text support, and color contrast. Use when creating or modifying UI components, screens, or when the user asks about accessibility.
---

# Accessibility Validator (Android)

## Checklist

### TalkBack
- [ ] Interactive elements have `contentDescription` via semantics
- [ ] Decorative elements: `Modifier.semantics { invisibleToUser() }`
- [ ] Related elements: `Modifier.semantics(mergeDescendants = true)`
- [ ] contentDescription is localized

### Dynamic Text
- [ ] Use `sp` for text sizes, not `dp`
- [ ] Use `MaterialTheme.typography` scales
- [ ] Layout adapts to large text sizes

### Color Contrast
- [ ] Text: 4.5:1 (normal), 3:1 (large 18sp+)
- [ ] Use Material Theme semantic colors
- [ ] Color not sole indicator

### Touch Targets
- [ ] Minimum 48dp
- [ ] Use `Modifier.minimumInteractiveComponentSize()`

## Quick Fixes

| Issue | Fix |
|-------|-----|
| No contentDescription | `Modifier.semantics { contentDescription = "desc" }` |
| Decorative | `Modifier.semantics { invisibleToUser() }` |
| Group | `Modifier.semantics(mergeDescendants = true)` |
| Small target | `Modifier.size(48.dp)` |
| Fixed font | Use MaterialTheme.typography.bodyLarge |

## Severity

- 🔴 Critical: Blocks accessibility
- 🟡 Moderate: Reduces usability
- 🟢 Minor: Enhancement
