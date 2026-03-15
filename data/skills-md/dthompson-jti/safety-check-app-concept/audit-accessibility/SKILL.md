---
name: audit-accessibility
description: WCAG 2.1 AA accessibility audit. Use to ensure the application is accessible to all users.
---

# Audit Accessibility

WCAG 2.1 AA compliance review.

## When to Use
- Before releases
- After adding interactive components
- Accessibility compliance check

## Approach

### Step 1: Project Invariants (Required)
**Before auditing**, check `docs/knowledge-base/` for accessibility-specific constraints:
- Any documented a11y requirements
- Component-specific ARIA patterns
- Flag any violation of documented invariants as **Critical** priority.

### Step 2: Focus Areas

#### Screen Reader
- [ ] Interactive elements announced correctly
- [ ] Form labels read properly
- [ ] Error messages conveyed
- [ ] Landmarks defined

#### Keyboard Navigation
- [ ] All controls reachable via Tab
- [ ] Focus order logical
- [ ] Focus visible (ring)
- [ ] Escape closes modals

#### Color & Contrast
- [ ] Text contrast ≥4.5:1 (normal), ≥3:1 (large)
- [ ] Not relying on color alone
- [ ] Works with high contrast mode

#### Motion
- [ ] Respects `prefers-reduced-motion`
- [ ] No auto-playing animations >5s

### Step 3: Testing
1. Run automated tools (Lighthouse, axe)
2. Manual keyboard testing
3. Screen reader spot-check

### Output
Prioritized findings with WCAG criterion references (e.g., "WCAG 1.4.3 Contrast").
