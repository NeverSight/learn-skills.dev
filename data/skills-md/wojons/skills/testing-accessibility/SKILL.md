---
name: testing-accessibility
description: Test application accessibility compliance
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Accessibility Testing

Test applications for accessibility compliance with WCAG guidelines to ensure usability for people with disabilities.

## When to use me

Use this skill when:
- Developing public-facing applications
- Complying with legal requirements (ADA, Section 508)
- Ensuring inclusive design for all users
- Testing screen reader compatibility
- Validating keyboard navigation
- Checking color contrast and visual accessibility
- Testing with assistive technologies

## What I do

- Test screen reader compatibility and semantic HTML
- Validate keyboard navigation and focus management
- Check color contrast ratios for visual accessibility
- Test form labels and input accessibility
- Verify proper heading structure and document outline
- Test alternative text for images and media
- Check ARIA attributes and roles
- Validate touch target sizes on mobile devices
- Test with actual assistive technologies

## Examples

```bash
# Automated accessibility testing
npm run test:a11y                 # axe-core, pa11y
npx pa11y https://app.example.com
npx axe https://app.example.com --save results.json

# Lighthouse accessibility audits
npx lighthouse https://app.example.com --output json --only-categories=accessibility

# Color contrast checking
npx color-contrast-checker --url https://app.example.com

# Screen reader testing guidance
# Manual testing with NVDA, JAWS, VoiceOver, TalkBack

# HTML validation
npm run html-validator           # HTML validation
python -m html5validator src/   # HTML5 validation
```

## Output format

```
Accessibility Test Results:
──────────────────────────────
WCAG 2.1 AA Compliance:

Critical Issues (4):
  ❌ Missing form labels (3 instances)
    Impact: Screen reader users cannot identify form fields
    Fix: Add <label> elements with for attributes

  ❌ Insufficient color contrast (12 elements)
    Impact: Low vision users cannot read text
    Fix: Increase contrast ratio to 4.5:1 minimum

  ❌ Missing alternative text for images (7 images)
    Impact: Screen reader users miss image content
    Fix: Add descriptive alt text

  ❌ Keyboard trap in modal dialog
    Impact: Keyboard users cannot escape modal
    Fix: Implement proper focus management

Moderate Issues (8):
  ⚠️ Heading structure skips levels (h2 → h4)
  ⚠️ ARIA attributes missing on dynamic content
  ⚠️ Form error messages not associated with fields

Passed Checks (42):
  ✅ Semantic HTML structure
  ✅ Keyboard navigation works
  ✅ Focus indicators visible
  ✅ Language attribute set

Summary: 4 critical, 8 moderate issues found
Compliance: Partially compliant with WCAG 2.1 AA
```

## Notes

- Automated tools catch ~30-40% of accessibility issues
- Manual testing with assistive technologies is essential
- Follow WCAG 2.1/2.2 guidelines (A, AA, AAA levels)
- Test with real users with disabilities when possible
- Consider cognitive and motor disabilities beyond visual
- Implement accessibility early in development cycle
- Train developers on accessible coding practices
- Create accessibility statement for your application
