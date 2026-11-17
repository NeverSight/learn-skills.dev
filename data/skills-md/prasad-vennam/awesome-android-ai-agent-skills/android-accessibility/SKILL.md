---
name: android-accessibility
description: "Use when improving app accessibility, ensuring WCAG compliance, or fixing TalkBack navigation for Android."
category: accessibility
risk: low
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@accessibility"
    - "wcag-compliance"
    - "talkback-support"
    - "content-description"
    - "semantic-tags"
---

# Android Accessibility Excellence ♿🛡️

Standard practices for creating inclusive, easy-to-use Android applications that comply with WCAG 2.1+ standards.

## ⚡ When to Use
- **Accessibility Audit**: Reviewing current UI for screen reader issues.
- **Compose Semantics**: Customizing how UI elements are announced.
- **Contrast Ratios**: Ensuring text is readable for low-vision users.
- **Screen Reader Support**: Optimizing navigation with TalkBack.
- **Touch Target Sizes**: Ensuring buttons and links are easy to hit.

## 🏗️ The 4 Principles (POUR)

1.  **Perceivable**: Users can perceive all info via sight, sound, or touch.
2.  **Operable**: Users can interact with the app via various methods.
3.  **Understandable**: UI and navigation are predictable.
4.  **Robust**: Compatible with many assistive tools.

## 🛠️ Compose Semantics Essentials

### 1. `contentDescription`
- **Rule**: Every `Image`, `IconButton`, or clickable decorative icon MUST have a descriptive `contentDescription`.
- **Bad**: `contentDescription = "icon"` or `null` for meaningful icons.
- **Good**: `contentDescription = "Search for products"` or `contentDescription = null` for purely decorative items.

### 2. Semantic Properties
- Use `Modifier.semantics { ... }` for custom descriptions or element roles.
- Use `Modifier.clearAndSetSemantics { ... }` to hide complex child hierarchies from screen readers.

### 3. Merging Descendants
- For a list item, use `Modifier.semantics(mergeDescendants = true)` to announce the whole item at once.
  ```kotlin
  Row(modifier = Modifier.semantics(mergeDescendants = true).clickable { ... }) {
      Text("Order #123")
      Text("Status: Shipped")
  }
  ```

## 📐 Design Best Practices

- **Contrast**: Aim for 4.5:1 for normal text and 3:1 for large text.
- **Touch Targets**: Minimum size of **48dp x 48dp**.
- **Dynamic Type**: Ensure layouts resize correctly for large font scales (`@PreviewFontScales`).

## 🧪 Testing and Verification

- **Accessibility Scanner**: Use the Google app to automatically scan screens for common issues.
- **TalkBack**: Manually test with the screen reader enabled on a physical device.
- **Lint Checks**: Enable `@LintRule` for missing `contentDescription`.

## 📜 Checklist for Developers

- [ ] **Descriptive Labels**: All actionable items state their purpose (e.g., "Delete Comment" vs "Delete").
- [ ] **State Announcements**: Use `liveRegion` or `AnnounceAccessibilityEvent` for dynamic updates (e.g., "Added to cart").
- [ ] **Navigation Order**: Ensure focus moves in a logical left-to-right, top-to-bottom order.
- [ ] **Role Identification**: Mark elements as buttons, checkboxes, or headers.

## 🔗 Related Resources
- [Android Accessibility Help](https://developer.android.com/guide/topics/ui/accessibility)
- [Compose Accessibility Guide](https://developer.android.com/jetpack/compose/accessibility)
