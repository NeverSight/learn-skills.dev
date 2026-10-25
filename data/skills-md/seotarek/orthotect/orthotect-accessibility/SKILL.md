---
name: orthotect-accessibility
description: Audit and enforce WCAG 2.2 Level AA/AAA accessibility standards. Verifies color contrast, keyboard navigation, focus appearance, touch target sizes (min 44x44px), and screen reader announcements. Use before shipping any UI.
---

# Skill: Orthotect WCAG 2.2 Accessibility Auditing

Use this skill to audit, diagnose, and resolve accessibility barriers in web applications according to WCAG 2.2 Level AA (and Level AAA where required).

## Critical Verification Criteria
1. **WCAG 1.4.3 / 1.4.6 Contrast:** Normal text >= 4.5:1 (AA) or >= 7.0:1 (AAA); large text >= 3.0:1 (AA) or >= 4.5:1 (AAA).
2. **WCAG 1.4.11 Non-text Contrast:** UI components and focus indicators >= 3.0:1 against background.
3. **WCAG 2.1.1 Keyboard Navigation:** 100% of interactive controls operable without a mouse.
4. **WCAG 2.4.7 / 2.4.13 Focus Appearance:** High-contrast visible focus indicator on keyboard tab navigation.
5. **WCAG 2.5.8 Target Size:** Minimum pointer target 24×24px; touch target minimum 44×44px.

## Deterministic Verification
```bash
# Mathematical contrast verification across all token pairs
python3 gates/gate_contrast_wcag.py
```
